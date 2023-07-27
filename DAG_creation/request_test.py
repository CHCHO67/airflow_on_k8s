import requests
import json

# JSON 데이터를 로드
with open('dag_test.json', 'r') as f:
    data = json.load(f)
print(data)
# Flask 앱에 POST 요청
response = requests.post('http://0.0.0.0:8088/create_dag', json=data)
print(response.status_code)
print(response.text)

# Response 출력
print(response.json())
