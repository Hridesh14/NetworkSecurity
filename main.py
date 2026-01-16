from Networksecurity.components.data_ingestion import DataIngustion
from Networksecurity.Exception.Exception import NetworkSecurityException
from Networksecurity.logging.logger import logging
from Networksecurity.entity.config_entity import DataIngestionConfig,DataValidationconfig
from Networksecurity.entity.config_entity import TraningPipelineConfig
from Networksecurity.components.data_validation import DataValidation

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
        


    except Exception as e:
        raise NetworkSecurityException(e,sys)



