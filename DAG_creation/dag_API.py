from flask import Flask, request
from jinja2 import Template

app = Flask(__name__)

@app.route('/create_dag', methods=['POST'])
def create_dag():
    data = request.get_json()  # Get the JSON data sent with the POST request
    template = Template(open('dag_template.j2').read())  # Load the Jinja2 template
    dag = template.render(data)  # Fill the template with the data
    print(data)
    # Write the filled template to a .py file in the Airflow DAGs directory
    with open(f'/mnt/shared/airflow/dags/{data["dag"]["dag_id"]}.py', 'w') as f:
        f.write(dag)
    
    return {'message': 'DAG created'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8088', debug=True)

# flask run --port=8080
# flask run --host=0.0.0.0 --port=8080
