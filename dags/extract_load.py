from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.models.baseoperator import chain

from random import randint
from datetime import datetime
import requests
import json
from ulid import ULID

def _extract(ti):
    url = "http://fastapi:80/synthesize"
    response = requests.get(url)
    data = response.json()
    ti.xcom_push(key="syn_data", value=data)

def _classify(ti):
    url = "http://fastapi:80/predict"
    data = ti.xcom_pull(key="syn_data", task_ids="extract_synthetic")
    response = requests.post(url, json=data)
    data = response.json()
    ti.xcom_push(key="inference", value=data)

def _gen_ulid(ti):
    ti.xcom_push(key="ulid", value=str(ULID().to_uuid()))


with DAG("extract_load", start_date=datetime(2023, 7, 23),
    schedule_interval="*/1 * * * *", catchup=False) as dag:

        extract_synthetic = PythonOperator(
            task_id="extract_synthetic",
            python_callable=_extract
        )

        gen_ulid = PythonOperator(
            task_id="gen_ulid",
            python_callable=_gen_ulid
        )

        get_inference = PythonOperator(
            task_id="get_inference",
            python_callable=_classify
        )

        insert_customers = PostgresOperator(
            task_id="insert_customers",
            postgres_conn_id="pg_conn",
            sql="sql/insert_customers.sql"
        )

        insert_syn = PostgresOperator(
            task_id="insert_syn",
            postgres_conn_id="pg_conn",
            sql="sql/insert_syn.sql"
        )

        insert_cls = PostgresOperator(
            task_id="insert_cls",
            postgres_conn_id="pg_conn",
            sql="sql/insert_cls.sql"
        )

        chain([extract_synthetic, gen_ulid], insert_customers, [get_inference, insert_syn], insert_cls)
