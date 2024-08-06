# ruff: noqa: F401

# Import the required modules
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.models.baseoperator import chain

from random import randint
from datetime import datetime
import requests
import json
from ulid import ULID


# Define a function to obtain synthetic data from the fastapi service on another container
def _extract(ti):
    # Set the url of the fastapi service
    url = "http://fastapi:80/synthesize"
    # Send a get request to the url and get the data
    response = requests.get(url)
    # Parse the response in json format
    data = response.json()
    # Push the data to xcom with key "syn_data"
    ti.xcom_push(key="syn_data", value=data)


# Define a function to classify the synthetic data using the fastapi service on another container
def _classify(ti):
    # Set the url of the fastapi service
    url = "http://fastapi:80/predict"
    # Pull the data from xcom with key "syn_data" and task id "extract_synthetic"
    data = ti.xcom_pull(key="syn_data", task_ids="extract_synthetic")
    # Send a post request to the url with the data as json payload and get model prediction
    response = requests.post(url, json=data)
    # Parse the response as json data
    data = response.json()
    # Push the data to xcom with key "inference"
    ti.xcom_push(key="inference", value=data)


# Define a function to generate a ULID for use as primary key
def _gen_ulid(ti):
    # Generate a ULID object and convert it to UUID format
    ulid = str(ULID().to_uuid())
    # Push the ulid to xcom with key "ulid"
    ti.xcom_push(key="ulid", value=ulid)


# Create a DAG object that started at a previous date and runs hourly (cron format)
with DAG(
    "extract_load",
    start_date=datetime(2023, 7, 23),
    schedule_interval="0 * * * *",
    catchup=False,
) as dag:
    # Create a PythonOperator task to extract synthetic data
    extract_synthetic = PythonOperator(
        task_id="extract_synthetic", python_callable=_extract
    )

    # Create a PythonOperator task to generate a ULID
    gen_ulid = PythonOperator(task_id="gen_ulid", python_callable=_gen_ulid)

    # Create a PythonOperator task to classify the synthetic data
    get_inference = PythonOperator(task_id="get_inference", python_callable=_classify)

    # Create a PostgresOperator task to insert customers data into a postgres database
    insert_customers = PostgresOperator(
        task_id="insert_customers",
        postgres_conn_id="pg_conn",
        sql="sql/insert_customers.sql",
    )

    # Create a PostgresOperator task to insert synthetic data into a postgres database
    insert_syn = PostgresOperator(
        task_id="insert_syn", postgres_conn_id="pg_conn", sql="sql/insert_syn.sql"
    )

    # Create a PostgresOperator task to insert inference data into a postgres database
    insert_cls = PostgresOperator(
        task_id="insert_cls", postgres_conn_id="pg_conn", sql="sql/insert_cls.sql"
    )

    # Use the chain function to define the dependencies between the tasks in the DAG
    chain(
        [extract_synthetic, gen_ulid],
        insert_customers,
        [get_inference, insert_syn],
        insert_cls,
    )
