import os
import sys

from Networksecurity.Exception.Exception import NetworkSecurityException
from Networksecurity.logging.logger import logging

from Networksecurity.entity.artifacts_entity import DataTransformationArtifects,ModleTrainerArtifact
from Networksecurity.entity.config_entity import Modeltrainerconfig

from Networksecurity.utils.ml_utils.model.estimater import NetworkModel
from Networksecurity.utils.Main_utils.utils import save_object,load_object,load_numpy_array_data,Evaluate_models
from Networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import(
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier,
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from catboost import CatBoostClassifier



class ModelTrainner:
    def __init__(self,model_trainer_config:Modeltrainerconfig,data_transformatuion_artifect:DataTransformationArtifects):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifect= data_transformatuion_artifect
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def train_model(self,x_train,y_train,x_test,y_test):
        models = {
            'Random Forest': RandomForestClassifier(verbose=1),
            'Decision Tree': DecisionTreeClassifier(),
            'Logistic Regressor': LogisticRegression(verbose=1),
            'AdaBoost': AdaBoostClassifier(),
            'GridBoost':GradientBoostingClassifier(),
            'KNeighbors':KNeighborsClassifier(),
            'CatBoost': CatBoostClassifier(),

        }

        param_dict = {
        'Random Forest': {
        'n_estimators': [100, 200, 500],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'criterion': ['gini', 'entropy']
    },
        'Decision Tree': {
        'criterion': ['gini', 'entropy'],
        'max_depth': [None, 5, 10, 20],
        'min_samples_split': [2, 10, 20],
        'splitter': ['best', 'random']
    },
        'Logistic Regressor': {
        'penalty': ['l1', 'l2', 'elasticnet'],
        'C': [0.01, 0.1, 1, 10],
        'solver': ['liblinear', 'saga'],
        'max_iter': [100, 500]
    },
        'AdaBoost': {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.1, 1.0],
        'algorithm': ['SAMME', 'SAMME.R']
    },
        'GridBoost': {  # GradientBoostingClassifier
        'learning_rate': [0.01, 0.1, 0.2],
        'n_estimators': [100, 200],
        'subsample': [0.8, 1.0],
        'max_depth': [3, 5, 8]
    },
        'KNeighbors': {
        'n_neighbors': [3, 5, 7, 9],
        'weights': ['uniform', 'distance'],
        'algorithm': ['auto', 'ball_tree', 'kd_tree']
    },
         'CatBoost': {
        'depth': [4, 6, 10],
        'learning_rate': [0.01, 0.03, 0.1],
        'iterations': [100, 500, 1000],
        'l2_leaf_reg': [1, 3, 5]
       }
     }
        model_Reports : dict = Evaluate_models(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models,parems=param_dict)
        best_model_score = max(sorted(model_Reports.values()))
        best_model_index = list(model_Reports.values()).index(best_model_score)
        best_model_name = list(model_Reports.keys())[
            list(model_Reports.values()).index(best_model_score)
        ]
        best_model = models[best_model_name]
        y_train_pred = best_model.predict(x_train)
        classification_train_metric = get_classification_score(y_true=y_train,y_pred=y_train_pred)


        # Track teh ml flow
        y_test_pred = best_model.predict(x_test)
        calcification_test_metric = get_classification_score(y_true=y_test,y_pred=y_test_pred)


        preprocessor = load_object(file_path=self.data_transformation_artifect.transformed_object_file_path)
        model_dir_pth = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_pth,exist_ok=True)

        network_model=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,obj=network_model)


        #modelTrainer atrifect

        model_trainer_artifect = ModleTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metric,
                             test_metric_artifact=calcification_test_metric)
        logging.info(f'model trainer artifects {model_trainer_artifect}')
        return model_trainer_artifect




        



    def initate_model_trainer(self)-> ModleTrainerArtifact:
        try:
            train_file_pth = self.data_transformation_artifect.transformed_train_file_path
            test_file_pth = self.data_transformation_artifect.trasnformed_test_file_path

            #lodding traing arry and test arry
            train_arr = load_numpy_array_data(train_file_pth)
            test_arr = load_numpy_array_data(test_file_pth)

            x_train,y_train,x_test,y_test=(
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],   
            )
            model_trainer_artifect = self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifect
        except Exception as e:
            raise NetworkSecurityException(e,sys)