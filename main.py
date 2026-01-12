from Networksecurity.components.data_ingestion import DataIngustion
from Networksecurity.Exception.Exception import NetworkSecurityException
from Networksecurity.logging.logger import logging
from Networksecurity.entity.config_entity import DataIngestionConfig
from Networksecurity.entity.config_entity import TraningPipelineConfig

import sys

if __name__ =='__main__':
    try:
        TraningPipelineConfi = TraningPipelineConfig()
        DataIngestionConfi = DataIngestionConfig(TraningPipelineConfi)
        dataingestion = DataIngustion(DataIngestionConfi)
        logging.info('initate Data Ingustion config')
        dataingustionartifacts = dataingestion.initate_data_ingestion()
        print(dataingustionartifacts)


    except Exception as e:
        raise NetworkSecurityException(e,sys)



