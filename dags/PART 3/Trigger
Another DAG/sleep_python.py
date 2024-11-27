from airflow.decorators import dag, task
from datetime import datetime

@dag()
def sleep_python():
    @task
    def sleep():
        import time
        time.sleep(30)

    # Memanggil task
    sleep_task = sleep()

sleep_python()
