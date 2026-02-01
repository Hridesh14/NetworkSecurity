import sys
import os
import certifi
import pandas as pd
import pymongo
import re
from urllib.parse import urlparse

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Request, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, FileResponse
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run

# Custom Imports (Aapke project structure ke hisab se)
from Networksecurity.Exception.Exception import NetworkSecurityException
from Networksecurity.logging.logger import logging
from Networksecurity.pipeline.Tranning_pipeline import TranningPipeline
from Networksecurity.utils.ml_utils.model.estimater import NetworkModel
from Networksecurity.utils.Main_utils.utils import load_object
from Networksecurity.constant.traning_pipeline import DATA_INTEGRATION_COLLECTION_NAME, DATA_INTEGRATION_DB_NAME

# --- Config ---
load_dotenv()
mongo_db_url = os.getenv('MONGO_DB_URL')
ca = certifi.where()

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=5000)
database = client[DATA_INTEGRATION_DB_NAME]
collection = database[DATA_INTEGRATION_COLLECTION_NAME]

app = FastAPI()
templates = Jinja2Templates(directory="templates")

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# This tells the browser: "It is okay to talk to this server."
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all connections
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/Predict")
async def predict_file_route(request: Request, file: UploadFile = File(...)):
    try:
        preprocessor = load_object('final_model/preprocessor.pkl')
        final_model = load_object('final_model/model.pkl')
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        df = pd.read_csv(file.file)
        
       
        if hasattr(preprocessor, 'feature_names_in_'):
            df = df[preprocessor.feature_names_in_]
        elif hasattr(final_model, 'feature_names_in_'):
             df = df[final_model.feature_names_in_]

        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_label'] = df['predicted_column'].replace({1: 'Phishing (Unsafe)', 0: 'Legitimate (Safe)'})

        table_html = df.to_html(classes='table table-striped table-bordered')
        return templates.TemplateResponse("Table.html", {"request": request, "table": table_html})

    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.get("/", tags=['authentication'])
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/train")
async def train_route():
    train_pipeline = TranningPipeline()
    train_pipeline.run_pipeline()
    return Response("Training is successful")

if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)