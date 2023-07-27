from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
import time

from kubernetes.client import models as k8s

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
    read_only=False,
)

# Define resources
# Resource 제한을 하면 에러 발생. 리소스는 차후 해결.
# resources = k8s.V1ResourceRequirements(
#     requests={"cpu": "1", "memory": "1Gi", "nvidia.com/gpu": "1"},
#     limits={"cpu": "1", "memory": "2Gi", "nvidia.com/gpu": "1"},
# )

# Define default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 6, 27),
}

# Define the DAG
dag = DAG(
    "yolov5_ml_pipeline",
    description="yolo DAG",
    schedule_interval="0 12 * * *",
    default_args=default_args,
    catchup=False,
)


def sleep_on_failure(context):
    print("Task failed. sleeping for 2minutes")
    time.sleep(120)


# Define the tasks
start_task = DummyOperator(task_id="start_task", dag=dag)

# # Generate the training images
# generate_train_images_task = KubernetesPodOperator(
#     task_id="generate_train_images",
#     name="generate-train-images",
#     namespace="default",
#     image="ultralytics/yolov5:v5.0",
#     cmds=["python", "generate.py"],
#     arguments=[
#         "--source",
#         "/data/input/train",
#         "--output",
#         "/data/output/train",
#         "--size",
#         "640",
#     ],
#     volumes=[volume],
#     volume_mounts=[input_mount],
#     container_resources=resources,
#     labels={"app": "my_app"},
#     startup_timeout_seconds=120,
#     dag=dag,
# )

detect_images_task = KubernetesPodOperator(
    task_id="detect_images",
    name="detect-images",
    namespace="airflow-cluster",
    image="ultralytics/yolov5:latest",
    cmds=["python", "detect.py"],
    arguments=[
        "--weights",
        "yolov5s.pt",  # 여기서는 미리 학습된 yolov5s 모델을 사용
        "--source",
        "/data/input/",
        "--project",
        "/data/output/",
    ],
    volumes=[volume],
    volume_mounts=[mount],
    labels={"app": "my_app"},
    startup_timeout_seconds=120,
    in_cluster=True,
    is_delete_operator_pod=True,
    get_logs=True,
    image_pull_secrets="c2hcred",
    # container_resources=resources,
    on_failure_callback=sleep_on_failure,
    dag=dag,
)


# # Validate the model
# validate_model_task = KubernetesPodOperator(
#     task_id="validate_model",
#     name="validate-model",
#     namespace="default",
#     image="ultralytics/yolov5:v5.0",
#     cmds=["python", "val.py"],
#     arguments=[
#         "--data",
#         "/data/output/train",
#         "--weights",
#         "/path/to/your/weights.pt",  # 이 값을 모델의 가중치 파일 경로로 변경해야 합니다.
#         "--save-txt",
#         "--save-conf",
#         "--img",
#         "640",
#     ],
#     volumes=[volume],
#     volume_mounts=[output_mount],
#     container_resources=resources,
#     labels={"app": "my_app"},
#     startup_timeout_seconds=120,
#     dag=dag,
# )


# End the pipeline
end_task = DummyOperator(task_id="end_task", dag=dag)

# Define the task dependencies
start_task >> detect_images_task >> end_task
