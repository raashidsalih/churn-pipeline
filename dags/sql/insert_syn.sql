-- Insert into synthesized table
-- Use Jinja templating to get the synthetic model metadata and uuid from xcom
{% set data = ti.xcom_pull(key="syn_data", task_ids="extract_synthetic") %}
{% set uuid = ti.xcom_pull(key="ulid", task_ids="gen_ulid") %}

-- Use the data and uuid to insert a new row into the churn.synthesized table
INSERT INTO churn.synthesized
VALUES
('{{uuid}}',
'{{ data["model_version"]}}',
'{{ data["date"] }}');