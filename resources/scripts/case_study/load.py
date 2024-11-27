def load_logic(item, **kwargs):
    import pandas as pd
    from airflow.providers.postgres.hooks.postgres import PostgresHook

    # Connect to PostgreSQL using SQLAlchemy engine
    postgres_hook = PostgresHook("postgres_dibimbing").get_sqlalchemy_engine()

    # Read data from CSV
    df = pd.read_csv(f"data/case_study/{item['table']}.csv")

    # Connect to PostgreSQL and check if the table exists
    with postgres_hook.connect() as conn:
        table_exists = pd.read_sql(f"SELECT to_regclass('bronze.{item['table']}')", conn).iloc[0, 0]
        ingest_type = kwargs['var']['json'].get("case_study_ingest_type", {}).get(item['table'], "full")

        if not table_exists or ingest_type == "full":
            # If the table does not exist, create a new table in the bronze schema
            df.to_sql(
                name=item['table'],
                con=conn,
                schema="bronze",
                if_exists="replace",
                index=False,
            )
            print("Load data ke bronze table berhasil")
        else:
            # If the table exists, load data to a temporary table and prepare for merge
            conn.execute(f"DROP TABLE IF EXISTS temp.{item['table']}")
            conn.execute(f"CREATE TABLE temp.{item['table']} (LIKE bronze.{item['table']})")
            df.to_sql(
                name=item['table'],
                con=conn,
                schema="temp",
                if_exists="append",
                index=False,
            )
            print("Load data ke temp table berhasil")

# Prepare the SQL query for merging data from temp to bronze
query_merge = """
MERGE INTO bronze.{main_table} M
USING temp.{temp_table} T
ON {merge_on}
WHEN MATCHED THEN
UPDATE SET
{update_set}
WHEN NOT MATCHED THEN
INSERT ({insert_cols}) VALUES ({insert_vals})
""".format(
    main_table=item['table'],
    temp_table=item['table'],
    merge_on=" AND ".join(f'M."{col}" = T."{col}"' for col in item['merge_on']),
    update_set=", ".join(f'M."{col}" = T."{col}"' for col in df.columns),
    insert_cols=", ".join(f'"{col}"' for col in df.columns),
    insert_vals=", ".join(f'T."{col}"' for col in df.columns),
)

# Print and execute the merge query
print("Query merge:", query_merge)
conn.execute(query_merge)
print("Merge data berhasil")
