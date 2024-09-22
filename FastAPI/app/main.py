# ruff: noqa: F401

from fastapi import FastAPI
from fastapi import Response
from pydantic import BaseModel
import json
import pandas as pd
from app.model.synthesize import synthesize
from app.model.synthesize import __version__ as syn_model_version
from app.model.classify import classify
from app.model.classify import __version__ as cls_model_version
from datetime import datetime
import uvicorn

app = FastAPI()


class cls_DataModel(BaseModel):
    CustomerID: str
    Country: str
    State: str
    City: str
    Zip_Code: int
    Lat_Long: str
    Latitude: float
    Longitude: float
    Gender: str
    Senior_Citizen: str
    Partner: str
    Dependents: str
    Tenure_Months: int
    Phone_Service: str
    Multiple_Lines: str
    Internet_Service: str
    Online_Security: str
    Online_Backup: str
    Device_Protection: str
    Tech_Support: str
    Streaming_TV: str
    Streaming_Movies: str
    Contract: str
    Paperless_Billing: str
    Payment_Method: str
    Monthly_Charges: float
    Total_Charges: float
    Actual_Churn_Label: str
    model_version: str
    date: datetime

class syn_DataModel(BaseModel):
    CustomerID: str
    Country: str
    State: str
    City: str
    Zip_Code: int
    Lat_Long: str
    Latitude: float
    Longitude: float
    Gender: str
    Senior_Citizen: str
    Partner: str
    Dependents: str
    Tenure_Months: int
    Phone_Service: str
    Multiple_Lines: str
    Internet_Service: str
    Online_Security: str
    Online_Backup: str
    Device_Protection: str
    Tech_Support: str
    Streaming_TV: str
    Streaming_Movies: str
    Contract: str
    Paperless_Billing: str
    Payment_Method: str
    Monthly_Charges: float
    Total_Charges: float
    Actual_Churn_Label: str
    model_version: str
    date: datetime


class ResponseModel(BaseModel):
    predicted_churn_label: str
    confidence: float
    model_version: str
    date: datetime


@app.get("/")
def home():
    return {
        "health_check": "OK",
        "syn_model_version": syn_model_version,
        "cls_model_version": cls_model_version,
    }


@app.get("/synthesize", response_model=syn_DataModel)
def synthesize_record():
    df = synthesize()
    df["model_version"] = syn_model_version
    df["date"] = datetime.now()
    return Response(
        df.to_json(orient="records", date_format="iso")[1:-1],
        media_type="application/json",
    )


@app.post("/predict", response_model=ResponseModel)
def predict(payload: cls_DataModel):
    parsed = json.loads(payload.json())
    result = classify([parsed])

    label = result[0]
    values = {"No": 0, "Yes": 1}
    label_val = values[label]
    confidence = result[1][label_val]

    return {
        "predicted_churn_label": label,
        "confidence": confidence,
        "model_version": cls_model_version,
        "date": datetime.now(),
    }


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000)
