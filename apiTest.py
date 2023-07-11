import requests

# Airflow의 webserver 주소를 지정하세요.
airflow_webserver_url = "http://localhost:8080"

# Airflow 2.0 이상에서는 기본적으로 API에 대한 인증이 필요합니다.
# 인증 토큰이나 사용자 이름과 비밀번호를 사용하여 인증할 수 있습니다.
# 아래 코드에서는 사용자 이름과 비밀번호를 사용하였습니다.
auth_info = ("admin", "admin")

# DAG의 ID를 지정하세요.
dag_id = "my_dag"

# Airflow의 REST API를 호출하여 DAG 정보를 조회합니다.
response = requests.get(
    f"{airflow_webserver_url}/api/v1/dags/yolov5_ml_pipeline",
    auth=auth_info,
)

# 조회한 DAG 정보를 출력합니다.
print(response.json())
