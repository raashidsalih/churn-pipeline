DROP TABLE IF EXISTS churn.customers;
create table churn.customers (
    id uuid not null primary key,
    country varchar(50),
    state varchar(50),
    city varchar(50),
    zip_code int,
    lat_long varchar(30),
    latitude float,
    longitude float,
    gender varchar(10),
    senior_citizen varchar(10),
    partner varchar(10),
    dependents varchar(10),
    tenure_months int,
    phone_service varchar(20),
    multiple_lines varchar(20),
    internet_service varchar(20),
    online_security varchar(20),
    online_backup varchar(20),
    device_protection varchar(20),
    tech_support varchar(20),
    streaming_tv varchar(20),
    streaming_movies varchar(20),
    contract varchar(20),
    paperless_billing varchar(20),
    payment_method varchar(30),
    monthly_charges float,
    total_charges float,
    actual_churn_label varchar(5),
    insert_datetime timestamp not null default current_timestamp
);


DROP TABLE IF EXISTS churn.synthesized;
CREATE TABLE churn.synthesized (
    id UUID NOT NULL PRIMARY KEY,
    model_version VARCHAR(20),
    synthesis_datetime TIMESTAMP,
    insert_datetime TIMESTAMP not null default CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS churn.classified;
CREATE TABLE churn.classified (
    id UUID NOT NULL PRIMARY KEY,
    model_version VARCHAR(20),
    predicted_churn_label VARCHAR(5),
    confidence FLOAT,
    inference_datetime TIMESTAMP,
    insert_datetime TIMESTAMP not null default CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS churn.models;
CREATE TABLE churn.models (
    model_version VARCHAR(20),
    accuracy FLOAT,
    f1_score FLOAT,
    log_loss FLOAT,
    precision FLOAT,
    recall FLOAT,
    roc_auc FLOAT,
    metrics_type VARCHAR(50),
    insert_datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (model_version, metrics_type, insert_datetime)
);