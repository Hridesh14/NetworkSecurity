from Networksecurity.components.data_ingestion import DataIngustion
from Networksecurity.Exception.Exception import NetworkSecurityException
from Networksecurity.logging.logger import logging
from Networksecurity.entity.config_entity import DataIngestionConfig,DataValidationconfig ,datatransformationconfig
from Networksecurity.entity.config_entity import TraningPipelineConfig
from Networksecurity.components.data_validation import DataValidation
from Networksecurity.components.data_transformation import Data_Transformation

import sys

if __name__ =='__main__':
    try:
        TraningPipelineConfi = TraningPipelineConfig()
        DataIngestionConfi = DataIngestionConfig(TraningPipelineConfi)
        dataingestion = DataIngustion(DataIngestionConfi)
        logging.info('initate Data Inguetion')
        dataingustionartifacts = dataingestion.initate_data_ingestion()
        logging.info('Data Initiation completed')
        print(dataingustionartifacts)
        datavelid_config=DataValidationconfig(TraningPipelineConfi)
        datacelidation =DataValidation(dataingustionartifacts,datavelid_config)
        logging.info('initate Data velidation')
        data_velid_arti=datacelidation.initate_data_velidation() 
        logging.info('initate Data velidation complted')
        print(data_velid_arti)
        data_transformation_config=datatransformationconfig(TraningPipelineConfi)
        logging.info('Data Transformation Started')
        DATA_Transformation =Data_Transformation(data_velid_arti,data_transformation_config)
        Data_Transformation_artifect = DATA_Transformation.initate_data_transformation()
        logging.info('Data Transformation completed')
        print(Data_Transformation_artifect)


    except Exception as e:
        raise NetworkSecurityException(e,sys)



