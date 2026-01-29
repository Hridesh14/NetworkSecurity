import os 
import pandas as pd
import numpy as np


'''Defining comman constant variable for traning pipeline'''
TARGET_COLUMN_NAME :str= 'Result'
PIPELINE_NAME : str='NetworkData'
ARTIFACTS_NAME :str= 'Artifacts'
FILE_NAME :str = 'phisingData.csv'

TRAIN_FILE_NAME : str = 'train.csv'
TEST_FILE_NAME : str ='test.csv'

SCHEMA_FILE_PATH  = os.path.join('Data_schema','Schema.yaml')   

SAVED_MODEL_DIR =os.path.join("saved_models")
MODEL_FILE_NAME : str = 'model.pkl'


'''
Data integretion related config strart with data integratir var name
'''
DATA_INTEGRATION_COLLECTION_NAME : str = 'NetworkData'
DATA_INTEGRATION_DB_NAME : str = 'HrideshNetworkAI'
DATA_INTEGRATION_DIR_NAME :str ='data_ingestion'
DATA_INTEGRATION_FEATURE_STORE_DIR :str ='feature_store'
DATA_INTEGRATION_INGESTED_DIR: str ='ingested'
DATA_INTEGRATION_TRAIN_TEST_SIZE: float=0.2

''' Data Validation related config starts with DATA_VALIDATION VAR NAME
'''
DATA_VALIDATION_DIR_NAME : str = 'data_validation'
DATA_VALIDATION_VALID_DIR : str ='validated'
DATA_VALIDATION_INVALID_DIR : str ='invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR : str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME :str = 'report.yaml'
PREPROCESSING_OBJ_FILE_NAME :str = 'preprocessing.pkl'


''' Data Transformation related constant start with DATA_TRANSFORMAATION VAR NAME
'''

DATA_TRANSFORMATRION_DIR_NAME : str = 'Data_transformation'
DATA_TRANSFORMATION_DATA_DIR : str = 'transformed'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR : str = 'Transformed_object'


DATA_TRANSFORMATION_IMPUTER_PARAMS : dict ={
    'missing_values':np.nan,
    'n_neighbors':3,
    'weights':'uniform'
}

DATA_TRANSFORMATION_TRAIN_FILE_PATH : str = 'train.npy'
DATA_TRANSFORMATION_TEST_FILE_PATH : str = 'test.npy'
'''
Model Trainer related constant start with MODE TRAINER VAR NAME
'''

MODEL_TRANNIG_NAME_DIR : str = 'model_trainer'
MODEL_TRANNING_TRAINED_MODEL_DIR : str ='trained_model'
MODEL_TRAINER_TRAINED_MODEL_NAME : str = 'model.pkl'
MODEL_TRAINER_EXPECTED_SCORE : float = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD : float =0.05
