import yaml
from Networksecurity.logging.logger import logging
from Networksecurity.Exception.Exception import NetworkSecurityException
import os,sys
import numpy as np
import pandas as pd
import dill
import pickle
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