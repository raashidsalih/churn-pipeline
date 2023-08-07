-- insert into synthesized table
{% set data = ti.xcom_pull(key="syn_data", task_ids="extract_synthetic") %}
{% set uuid = ti.xcom_pull(key="ulid", task_ids="gen_ulid") %}

INSERT INTO churn.synthesized
VALUES
('{{uuid}}', '{{ data["model_version"]}}', '{{ data["date"] }}');
