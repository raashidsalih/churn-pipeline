# ruff: noqa: F401

# Import the required modules
import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# Get the value of the AIRFLOW_HOME environment variable
AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")
# Join the AIRFLOW_HOME path with the dbt_project subdirectory to get working directory
cwd = os.path.join(AIRFLOW_HOME, "dbt_project")

# Create a DAG object that started at a previous date and runs every six hours (cron format)
with DAG(
    dag_id="dbt_transform",
    schedule_interval="0 */6 * * *",
    start_date=datetime(2023, 8, 4),
    catchup=False,
) as dag:
    # Create a BashOperator task to run the dbt build command
    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="dbt build",
        # change working directory from path defined above
        cwd=cwd,
        env=os.environ.copy(),
        dag=dag,
    )
