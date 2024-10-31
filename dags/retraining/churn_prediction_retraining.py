from pathlib import Path
import pandas as pd
import psycopg2
import os
from sqlalchemy import create_engine
from flaml import AutoML
import mlflow
from mlflow.exceptions import MlflowException
from mlflow import MlflowClient
from mlflow.models import infer_signature, set_signature
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, log_loss, roc_auc_score

def main():
    BASE_DIR = Path(__file__).resolve(strict=True).parent

    # Access environment variables
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    db = os.environ.get('POSTGRES_DB')

    # Construct the connection string
    conn_str = f"postgresql://{user}:{password}@pg:5432/{db}"

    # Initialize mlflow and connect to the same Postgres database
    mlflow.set_tracking_uri("http://airflow-webserver:5000")
    experiment = mlflow.set_experiment("Customer Churn Prediction")

    # mlflow model credentials
    model_name = "ChurnPredictionModel"
    model_alias = "Champion"

    # flag if training first model
    model_exists = False

    try:
        model = mlflow.sklearn.load_model(f"models:/{model_name}@{model_alias}")
        model_exists = True
    except MlflowException as e:
        print(f"An error occurred: {e}")

    # if model exists, get retraining data. Else, use train_set to develop first model.
    if model_exists:
        engine = create_engine(conn_str)
        conn = psycopg2.connect(conn_str)
        query = """SELECT 
        loc.country AS Country,
        loc.state AS State,
        loc.city AS City,
        loc.zip_code AS Zip_Code,
        loc.lat_long AS Lat_Long,
        loc.latitude AS Latitude,
        loc.longitude AS Longitude,
        demo.gender AS Gender,
        demo.senior_citizen AS Senior_Citizen,
        demo.partner AS Partner,
        demo.dependents AS Dependents,
        serv.tenure_months AS Tenure_Months,
        serv.phone_service AS Phone_Service,
        serv.multiple_lines AS Multiple_Lines,
        serv.internet_service AS Internet_Service,
        serv.online_security AS Online_Security,
        serv.online_backup AS Online_Backup,
        serv.device_protection AS Device_Protection,
        serv.tech_support AS Tech_Support,
        serv.streaming_tv AS Streaming_TV,
        serv.streaming_movies AS Streaming_Movies,
        con.contract AS Contract,
        con.paperless_billing AS Paperless_Billing,
        con.payment_method AS Payment_Method,
        con.monthly_charges AS Monthly_Charges,
        con.total_charges AS Total_Charges,
        fct.actual_churn_label AS Churn_Label
        FROM 
            churn.dim_location loc
        JOIN 
            churn.dim_demographics demo ON loc.id = demo.id
        JOIN 
            churn.dim_services serv ON loc.id = serv.id
        JOIN 
            churn.dim_contract con ON loc.id = con.id
        JOIN 
            churn.fct_churn fct ON loc.id = fct.id;
        """
        df = pd.read_sql(query, conn)
        conn.close()
    else:
        df = pd.read_csv(f"{BASE_DIR}/train_set.csv", encoding="utf-8")

    # Preprocess training set and read test set
    features = df.drop(columns=['churn_label'])
    target = df['churn_label']

    test_set = pd.read_csv(f"{BASE_DIR}/test_set.csv", encoding="utf-8")
    test_features = test_set.drop(columns=['churn_label'])
    test_target = test_set['churn_label']

    automl = AutoML()
    client = MlflowClient()

    inferred_signature = infer_signature(features.head(), target.head())

    with mlflow.start_run() as run:
        mlflow.sklearn.autolog()
        automl.fit(features, target, task="classification", time_budget=60*1)
        
        # Log the model
        model_uri = f"runs:/{run.info.run_id}/model"
        set_signature(model_uri, inferred_signature)
        model = mlflow.register_model(model_uri, "ChurnPredictionModel")
        client.set_registered_model_alias("ChurnPredictionModel", "Champion", version=model.version)  

        # Make predictions on the test set
        test_predictions = automl.predict(test_features)
        test_probabilities = automl.predict_proba(test_features)[:, 1]  # Assuming binary classification
        
        # Calculate test metrics
        test_accuracy = accuracy_score(test_target, test_predictions)
        test_precision = precision_score(test_target, test_predictions, pos_label="Yes", zero_division=1)
        test_recall = recall_score(test_target, test_predictions, pos_label="Yes", zero_division=1)
        test_f1 = f1_score(test_target, test_predictions, pos_label="Yes")
        test_log_loss = log_loss(test_target, test_probabilities)
        test_roc_auc = roc_auc_score(test_target, test_probabilities)
        
        # Log test metrics
        mlflow.log_metric("test_accuracy_score", test_accuracy)
        mlflow.log_metric("test_f1_score", test_f1)
        mlflow.log_metric("test_log_loss", test_log_loss)
        mlflow.log_metric("test_precision_score", test_precision)
        mlflow.log_metric("test_recall_score", test_recall)
        mlflow.log_metric("test_roc_auc", test_roc_auc)
        mlflow.log_metric("test_score", test_accuracy)  # Assuming test_score is the same as test_accuracy

    if model_exists:
        print("Retraining complete!")
    else:
        print("First model successfully created!")

if __name__ == "__main__":
    main()