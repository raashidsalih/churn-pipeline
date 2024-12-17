import mlflow
from mlflow.tracking import MlflowClient
import psycopg2
import os
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)


def main():
    # Access environment variables
    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")
    db = os.environ.get("POSTGRES_DB")

    # Construct the connection string
    conn_str = f"postgresql://{user}:{password}@pg:5432/{db}"

    # Initialize mlflow and connect to the same Postgres database
    mlflow.set_tracking_uri("http://airflow-webserver:5000")

    # mlflow model credentials
    model_name = "ChurnPredictionModel"
    model_alias = "Champion"

    # Get the model version using MlflowClient
    client = MlflowClient()
    model_info = client.get_model_version_by_alias(model_name, model_alias)
    model_version = str(float(model_info.version))

    # Connect to the Postgres database
    conn = psycopg2.connect(conn_str)
    cursor = conn.cursor()

    # Join tables churn.customers and churn.classified on column id and filter by model version
    query = f"""
        SELECT c.actual_churn_label, cl.predicted_churn_label, cl.confidence
        FROM churn.customers c
        JOIN churn.classified cl ON c.id = cl.id
        WHERE cl.model_version = '{model_version}'
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Separate actual labels, predicted labels, and predicted probabilities
    actual_labels = [1 if row[0] == "Yes" else 0 for row in results]
    predicted_labels = [1 if row[1] == "Yes" else 0 for row in results]
    predicted_probs = [row[2] for row in results]

    # Check if the arrays are not empty before calculating metrics
    if actual_labels and predicted_labels and predicted_probs:
        # Calculate model metrics
        accuracy = accuracy_score(actual_labels, predicted_labels)
        f1 = f1_score(actual_labels, predicted_labels)
        logloss = log_loss(actual_labels, predicted_probs)
        precision = precision_score(actual_labels, predicted_labels)
        recall = recall_score(actual_labels, predicted_labels)
        roc_auc = roc_auc_score(actual_labels, predicted_probs)

        # Write metrics to table churn.models with metrics_type 'scheduled'
        insert_query = """
            INSERT INTO churn.models (model_version, accuracy, f1_score, log_loss, precision, recall, roc_auc, metrics_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            insert_query,
            (
                model_version,
                accuracy,
                f1,
                logloss,
                precision,
                recall,
                roc_auc,
                "scheduled",
            ),
        )

        # Commit the transaction
        conn.commit()
        print("Model metrics calculated and written to churn.models table.")
    else:
        print(f"No data available for the specified model version {model_version}.")

    # Close the connection
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
