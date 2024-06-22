from datetime import datetime
import json
from airflow import DAG
from pandas import json_normalize

from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow. providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import timedelta
import sys

sys.path.append(r'C:\Users\Simmy\sungsim\dataEngineering\bitcoinTwit')
sys.path.append(r'C:\Users\Simmy\sungsim\dataEngineering\bitcoinTwit\preprocess')

from news_realtime import execute

default_args = {
    "start_date": datetime(2024, 6, 6)
}

dag = DAG(
    'news_realtime_pipeline',
    default_args=default_args,
    description='A news pipeline',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 6, 6),
    catchup=False,
    tags=['news']
)

hello_task = PythonOperator(
    task_id='print_hello',
    python_callable=execute,
    dag=dag,
)