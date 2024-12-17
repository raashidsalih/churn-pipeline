from pathlib import Path
import sys
import pandas as pd
import psycopg2
import os
from flaml import AutoML
import mlflow
from mlflow.exceptions import MlflowException
from mlflow import MlflowClient
from mlflow.models import infer_signature, set_signature
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    log_loss,
    roc_auc_score,
)


def main():
    BASE_DIR = Path(__file__).resolve(strict=True).parent

    # Credentials to connect to the Postgres database
    # conn_str = "postgresql://pguser:pgpassword@pg:5432/pgdb"

    # Access environment variables
    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")
    db = os.environ.get("POSTGRES_DB")

    # # Construct the connection string
    conn_str = f"postgresql://{user}:{password}@pg:5432/{db}"

    # Initialize mlflow and connect to the same Postgres database
    mlflow.set_tracking_uri("http://localhost:5000")

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

    # if model exists, exit. Else, use train_set to develop first model.
    if model_exists:
        sys.exit()

    df = pd.read_csv(f"{BASE_DIR}/train_set.csv", encoding="utf-8")

    # Preprocess training set and read test set
    features = df.drop(columns=["churn_label"])
    target = df["churn_label"]

    test_set = pd.read_csv(f"{BASE_DIR}/test_set.csv", encoding="utf-8")
    test_features = test_set.drop(columns=["churn_label"])
    test_target = test_set["churn_label"]

    automl = AutoML()
    client = MlflowClient()

    inferred_signature = infer_signature(features.head(), target.head())

    with mlflow.start_run() as run:
        mlflow.sklearn.autolog()
        automl.fit(features, target, task="classification", time_budget=60 * 2)
        # Log the model
        model_uri = f"runs:/{run.info.run_id}/model"
        set_signature(model_uri, inferred_signature)
        model = mlflow.register_model(model_uri, "ChurnPredictionModel")
        client.set_registered_model_alias(
            "ChurnPredictionModel", "Champion", version=model.version
        )

        # Make predictions on the test set
        test_predictions = automl.predict(test_features)
        test_probabilities = automl.predict_proba(test_features)[:, 1]
        # Calculate test metrics
        test_accuracy = accuracy_score(test_target, test_predictions)
        test_precision = precision_score(
            test_target, test_predictions, pos_label="Yes", zero_division=1
        )
        test_recall = recall_score(
            test_target, test_predictions, pos_label="Yes", zero_division=1
        )
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
        print("First model successfully created!")

        run_data_dict = client.get_run(run.info.run_id).data.to_dictionary()

        # Connect to the PostgreSQL database and insert metrics
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()

        # Insert training metrics
        cursor.execute(
            """
            INSERT INTO churn.models (model_version, accuracy, f1_score, log_loss, precision, recall, roc_auc, metrics_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                str(float(model.version)),
                run_data_dict["metrics"]["training_accuracy_score"],
                run_data_dict["metrics"]["training_f1_score"],
                run_data_dict["metrics"]["training_log_loss"],
                run_data_dict["metrics"]["training_precision_score"],
                run_data_dict["metrics"]["training_recall_score"],
                run_data_dict["metrics"]["training_roc_auc"],
                "training",
            ),
        )

        # Insert test metrics
        cursor.execute(
            """
            INSERT INTO churn.models (model_version, accuracy, f1_score, log_loss, precision, recall, roc_auc, metrics_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                str(float(model.version)),
                test_accuracy,
                test_f1,
                test_log_loss,
                test_precision,
                test_recall,
                test_roc_auc,
                "test",
            ),
        )

        conn.commit()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
