# ruff: noqa: F401

import mlflow
import mlflow.sklearn
from mlflow import MlflowClient
import pickle
import sys
import pandas as pd
from sqlalchemy.exc import IntegrityError
from mlflow.exceptions import MlflowException
from sklearn.preprocessing import LabelEncoder
import os

# Credentials to connect to the Postgres database
# conn_str = "postgresql://pguser:pgpassword@pg:5432/pgdb"

# Access environment variables
user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
db = os.environ.get('POSTGRES_DB')
artifact_uri = os.environ.get('MLFLOW_S3_ENDPOINT_URL')

# # Construct the connection string
# conn_str = f"postgresql://{user}:{password}@pg:5432/{db}"

mlflow.set_tracking_uri("http://airflow-webserver:5000")

client = MlflowClient()

# Load the model from MLflow registry
model_name = "ChurnPredictionModel"
model_alias = "Champion"
__version__ = "0.0"

def classify(data):

    while True:
        try:
            model = mlflow.sklearn.load_model(f"models:/{model_name}@{model_alias}")
            model_info = client.get_model_version_by_alias(model_name, model_alias)
            __version__ = str(float(model_info.version))
            print("Model loaded successfully.")
            break
        except MlflowException as e:
            print(f"Failed to load model: {e}")
            return [0,0]
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return [0,0]

    df_raw = pd.DataFrame.from_dict(data)
    df = df_raw[
        [
            "Country",
            "State",
            "City",
            "Zip_Code",
            "Lat_Long",
            "Latitude",
            "Longitude",
            "Gender",
            "Senior_Citizen",
            "Partner",
            "Dependents",
            "Tenure_Months",
            "Phone_Service",
            "Multiple_Lines",
            "Internet_Service",
            "Online_Security",
            "Online_Backup",
            "Device_Protection",
            "Tech_Support",
            "Streaming_TV",
            "Streaming_Movies",
            "Contract",
            "Paperless_Billing",
            "Payment_Method",
            "Monthly_Charges",
            "Total_Charges",
        ]
    ]
    df.columns = df.columns.str.lower()
    df = df[model.feature_names_in_]

    label_encoder = LabelEncoder()
    for column in df.select_dtypes(include=['object']).columns:
        df[column] = label_encoder.fit_transform(df[column])

    pred = model.predict(df)
    prob = model.predict_proba(df)
    return [pred[0], prob[0].tolist()]


# if __name__ == "__main__":
#     print(classify(data))
