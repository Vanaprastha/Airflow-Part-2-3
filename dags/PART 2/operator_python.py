from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from datetime import datetime

def print_python(param1, **kwargs):
    print("ini adalah operator python")
    print(param1)
    print(kwargs['param2'])

@dag(schedule_interval='@daily', start_date=datetime(2023, 1, 1), catchup=False)
def operator_python():
    python = PythonOperator(
        task_id="python",
        python_callable=print_python,
        op_kwargs={
            "param1": "ini adalah param1",
            "param2": "ini adalah param2",
        },
    )
    return python  # Mengembalikan objek DAG

dag_instance = operator_python()  # Membuat instance DAG
