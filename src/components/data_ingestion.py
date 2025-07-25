import os, sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation, DataTransformationConfig

from src.components.model_trainer import ModelTrainer, ModelTrainerConfig


@dataclass
class DataIngestionConfig:
    train_data_path:str = os.path.join('Artifact', 'train.csv')
    test_data_path: str = os.path.join('Artifact', 'test.csv')
    raw_data_path: str = os.path.join('Artifact', 'raw.csv')

class DataIngesion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method")
        try:
            csv_path = "Notebook/data/stud.csv"
            df = pd.read_csv(csv_path)
            logging.info(f"Reading csv is done with shape {df.shape}")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info('Train test split initiated')
            
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            logging.info('Train test split is completed')

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)

            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Splitted and saved in the artifact")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e, sys)
        

if __name__=='__main__':
    logging.info("\n\nDATA INGESTION IS INIIALIZING\n\n")
    obj = DataIngesion()
    train_data, test_data = obj.initiate_data_ingestion()
    logging.info("\n\nDATA INGESTION COMPLETED\n\n")

    logging.info("\n\nDATA TRANSFORMATION IS INIIALIZING\n\n")
    data_transformation = DataTransformation()
    train_arr, test_arr,_ = data_transformation.initiate_data_transformation(train_data, test_data)
    logging.info("\n\nDATA TRANSFORMATION COMPLETED\n\n")

    logging.info("\n\nMODEL TRAINER IS INIIALIZING\n\n")
    model_trainer = ModelTrainer()
    print(model_trainer.initiate_model_trainer(train_arr, test_arr))
    logging.info("\n\nMODEL TRAINER COMPLETED\n\n")


