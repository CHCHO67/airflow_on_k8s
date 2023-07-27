from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'me',
    'start_date': datetime(2023, 7, 7),
}

dag = DAG(
    'file-dag-test',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval='@once',
)

t1 = BashOperator(
    task_id='run_python_preprocess',
    bash_command='python3 /opt/airflow/dags/preprocess.py',
    dag=dag,
)

# t2 = BashOperator(
#     task_id='run_python_script_2',
#     bash_command='python3 /path/to/your/python_script2.py',
#     dag=dag,
# )

# t3 = BashOperator(
#     task_id='run_python_script_3',
#     bash_command='python3 /path/to/your/python_script3.py',
#     dag=dag,
# )

t1 # Task 실행 순서 설정
