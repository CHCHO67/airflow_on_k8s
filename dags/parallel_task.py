from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {"start_date": datetime(2021, 1, 1)}

dag = DAG(
    dag_id="parallel_task_sample", default_args=default_args, schedule_interval="@daily"
)

task_1 = BashOperator(task_id="task_1", bash_command='echo "Hello World"', dag=dag)

task_2 = BashOperator(task_id="task_2", bash_command='echo "Goodbye World"', dag=dag)

task_3 = BashOperator(task_id="task_3", bash_command='echo "Hello Again"', dag=dag)

task_4 = BashOperator(task_id="task_4", bash_command='echo "Goodbye Again"', dag=dag)

# 병렬 task 리스트 의존성 작성하기
task_1 >> [task_2, task_3] >> task_4
