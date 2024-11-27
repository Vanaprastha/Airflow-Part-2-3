from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import json
import requests

# Default arguments
default_args = {
    'start_date': datetime(2024, 1, 1),  # Tanggal mulai eksekusi DAG
    'retries': 3,  # Retry up to 3 times
    'retry_delay': timedelta(minutes=5),  # 5 minutes delay between retries
}

# Define DAG
dag = DAG(
    'rocket_launch_pipeline',
    default_args=default_args,
    schedule_interval='0 6 * * *'  # Set to run daily at 06:00 AM
)

# Task 1: Download launch data using BashOperator
fetch_data = BashOperator(
    task_id='fetch_rocket_data',
    bash_command='curl -L -o /tmp/launches.json https://llapi.thespacedevs.com/2.2.0/launch/upcoming',
    dag=dag
)

# Task 2: Extract image URLs from JSON
def extract_images():
    with open('/tmp/launches.json') as f:
        launches = json.load(f)
    image_urls = [launch['image'] for launch in launches['launches']]
    
    # Download the images
    for url in image_urls:
        download_image(url)

def download_image(url):
    response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(f'/tmp/{file_name}', 'wb') as f:
        f.write(response.content)

extract_images_task = PythonOperator(
    task_id='extract_images',
    python_callable=extract_images,
    dag=dag
)

# Task dependencies
fetch_data >> extract_images_task
