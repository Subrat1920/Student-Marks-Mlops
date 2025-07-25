import os, sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class DataTransformationConfig: 
    preprocessort_ob_file_path = os.path.join('Artifact', 'preprocessor', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_columns = ['writing_score', 'reading_score']

            categorical_columns = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy='median')),
                    ("Scaler", StandardScaler())
                ]
            )
            logging.info("Numerical Columns standardization completed")
            cat_pipeline = Pipeline(
                steps=[
                    ("Imputer", SimpleImputer(strategy='most_frequent')),
                    ("one_hot_encoding", OneHotEncoder()),
                    ("Scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info("Categorical Columns encoding completed")

            logging.info(f"Categorical Columns : {categorical_columns}")
            logging.info(f"Numerical Columns : {numerical_columns}")

            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline", num_pipeline, numerical_columns),
                    ('categorical pipeline', cat_pipeline, categorical_columns)
                ]
            )
            logging.info('Pre-Processing of the numerical and categorical columns is over')

            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info('Read train and test data is completed')
            logging.info("Obtaining pre-processing object")

            preprocessor_obj = self.get_data_transformer_object()

            target_column_name = 'math_score'
            numerical_columns = ['writing_score', 'reading_score']

            input_features_train_df = train_df.drop(columns=[target_column_name], axis=1)

            target_feature_train_df = train_df[target_column_name]

            input_features_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(f"Applying pre-processing object on training dataframe and testing dataframe")

            input_feature_train_arr = preprocessor_obj.fit_transform(input_features_train_df)

            input_feature_test_arr = preprocessor_obj.transform(input_features_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)    
            ]

            logging.info("Saving preprocess object")

            save_object(
                file_path = self.data_transformation_config.preprocessort_ob_file_path,
                obj = preprocessor_obj
            )

            return (
                train_arr, test_arr, self.data_transformation_config.preprocessort_ob_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
        


