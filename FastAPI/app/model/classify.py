# ruff: noqa: F401

import pickle
import pandas as pd
from pathlib import Path
from flaml import AutoML

__version__ = "1.0.0"

BASE_DIR = Path(__file__).resolve(strict=True).parent

with open(f"{BASE_DIR}/cls_model_1.0.0.pkl", "rb") as f:
    automl = pickle.load(f)

def classify(data):
    df_raw = pd.DataFrame.from_dict(data)
    df = df_raw[['Country', 'State', 'City', 'Zip_Code', 'Lat_Long', 'Latitude',
       'Longitude', 'Gender', 'Senior_Citizen', 'Partner', 'Dependents',
       'Tenure_Months', 'Phone_Service', 'Multiple_Lines', 'Internet_Service',
       'Online_Security', 'Online_Backup', 'Device_Protection', 'Tech_Support',
       'Streaming_TV', 'Streaming_Movies', 'Contract', 'Paperless_Billing',
       'Payment_Method', 'Monthly_Charges', 'Total_Charges']]
    pred = automl.predict(df)
    prob = automl.predict_proba(df)
    return [pred[0], prob[0].tolist()]

# if __name__ == "__main__":
#     print(classify(data))
