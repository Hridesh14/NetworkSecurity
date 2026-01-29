from Networksecurity.Exception.Exception import NetworkSecurityException

from Networksecurity.logging.logger import logging



from Networksecurity.entity.config_entity import DataIngestionConfig

from Networksecurity.entity.artifacts_entity import DataIngestionArtifact



import os

import sys

import pandas as pd

import numpy as np

import pymongo

from typing import List

from sklearn.model_selection import train_test_split

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_LINK =os.getenv('MONGO_DB_URL')


MONGO_DB = os.getenv('MONGO_DB_URL')

class DataIngustion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def export_collection_asdf(self):
        try:
            database = self.data_ingestion_config.Database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mogo_client = pymongo.MongoClient(MONGO_DB)
            collection = self.mogo_client[database][collection_name]

            # Convert MongoDB cursor to list then to DataFrame
            df = pd.DataFrame(list(collection.find()))

            
            if df.empty:
                raise ValueError(f"No data found in MongoDB collection: {collection_name}")

            if '_id' in df.columns:
                df = df.drop(['_id'], axis=1)
            
           
            df.replace({'na': np.nan}, inplace=True)
            
            return df
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def feature_store_data_export(self, dataframe: pd.DataFrame):
        try:
            feature_store_path = self.data_ingestion_config.feature_store_filepath
            dir_path = os.path.dirname(feature_store_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def Trining_test_split(self, dataframe: pd.DataFrame):
        try:
            # The error n_samples=0 happens here if dataframe is empty
            Train_set, Test_set = train_test_split(
               dataframe, test_size=self.data_ingestion_config.train_test_split
            )
            logging.info('Performed Train test Split')

            dir_path = os.path.dirname(self.data_ingestion_config.traning_file_path)
            os.makedirs(dir_path, exist_ok=True)

            # Fix: Ensure you use traning_file_path for the training set
            Train_set.to_csv(
                self.data_ingestion_config.traning_file_path, index=False, header=True
            )

            Test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info('Exported Train and Test set')
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initate_data_ingestion(self):
        try:
            dataframe = self.export_collection_asdf()
            dataframe = self.feature_store_data_export(dataframe)
            self.Trining_test_split(dataframe)
            
            data_artifacts = DataIngestionArtifact(
            trained_file_path=self.data_ingestion_config.traning_file_path,
            test_file_path=self.data_ingestion_config.testing_file_path
            )
            return data_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)