from datetime import datetime
import os
from Networksecurity.constant import traning_pipeline

class TraningPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime('%m_%d_%Y_%M_%H_%S')
        self.Pipeliname_name = traning_pipeline.PIPELINE_NAME
        self.Artifect_name = traning_pipeline.ARTIFACTS_NAME
        self.Artifects_dir = os.path.join(self.Artifect_name,timestamp)
        self.timestamp : str = timestamp

class DataIngestionConfig:
    def __init__(self,tranning_pipeline_config:TraningPipelineConfig):
        self.dataingestion_dir = os.path.join(
            tranning_pipeline_config.Artifects_dir,traning_pipeline.DATA_INTEGRATION_DIR_NAME
        )
        self.feature_store_filepath = os.path.join(
            self.dataingestion_dir,traning_pipeline.DATA_INTEGRATION_FEATURE_STORE_DIR,traning_pipeline.FILE_NAME
        )
        self.traning_file_path = os.path.join(
            self.dataingestion_dir,traning_pipeline.DATA_INTEGRATION_INGESTED_DIR,traning_pipeline.TRAIN_FILE_NAME
        )
        self.testing_file_path = os.path.join(
            self.dataingestion_dir,traning_pipeline.DATA_INTEGRATION_INGESTED_DIR,traning_pipeline.TEST_FILE_NAME
        )
        self.train_test_split : float =traning_pipeline.DATA_INTEGRATION_TRAIN_TEST_SIZE
        self.collection_name :str = traning_pipeline.DATA_INTEGRATION_COLLECTION_NAME
        self.Database_name :str = traning_pipeline.DATA_INTEGRATION_DB_NAME

class DataValidationconfig:
    def __init__(self,tranning_pipeline_config:TraningPipelineConfig):
         self.data_velidation_dir : str = os.path.join(tranning_pipeline_config.Artifects_dir,traning_pipeline.DATA_VALIDATION_DIR_NAME)
         self.valid_dir : str = os.path.join(self.data_velidation_dir,traning_pipeline.DATA_VALIDATION_VALID_DIR)
         self.invalid_dir : str = os.path.join(self.data_velidation_dir,traning_pipeline.DATA_VALIDATION_INVALID_DIR)
         self.valid_Train_path : str = os.path.join(self.valid_dir,traning_pipeline.TRAIN_FILE_NAME)
         self.valid_Test_path : str = os.path.join(self.valid_dir,traning_pipeline.TEST_FILE_NAME)
         self.invalid_Train_path : str = os.path.join(self.invalid_dir,traning_pipeline.TRAIN_FILE_NAME)
         self.invalid_Test_path : str  = os.path.join(self.invalid_dir,traning_pipeline.TEST_FILE_NAME)
         self.drift_report : str = os.path.join(
             self.data_velidation_dir,
             traning_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
             traning_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
class datatransformationconfig:
    def __init__(self,tranning_pipeline_config:TraningPipelineConfig):
        self.data_transformation_dir : str = os.path.join(tranning_pipeline_config.Artifects_dir,traning_pipeline.DATA_TRANSFORMATRION_DIR_NAME)
        self.transformed_train_file_path : str = os.path.join(self.data_transformation_dir,traning_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
        traning_pipeline.TRAIN_FILE_NAME.replace('csv','npy'),)
        self.transformed_test_file_path : str = os.path.join(self.data_transformation_dir,traning_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
        traning_pipeline.TEST_FILE_NAME.replace('csv','npy'),)
        self.transformed_object_file_path : str = os.path.join(self.data_transformation_dir,traning_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
        traning_pipeline.PREPROCESSING_OBJ_FILE_NAME,)