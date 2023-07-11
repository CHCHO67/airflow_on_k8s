from datetime import datetime, timedelta
import time

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 4, 24),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    dag_id="sample_dag",
    default_args=default_args,
    description="A sample DAG",
    schedule_interval=timedelta(days=1),
)

# Task 1: Print the current date
task1 = BashOperator(
    task_id="print_date",
    bash_command="date",
    dag=dag,
)


# Task 2: Python function to greet someone
def greet(name):
    print(f"Hello, {name}!")
    time.sleep(int(10))


task2 = PythonOperator(
    task_id="greet",
    python_callable=greet,
    op_kwargs={"name": "John"},
    dag=dag,
)

task1 >> task2
