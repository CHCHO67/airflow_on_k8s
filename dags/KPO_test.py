from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

# Define default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 4, 11),
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
}

# Define the DAG
dag = DAG(
    "k8s_pod_operator_example",
    default_args=default_args,
    schedule_interval=None,
)

# Define the Kubernetes Pod Operator
kubernetes_pod_operator = KubernetesPodOperator(
    task_id="run_pod",
    name="c2h_pod",
    namespace="airflow-clsuter",
    image="my_image:latest",
    # cmds=["python", "my_script.py"],
    # arguments=['arg1', 'arg2'],
    # volumes=[],
    # volume_mounts=[],
    labels={"app": "my_app"},
    startup_timeout_seconds=120,
    dag=dag,
)

# Define the start and end tasks
start_task = DummyOperator(task_id="start_task", dag=dag)
end_task = DummyOperator(task_id="end_task", dag=dag)

# Define the task dependencies
start_task >> kubernetes_pod_operator >> end_task
