import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from Networksecurity.constant.traning_pipeline import TARGET_COLUMN_NAME
from Networksecurity.constant.traning_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from Networksecurity.logging.logger import logging
from Networksecurity.Exception.Exception import NetworkSecurityException
from Networksecurity.entity.artifacts_entity import (
   DataTransformationArtifects,
   DataValidationArtifacts
)
from Networksecurity.entity.config_entity import datatransformationconfig
from Networksecurity.utils.Main_utils.utils import save_numpy_arry,save_object




class Data_Transformation:
    def __init__(self, datavelidationartifict:DataValidationArtifacts,
                 dataTransformationconfig:datatransformationconfig):
        try:
            self.datavelidation_artifect:DataValidationArtifacts=datavelidationartifict
            self.dataTransformationconfig:datatransformationconfig = dataTransformationconfig
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def get_data_transformer(cls)-> Pipeline:
        
        logging.info(
            'entered get_data_transformet_object methord of transformer class '
        )
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(
                f'Initiliase KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}'
            )
            processor:Pipeline=Pipeline([('imputer',imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
        
        

    def initate_data_transformation(self)->DataTransformationArtifects:
        logging.info('Entered initate data_transformation methord of DataTransformation class')
        try:
            logging.info('started Data Trandsformation')
            train_df = Data_Transformation.read_data(self.datavelidation_artifect.valid_train_file_path)
            test_df = Data_Transformation.read_data(self.datavelidation_artifect.valid_test_file_path)


            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN_NAME],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN_NAME]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN_NAME],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN_NAME]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            preprocessor = self.get_data_transformer()
            preprocessor_obj = preprocessor.fit(input_feature_train_df)
            transform_input_train_feature = preprocessor_obj.transform(input_feature_train_df)
            transform_input_test_feature = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[transform_input_train_feature,np.array(target_feature_train_df)]
            test_arr = np.c_[transform_input_test_feature,np.array(target_feature_test_df)]

            save_numpy_arry(self.dataTransformationconfig.transformed_train_file_path,array=train_arr)
            save_numpy_arry(self.dataTransformationconfig.transformed_test_file_path,array=test_arr)
            save_object(self.dataTransformationconfig.transformed_object_file_path,preprocessor_obj)


            data_transformation_artifect = DataTransformationArtifects(
                transformed_object_file_path=self.dataTransformationconfig.transformed_object_file_path,
                transformed_train_file_path=self.dataTransformationconfig.transformed_train_file_path,
                trasnformed_test_file_path=self.dataTransformationconfig.transformed_test_file_path
            )
            return data_transformation_artifect
            




        except Exception as e:
            raise NetworkSecurityException(e,sys)
