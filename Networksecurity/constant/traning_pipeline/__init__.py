import os 
import pandas as pd
import numpy as np


'''Defining comman constant variable for traning pipeline'''
TARGET_COLUMN_NAME :str='Result'
PIPELINE_NAME : str='NetworkSecurity'
ARTIFACTS_NAME :str= 'Artifacts'
FILE_NAME :str = 'phisingData.csv'

TRAIN_FILE_NAME : str = 'train.csv'
TEST_FILE_NAME : str ='test.csv'


'''
Data integretion related config strart with data integratir vir name
'''
DATA_INTEGRATION_COLLECTION_NAME : str = 'NetworkSecurity'
DATA_INTEGRATION_DB_NAME : str = 'HrideshNetworkAI'
DATA_INTEGRATION_DIR_NAME :str ='data_ingestion'
DATA_INTEGRATION_FEATURE_STORE_DIR :str ='feature_store'
DATA_INTEGRATION_INGESTED_DIR: str ='ingested'
DATA_INTEGRATION_TRAIN_TEST_SPLIR: float=0.2

