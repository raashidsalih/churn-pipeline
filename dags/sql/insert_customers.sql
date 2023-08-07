-- insert into customers table
{% set data = ti.xcom_pull(key="syn_data", task_ids="extract_synthetic") %}
{% set uuid = ti.xcom_pull(key="ulid", task_ids="gen_ulid") %}

INSERT INTO churn.customers
VALUES
('{{uuid}}', 
'{{ data["Country"]}}',
'{{ data["State"]}}',
'{{ data["City"]}}',
{{ data["Zip_Code"]}},
'{{ data["Lat_Long"] }}',
{{ data["Latitude"]}},
{{ data["Longitude"]}},
'{{ data["Gender"] }}',
'{{ data["Senior_Citizen"] }}',
'{{ data["Partner"] }}',
'{{ data["Dependents"] }}',
{{ data["Tenure_Months"]}},
'{{ data["Phone_Service"] }}',
'{{ data["Multiple_Lines"] }}',
'{{ data["Internet_Service"] }}',
'{{ data["Online_Security"] }}',
'{{ data["Online_Backup"] }}',
'{{ data["Device_Protection"] }}',
'{{ data["Tech_Support"] }}',
'{{ data["Streaming_TV"] }}',
'{{ data["Streaming_Movies"] }}',
'{{ data["Contract"] }}',
'{{ data["Paperless_Billing"] }}',
'{{ data["Payment_Method"] }}',
{{ data["Monthly_Charges"]}},
{{ data["Total_Charges"]}}
);