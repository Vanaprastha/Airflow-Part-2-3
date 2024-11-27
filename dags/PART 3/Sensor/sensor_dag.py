from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

@dag(schedule_interval=timedelta(minutes=1), start_date=datetime(2024, 8, 1), catchup=False)
def sensor_dag():
    start_task = EmptyOperator(task_id="start_task")
    end_task = EmptyOperator(task_id="end_task")
    
    wait_current_dag = ExternalTaskSensor(
        task_id="wait_current_dag",
        external_dag_id="sensor_sleep",
        external_task_id="end_task",
        execution_date_fn=lambda dt: dt.replace(second=0, microsecond=0),
        poke_interval=5,
    )

    def _wait_prev_dag_execution_date_fn(dt):
        print(dt, type(dt))
        return dt.replace(second=0, microsecond=0) - timedelta(minutes=2)

    wait_prev_dag = ExternalTaskSensor(
        task_id="wait_prev_dag",
        external_dag_id="sensor_sleep",
        external_task_id="end_task",
        execution_date_fn=_wait_prev_dag_execution_date_fn,
        poke_interval=5,
    )

    start_task >> wait_current_dag >> wait_prev_dag >> end_task

sensor_dag()
