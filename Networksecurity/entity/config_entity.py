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
        self.traning_pipeline = os.path.join(
            self.dataingestion_dir,traning_pipeline.DATA_INTEGRATION_FEATURE_STORE_DIR,traning_pipeline.TRAIN_FILE_NAME
        )
        self.testing_pipeline = os.path.join(
            self.dataingestion_dir,traning_pipeline.DATA_INTEGRATION_FEATURE_STORE_DIR,traning_pipeline.TEST_FILE_NAME
        )
        self.train_test_split : float =traning_pipeline.DATA_INTEGRATION_TRAIN_TEST_SPLIR
        self.collection_name :str = traning_pipeline.DATA_INTEGRATION_COLLECTION_NAME
        self.Database_name :str = traning_pipeline.DATA_INTEGRATION_DB_NAME