import os
import dotenv
import subprocess
from supabase import create_client, Client

from KoroKoro.components.data_transformation import DataTransformation
from KoroKoro.components.model_trainer import ModelTrainer

from KoroKoro.utils import bin_colors, read_config
from KoroKoro.utils.constants import CONFIG_FILE_PATH
from KoroKoro.logger import logger

dotenv.load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

config = read_config(CONFIG_FILE_PATH) 

try:
  logger.info(f"{bin_colors.INFO}Starting reconstruction pipeline{bin_colors.ENDC}")
  supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
  DataTransformation().transform_data()
  ModelTrainer().train_model()
  # os.system("python3 KoroKoro/components/post_processing.py")
  subprocess.run("python3 KoroKoro/components/post_processing.py", check = True, shell = True)
  logger.info(f"{bin_colors.SUCCESS}Stage 02 of reconstruction pipeline executed successfully!{bin_colors.ENDC}")
except Exception as e:
  supabase.table('products').update({'status': 'FAILED'}).eq('unique_id', config.unique_id).execute()
  logger.error(f"{bin_colors.ERROR}Error while running pipeline: {e}{bin_colors.ENDC}")
  raise e
finally:
  if not os.path.exists(f"artifacts/{config.unique_id}/part1.txt"):
    supabase.table('products').update({'status': 'FAILED'}).eq('unique_id', config.unique_id).execute()
    logger.error(f"{bin_colors.ERROR}Error while running pipeline{bin_colors.ENDC}")


  
