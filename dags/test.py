from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import time
import requests


def print_hello():
    now = datetime.now()  # current date and time
    with open("/data/hello_world.txt", "w") as f:
        f.write(f"Hello World, Current Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(120)  # Sleep for 60 seconds


default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 6, 1),
}

dag = DAG(
    "hello_world",
    description="Simple tutorial DAG",
    schedule_interval="0 12 * * *",
    default_args=default_args,
    catchup=False,
)

start_operator = DummyOperator(task_id="start_task", dag=dag)

hello_operator = PythonOperator(
    task_id="hello_task", python_callable=print_hello, dag=dag
)

end_operator = DummyOperator(task_id="end_task", dag=dag)

start_operator >> hello_operator >> end_operator
