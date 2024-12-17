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

# DAG object that started at a previous date and runs every six hours (cron format)
with DAG(
    dag_id="dbt_transform",
    schedule_interval="0 */6 * * *",
    start_date=datetime(2024, 9, 19),
    max_active_runs=1,
    catchup=False,
) as dag:
    # BashOperator task to run the dbt build command
    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="dbt build --profiles-dir ../.dbt",
        # change working directory from path defined above
        cwd=cwd,
        env=os.environ.copy(),
        dag=dag,
    )

    # BashOperator task to run the dbt docs generate command
    dbt_docs_generate = BashOperator(
        task_id="dbt_docs_generate",
        bash_command="dbt docs generate --profiles-dir ../.dbt",
        # change working directory from path defined above
        cwd=cwd,
        env=os.environ.copy(),
        dag=dag,
    )

    # BashOperator task to run the dbt docs serve command
    dbt_docs_serve = BashOperator(
        task_id="dbt_docs_serve",
        bash_command='nohup dbt docs serve --port 8001 --host "0.0.0.0" --profiles-dir ../.dbt --no-browser > dbt_docs_serve.log 2>&1 &',
        # change working directory from path defined above
        cwd=cwd,
        env=os.environ.copy(),
        dag=dag,
    )

    # Set task dependencies
    dbt_build >> dbt_docs_generate >> dbt_docs_serve
