import airflow
from airflow.decorators import dag
from airflow import DAG
# from airflow.providers.cncf.kubernetes.operators.pod import (
#    KubernetesPodOperator,
# )
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

dag = DAG(
    'simmy_news_crawling',
    description='DAG to execute local python file',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 7, 7),
    catchup=False
)
# Bash 스크립트 정의
bash_script = """
    echo " Hello, simmy dag"
    python3 /home/simmy/airflow/dags/news_realtime.py
"""

bash_task = BashOperator(
    task_id='bash_task',
    bash_command=bash_script,
    dag=dag
)

if __name__ == "__main__":
    dag.cli()

## It tailed becaue of mongodb connection... rest code work correctly
# @dag(
#     dag_id="news_realtime",
#     start_date=airflow.utils.dates.days_ago(0),
#     schedule_interval="0 0 * * *",
#     max_active_runs=1,
#     catchup=False
# )
# def news_realtime():
#     news_realtime = KubernetesPodOperator(
#         task_id="news_realtime",
#         name="news_realtime",
#         image="news_realtime:v1"
#     )

#     news_realtime

# DAG = news_realtime()
