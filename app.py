import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

mongo_db_url = os.getenv('MONGO_DB_URL')


import pymongo

from Networksecurity.Exception.Exception import NetworkSecurityException
from Networksecurity.logging.logger import logging
from Networksecurity.pipeline.Tranning_pipeline import TranningPipeline
from fastapi.templating import Jinja2Templates

# Initialize the templates object
# Ensure you have a folder named 'templates' in your project directory
templates = Jinja2Templates(directory="templates")
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,UploadFile,Request,File
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import Response
from starlette.responses import RedirectResponse
from Networksecurity.utils.ml_utils.model.estimater import NetworkModel
import pandas as pd


from Networksecurity.utils.Main_utils.utils import load_object

client = pymongo.MongoClient(mongo_db_url,tlsCAFile=ca,tlsAllowInvalidCertificates=True, 
                serverSelectionTimeoutMS=5000)

from Networksecurity.constant.traning_pipeline import DATA_INTEGRATION_COLLECTION_NAME,DATA_INTEGRATION_DB_NAME
database = client[DATA_INTEGRATION_DB_NAME]
collection = database[DATA_INTEGRATION_COLLECTION_NAME]

app = FastAPI()
origin = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins = origin,
    allow_credentials = True,
    allow_methods =['*'],
    allow_headers =['*'],
)


@app.get('/',tags=['authentication'])
async def index():
    return RedirectResponse(url='/docs')

@app.get('/train')
async def train_route():
    try:
        train_Pipeline = TranningPipeline()
        train_Pipeline.run_pipeline()
        return Response('Tranning is successful')
    except Exception as e:
            raise NetworkSecurityException(e, sys) 
@app.post('/Predict')
async def predict_route(request:Request,file:UploadFile=File(...)):
     try:
        df = pd.read_csv(file.file)

        preprocessor = load_object('final_model/preprocessor.pkl')
        final_model  = load_object('final_model/model.pkl')

        network_model =NetworkModel(preprocessor=preprocessor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse('Table.html',{'request':request,'table':table_html})
     except Exception as e:
            raise NetworkSecurityException(e, sys) 
     


if __name__ == '__main__':
     app_run(app,host='localhost',port=8000)

