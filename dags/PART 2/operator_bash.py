from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from datetime import datetime

@dag(
    dag_id="dag_with_bash_operator",
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),  # Specify a start date
    tags=["example"],
)
def operator_bash():
    bash = BashOperator(
        task_id="bash",
        bash_command="echo ini adalah operator bash",
    )

    return bash  # Return the task for proper DAG structure

# Instantiate the DAG
dag_instance = operator_bash()
