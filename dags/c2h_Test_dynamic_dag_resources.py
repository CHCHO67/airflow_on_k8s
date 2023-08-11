from datetime import datetime, timedelta
import time
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from kubernetes.client import models as k8s
from airflow.models import Variable
from kubernetes.client import V1ResourceRequirements

# Define volume
volume = k8s.V1Volume(
    name="data-volume",
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(
        claim_name="data-pvc"
    ),
)

mount = k8s.V1VolumeMount(
    name="data-volume",  # the same name you specified in the volume
    mount_path="/data",  # the path where you want the PVC to be mounted
    read_only="False",
)

default_args = {
    "owner": "c2h",
    "depends_on_past": False,
    "start_date": datetime(2023, 8, 1),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "Test_dynamic_dag_resources",
    default_args=default_args,
    schedule_interval="@daily",
)


def sleep_on_failure(context):
    print("Task failed. sleeping for 2minutes")
    time.sleep(120)


test_task_1 = KubernetesPodOperator(
    namespace="airflow-cluster",
    image="python:3.7",
    cmds=["python", "-c"],
    arguments=["print('hello')", "x=1+1", "print(x)"],
    name="task_1",
    task_id="task_1",
    env_vars={},
    container_resources={},
    in_cluster=True,
    is_delete_operator_pod=True,
    on_failure_callback=sleep_on_failure,
    do_xcom_push=True,
    dag=dag,
)


test_task_2 = KubernetesPodOperator(
    namespace="airflow-cluster",
    image="python:3.7",
    cmds=["python", "-c"],
    arguments=[
        "print('hello')",
        "x=1+1",
        "print(x)",
        "with open('/data/test_c2h.txt', 'w') as f: f.write(x)",
    ],
    name="task_2",
    task_id="task_2",
    env_vars={"ENV_VAR1": "value1", "ENV_VAR2": "value2"},
    container_resources={},
    in_cluster=True,
    is_delete_operator_pod=True,
    on_failure_callback=sleep_on_failure,
    do_xcom_push=True,
    dag=dag,
)

test_task_1 >> test_task_2


test_task_3 = KubernetesPodOperator(
    namespace="airflow-cluster",
    image="python:3.7",
    cmds=["python", "-c"],
    arguments=["print('hello')"],
    name="task_3",
    task_id="task_3",
    env_vars={"ENV_VAR1": "value1", "ENV_VAR2": "value2"},
    container_resources=V1ResourceRequirements(
        requests={"memory": "128Mi", "cpu": "100m"},
        limits={"memory": "1Gi", "cpu": "1"},
    ),
    in_cluster=True,
    is_delete_operator_pod=True,
    on_failure_callback=sleep_on_failure,
    do_xcom_push=True,
    dag=dag,
)

test_task_2 >> test_task_3
