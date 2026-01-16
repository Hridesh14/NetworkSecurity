from Networksecurity.entity.artifacts_entity import DataIngestionArtifact,DataValidationArtifacts
from Networksecurity.entity.config_entity import DataValidationconfig
from Networksecurity.Exception.Exception import NetworkSecurityException
from Networksecurity.logging.logger import logging
from Networksecurity.constant.traning_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd 
import numpy as np
import sys,os 
from Networksecurity.utils.Main_utils.utils import read_yaml_file,Write_yaml_file

class DataValidation:
    def __init__(self,data_ingustion_artifict:DataIngestionArtifact,
                 data_validation_config:DataValidationconfig):
        try:
            self.data_integration_artificts=data_ingustion_artifict
            self.data_validation_config = data_validation_config
            self._schema_config  = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    
    @staticmethod
    def read_dta(file_path)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    
    def velidation_nunmber_Column(self,dataframe:pd.DataFrame)->bool:
        try:
            num_of_column = len(self._schema_config)
            logging.info(f'Required no of column:{num_of_column}')

            logging.info(f'Dataframe has columns:{len(dataframe.columns)}')

            if len(dataframe.columns)==num_of_column:
                return True
            else:
                False
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def velidate_numerical_column(self,dataframe =pd.DataFrame)->bool:
        try:
            numerical_columns = dataframe.select_dtypes(include=[np.number]).columns 
            if len(numerical_columns)== len(dataframe.columns):
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status = True
            reports = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist =ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found =True
                    status=False
                reports.update({column:{
                    'Pvalue':float(is_same_dist.pvalue),
                    'Drift_stus': is_found

                }})
            drift_repor_file_path = self.data_validation_config.drift_report

            dir_pth = os.path.dirname(drift_repor_file_path)
            os.makedirs(dir_pth,exist_ok=True)
            Write_yaml_file(file_path=drift_repor_file_path,constent=reports)
            return status

        except Exception as e:
            raise NetworkSecurityException(e,sys)


    
    def initate_data_velidation(self)-> DataValidationArtifacts:
        try:
            Train_file_path = self.data_integration_artificts.trained_file_path
            Test_file_path = self.data_integration_artificts.test_file_path

            ## read data from train and test
            Train_dataframe = DataValidation.read_dta(Train_file_path)
            Test_dataframe = DataValidation.read_dta(Test_file_path)

            status = self.velidation_nunmber_Column(dataframe=Train_dataframe)
            if not status:
                error_message = f' Train dataframe does not contain all columns.\n'
            status = self.velidation_nunmber_Column(dataframe=Test_dataframe)
            if not status:
                error_message = f' Test dataframe does not contain all columns.\n'

            numerical_col = self.velidate_numerical_column(dataframe=Train_dataframe)
            if not numerical_col:
                error = f'The Train Dataframe does not contain numerical columns.\n '
            numerical_col = self.velidate_numerical_column(dataframe=Test_dataframe)
            if not numerical_col:
                error = f'The Test Dataframe does not contain numerical columns.\n '
            
            # cheack data drift
            status= self.detect_dataset_drift(base_df=Train_dataframe,current_df=Test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_Train_path)
            os.makedirs(dir_path,exist_ok=True)

            Train_dataframe.to_csv(
                self.data_validation_config.valid_Train_path,index=False,header=True
            )
            

            Test_dataframe.to_csv(
                self.data_validation_config.valid_Test_path,index=False,header=True
            )


            data_validation_artifact = DataValidationArtifacts(
                validation_status=status,  # Ensure this matches your entity field name
                valid_train_file_path=self.data_validation_config.valid_Train_path,
                valid_test_file_path=self.data_validation_config.valid_Test_path,
                invalid_train_file_path=self.data_validation_config.invalid_Train_path,
                invalid_test_file_path=self.data_validation_config.invalid_Test_path,
                drift_report_file_path=self.data_validation_config.drift_report
            )
            return data_validation_artifact


        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

