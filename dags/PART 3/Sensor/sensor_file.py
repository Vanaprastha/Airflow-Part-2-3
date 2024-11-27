from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta

@dag(schedule_interval=timedelta(minutes=1), start_date=datetime(2024, 8, 1), catchup=False)
def sensor_file():
    start_task = EmptyOperator(task_id="start_task")
    end_task = EmptyOperator(task_id="end_task")
    
    wait_file = FileSensor(
        task_id="wait_file",
        filepath="watch/text.txt",
        poke_interval=5,
    )
    
    start_task >> wait_file >> end_task

sensor_file()
