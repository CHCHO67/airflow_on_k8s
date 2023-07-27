from airflow.models import XCom

def push_function(**kwargs):
    value = "Value to be passed to the other task"
    XCom.push(key='my_key', value=value, context=kwargs)

def pull_function(**kwargs):
    value = XCom.pull(key='my_key', context=kwargs)
    print(f"Received value: {value}")
