import airflow
from airflow.decorators import dag
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

dag = DAG(
    'simmy_saving_realestate_crawling',
    description='DAG to execute local python file',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 8, 14),
    catchup=False
)
# Bash 스크립트 정의
bash_script = """
    echo " Hello, simmy dag"
    python3 /home/simmy/airflow/dags/saving_realestate.py
"""

bash_task = BashOperator(
    task_id='bash_task',
    bash_command=bash_script,
    dag=dag
)

if __name__ == "__main__":
    dag.cli()