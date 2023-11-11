import os

from KoroKoro.components.data_ingestion import DataIngestion
from KoroKoro.components.data_processing import DataProcessing
from KoroKoro.components.data_transformation import DataTransformation
from KoroKoro.components.model_trainer import ModelTrainer
from KoroKoro.components.post_processing import supabase

from KoroKoro.utils import bin_colors
from KoroKoro.logging import logger

try:
  logger.info(f"{bin_colors.INFO}Starting reconstruction pipeline{bin_colors.ENDC}")
  os.system("python3 KoroKoro/components/initialization.py")
  DataIngestion().download_data()
  DataProcessing().process_data()
  DataTransformation().transform_data()
  ModelTrainer().train_model()
  os.system("python3 KoroKoro/components/post_processing.py")
  logger.info(f"{bin_colors.SUCCESS}Reconstruction pipeline executed successfully!{bin_colors.ENDC}")
except Exception as e:
  supabase.table('products').update({'status': 'FAILED'}).eq('unique_id', config.unique_id).execute()
  logger.error(f"{bin_colors.ERROR}Error while running pipeline: {e}{bin_colors.ENDC}")
  raise e
