import yaml
from Networksecurity.logging.logger import logging
from Networksecurity.Exception.Exception import NetworkSecurityException
import os,sys
import numpy as np
import pandas as pd
import dill
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
def read_yaml_file(file_path:str)-> dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
    
import os
import sys
import yaml

def Write_yaml_file(file_path: str, constent: object, replace: bool = False) -> None:
    try:
        # 1. Handle replacement logic
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # 2. Ensure the directory structure exists
        # This part is correct in your code, but the error happens in the next step
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # 3. Attempt to write the file
        with open(file_path, 'w') as file:
            yaml.dump(constent, file)
            
    except PermissionError as e:
        # Specifically catch the permission error to give a better hint
        raise NetworkSecurityException(
            f"Permission Denied: Cannot write to {file_path}. "
            "Try running the terminal as Administrator or move the project folder "
            "out of 'Program Files'.", sys
        )
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_numpy_arry(file_path:str ,array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_path,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
    
def save_object(file_path: str ,obj: object)-> None:
    try:
        logging.info('Entered the save file object method of MainUtils class')
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj ,file_obj)
        logging.info('Exited the save_object method of MainUtils class')
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
    
def load_object(file_path:str,)-> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f'The file: {file_path} is not exists')
        with open(file_path,'rb') as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e

def load_numpy_array_data(file_path: str)-> np.array:
    try:
        with open(file_path,'rb')as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e

def Evaluate_models(x_train,y_train,x_test,y_test,models,parems):
    reports ={}

    try:
        for i in range(len(list(models))):
         model = list(models.values())[i]
         model_list = list(models.keys())
         model_name = model_list[i]
         para = parems[model_name]
        

         gs = GridSearchCV(model,para,cv=3)
         gs.fit(x_train,y_train)

         model.set_params(**gs.best_params_)
         model.fit(x_train,y_train)

         y_train_pred = model.predict(x_train)
         y_test_pred = model.predict(x_test)

         train_model_score = r2_score(y_train,y_train_pred)

         test_model_score = r2_score(y_test,y_test_pred)

         reports[list(models.keys())[i]]= test_model_score 

        return reports
    except Exception as e:
        raise NetworkSecurityException(e,sys)

import re
from urllib.parse import urlparse

def extract_features_from_url(url:str):
    features ={}
    features['url_length']=len(url)
    parsed_url = urlparse(url)
    features['hostname_length'] = len(parsed_url.netloc)
    features['path_length'] = len(parsed_url.path)
    features['count_at'] = url.count('@')
    features['count_question'] = url.count('?')
    features['count_hyphen'] = url.count('-')
    features['count_equal'] = url.count('=')
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    features['has_ip'] = 1 if re.search(ip_pattern, url) else 0

    return features