-- Insert into classified table
-- Use Jinja templating to get model prediction data and uuid from xcom
{% set data = ti.xcom_pull(key="inference", task_ids="get_inference") %}
{% set uuid = ti.xcom_pull(key="ulid", task_ids="gen_ulid") %}

-- Use the data and uuid to insert a new row into the churn.classified table
INSERT INTO churn.classified
VALUES
('{{uuid}}', '{{ data["model_version"]}}', '{{ data["label"]}}', {{ data["confidence"]}}, '{{ data["date"] }}');
