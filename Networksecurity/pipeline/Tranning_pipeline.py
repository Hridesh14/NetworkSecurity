import os
import sys

from Networksecurity.Exception.Exception import NetworkSecurityException
from Networksecurity.logging.logger import logging
from Networksecurity.components.data_ingestion import DataIngustion
from Networksecurity.components.data_validation import DataValidation
from Networksecurity.components.data_transformation import Data_Transformation
from Networksecurity.components.Model_trainer import ModelTrainner

from Networksecurity.entity.config_entity import(
    TraningPipelineConfig,
    DataIngestionConfig,
    DataValidationconfig,
    datatransformationconfig,
    Modeltrainerconfig
)

from Networksecurity.entity.artifacts_entity import (
    DataIngestionArtifact,
    DataValidationArtifacts,
    DataTransformationArtifects,
    ModleTrainerArtifact
)

class TranningPipeline:
    def __init__(self):
        self.tranning_pipeline_config = TraningPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(tranning_pipeline_config=self.tranning_pipeline_config)
            logging.info('Start Data Ingestion')
            
            data_ingestion = DataIngustion(data_ingestion_config=self.data_ingestion_config)
            
            data_ingestion_artifact = data_ingestion.initate_data_ingestion()
            logging.info('Data Ingestion Completed')
            return data_ingestion_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            data_validation_config = DataValidationconfig(tranning_pipeline_config=self.tranning_pipeline_config)
            
            logging.info('Initiate Data Validation')
            
            data_validation = DataValidation(
                data_ingustion_artifict=data_ingestion_artifact, 
                data_validation_config=data_validation_config
            )
            
            data_validation_artifact = data_validation.initate_data_velidation()
            return data_validation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifacts):
        try:
            data_transformation_config = datatransformationconfig(tranning_pipeline_config=self.tranning_pipeline_config)
            logging.info('Data Transformation Started')
            
            DATA_Transformation = Data_Transformation(
                data_validation_artifact=data_validation_artifact,
                dataTransformationconfig=data_transformation_config
            )
            
            data_transformation_artifact = DATA_Transformation.initate_data_transformation()
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_model_training(self, data_transformation_artifact: DataTransformationArtifects) -> ModleTrainerArtifact:
        try:
            logging.info('Model Training Started')
            
            # Reverted to use 'tranning_pipeline_coinfig' (with the typo 'coinfig')
            # This matches the typo found in your original code snippet.
            model_trainer_config = Modeltrainerconfig(tranning_pipeline_coinfig=self.tranning_pipeline_config)
            
            Model_Trainner = ModelTrainner(
                model_trainer_config=model_trainer_config,
                data_transformatuion_artifect=data_transformation_artifact
            )
            
            model_trainer_artifact = Model_Trainner.initate_model_trainer()
            return model_trainer_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
            
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            
            model_trainer_artifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)
            
            return model_trainer_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)