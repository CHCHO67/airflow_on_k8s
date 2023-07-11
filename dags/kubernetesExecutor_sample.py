from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from datetime import datetime
import time
import requests

from kubernetes.client import models as k8s


# Define your volume
volume = k8s.V1Volume(
    name="data-volume",
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(
        claim_name="data-pvc"
    ),
)

volume_mount = k8s.V1VolumeMount(
    name="data-volume",  # the same name you specified in the volume
    mount_path="/data",  # the path where you want the PVC to be mounted
    sub_path=None,
    read_only=False,
)

# Define your resources
resources = k8s.V1ResourceRequirements(
    requests={"cpu": "1", "memory": "1Gi"},
    limits={"cpu": "2", "memory": "2Gi"},
)


default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 6, 1),
}

dag = DAG(
    "text_hello",
    description="Simple tutorial DAG",
    schedule_interval="0 12 * * *",
    default_args=default_args,
    catchup=False,
)

start_operator = DummyOperator(task_id="start_task", dag=dag)

hello_operator = KubernetesPodOperator(
    task_id="hello_task",
    namespace="airflow-cluster",
    image="sail0603/airflow-task:text_hello",
    # cmds=["python", "-c"],
    # arguments=[
    #     print("test success")
    #     """
    #     print("Run this command!!!")
    #     # import time
    #     # from datetime import datetime
    #     # now = datetime.now()  # current date and time
    #     # with open("/data/hello_world.txt", "w") as f:
    #     #     f.write(f"Hello World, Current Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    #     # time.sleep(120)  # Sleep for 60 seconds
    #     """
    # ],
    name="text-hello-pod",
    in_cluster=True,
    is_delete_operator_pod=True,
    get_logs=True,
    image_pull_secrets="c2hcred",
    volumes=[volume],  # use the volume
    volume_mounts=[volume_mount],  # mount the volume
    container_resources=resources,  # set the resources
    dag=dag,
)

end_operator = DummyOperator(task_id="end_task", dag=dag)

start_operator >> hello_operator >> end_operator
