FROM apache/airflow:2.10.2-python3.10

COPY requirements.txt .

RUN pip install -r requirements.txt

USER root

RUN apt-get update && apt-get install -y libgomp1

USER airflow