DROP TABLE IF EXISTS churn.customers;
CREATE TABLE churn.customers (
    id UUID NOT NULL PRIMARY KEY,
    Country VARCHAR(50),
    State VARCHAR(50),
    City VARCHAR(50),
    Zip_Code INT,
    Lat_Long VARCHAR(30),
    Latitude FLOAT,
    Longitude FLOAT,
    Gender VARCHAR(10),
    Senior_Citizen VARCHAR(10),
    Partner VARCHAR(10),
    Dependents VARCHAR(10),
    Tenure_Months INT,
    Phone_Service VARCHAR(20),
    Multiple_Lines VARCHAR(20),
    Internet_Service VARCHAR(20),
    Online_Security VARCHAR(20),
    Online_Backup VARCHAR(20),
    Device_Protection VARCHAR(20),
    Tech_Support VARCHAR(20),
    Streaming_TV VARCHAR(20),
    Streaming_Movies VARCHAR(20),
    Contract VARCHAR(20),
    Paperless_Billing VARCHAR(20),
    Payment_Method VARCHAR(30),
    Monthly_Charges FLOAT,
    Total_Charges FLOAT,
    insert_datetime TIMESTAMP not null default CURRENT_TIMESTAMP );

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
    churn_label VARCHAR(5),
    confidence FLOAT,
    inference_datetime TIMESTAMP,
    insert_datetime TIMESTAMP not null default CURRENT_TIMESTAMP
);