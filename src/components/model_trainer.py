import os
import sys 
from dataclasses import dataclass
from catboost import CatBoostRegressor
from sklearn.ensemble import (

    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
import dill
import pickle 

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from exception import CustomException
from logger import logging
from utils import save_object,evaluate_models



@dataclass
class ModelTrainingConfig:
    trained_model_file_path=os.path.join("artificats","model.pkl")
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainingConfig()
    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Splitting Training and Test input data")
            x_train,y_train,x_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decison Trss": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbour Classifier": KNeighborsRegressor(),
                "XGBClassifier":XGBRegressor(),
                "CatBoosting Classifier": CatBoostRegressor(),
                "AdaBoost Classifier": AdaBoostRegressor()

            }
            model_report:dict=evaluate_models(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models)
            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]
            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info("Best Model Found")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            predicted=best_model.predict(x_test)
            r2_square = r2_score(y_test, predicted)
            return r2_square
        except:
            pass