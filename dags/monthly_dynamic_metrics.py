from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
from pathlib import Path
from dynamic_metrics import main

# Add the dynamic_metrics folder to the Python path
dag_folder = Path(__file__).resolve().parent
dynamic_metrics_folder = dag_folder / "dynamic_metrics"
sys.path.append(str(dynamic_metrics_folder))

# Define the default_args dictionary
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    "monthly_dynamic_metrics",
    default_args=default_args,
    description="A DAG to run dynamic metrics calculation monthly",
    schedule_interval="0 0 1 * *",  # Run at midnight on the first day of every month
    max_active_runs=1,
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

# Define the task
run_dynamic_metrics_task = PythonOperator(
    task_id="run_dynamic_metrics",
    python_callable=main,
    dag=dag,
)

# Set task dependencies (in this case, we only have one task)
run_dynamic_metrics_task

if __name__ == "__main__":
    dag.cli()
