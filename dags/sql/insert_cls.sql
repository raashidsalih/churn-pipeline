-- insert into classified table
{% set data = ti.xcom_pull(key="inference", task_ids="get_inference") %}
{% set uuid = ti.xcom_pull(key="ulid", task_ids="gen_ulid") %}

INSERT INTO churn.classified
VALUES
('{{uuid}}', '{{ data["model_version"]}}', '{{ data["label"]}}', {{ data["confidence"]}}, '{{ data["date"] }}');