import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')
cwd = os.path.join(AIRFLOW_HOME, 'dbt_project')

with DAG(dag_id='dbt_transform', schedule_interval="0 */6 * * *", start_date=datetime(2023, 8, 4), catchup=False) as dag:
    
    dbt_build = BashOperator(
        task_id = 'dbt_build',
        bash_command = 'dbt build',
        cwd = cwd,
        env = os.environ.copy(),
        dag = dag
        )
