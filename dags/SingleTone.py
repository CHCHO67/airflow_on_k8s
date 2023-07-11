from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from kubernetes.client.models import (
    V1ResourceRequirements,
    V1Volume,
    V1VolumeMount,
    V1PersistentVolumeClaimVolumeSource,
)

# Define default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 6, 8),
    "retries": 0,
    # "retry_delay": timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    "yolov5_inference_pipeline",
    default_args=default_args,
    schedule_interval=timedelta(days=1),
)

# Define resources
resources = V1ResourceRequirements(
    requests={"cpu": "12", "memory": "2Gi"}, limits={"cpu": "12", "memory": "2Gi"}
)

# Define volume and volume mount
volume = V1Volume(
    name="data-volume",
    persistent_volume_claim=V1PersistentVolumeClaimVolumeSource(
        claim_name="data-pvc",
    ),
)

volume_mount = V1VolumeMount(
    name="data-volume",
    mount_path="/data",
)

# Define the tasks
start_task = DummyOperator(task_id="start_task", dag=dag)

# Perform YOLOv5 inference
yolov5_inference_task = KubernetesPodOperator(
    task_id="yolov5_inference",
    name="yolov5-inference",
    namespace="default",
    image="ultralytics/yolov5:v5.0",
    cmds=["python", "detect.py"],
    arguments=["--source", "/data/input", "--weights", "yolov5s.pt", "--conf", "0.4"],
    volumes=[volume],
    volume_mounts=[volume_mount],
    container_resources=resources,
    labels={"app": "my_app"},
    startup_timeout_seconds=120,
    dag=dag,
)

# End the pipeline
end_task = DummyOperator(task_id="end_task", dag=dag)

# Define the task dependencies
start_task >> yolov5_inference_task >> end_task
