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

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import Response
from starlette.responses import RedirectResponse
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
if __name__ == '__main__':
     app_run(app,host='localhost',port=8000)

