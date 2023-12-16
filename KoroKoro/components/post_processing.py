import dotenv
import os
from supabase import create_client, Client

from KoroKoro.logger import logger
from KoroKoro.utils import bin_colors, read_config, split_obj_file
from KoroKoro.config.configuration import ConfigurationManager
from KoroKoro.utils.constants import CONFIG_FILE_PATH

dotenv.load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

try:
  supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
  products = supabase.table('products').select("*").execute()
  logger.info(f"{bin_colors.SUCCESS}Supabase connection successful{bin_colors.ENDC}")
except Exception as e:
  logger.error(f"{bin_colors.ERROR}Supabase connection failed: {e}{bin_colors.ENDC}")
  raise e

config_manager = ConfigurationManager(CONFIG_FILE_PATH)
config = config_manager.get_config()

try:
  logger.info(f"{bin_colors.OKCYAN}Uploading {config.unique_id} result to database{bin_colors.ENDC}")
  split_obj_file(config.obj_output, config.colmap_output)
  for file in os.listdir(config.colmap_output):
    if file.endswith(".txt"):
      filepath = os.path.join(config.colmap_output, file)
      with open(filepath, 'rb') as f:
        supabase.storage.from_("korokoro_bucket").upload(file=f,path=f"{config.unique_id}/{file}", file_options={"content-type": "plain/text"})
except Exception as e:
  logger.error(f"{bin_colors.ERROR}Failed to upload model result: {e}{bin_colors.ENDC}")
  raise e

try:
  logger.info(f"{bin_colors.OKCYAN}Updating product status: {config.unique_id}{bin_colors.ENDC}")
  supabase.table('products').update({'status': 'DONE'}).eq('unique_id', config.unique_id).execute()
except Exception as e:
  logger.error(f"{bin_colors.ERROR}Failed to update product status: {e}{bin_colors.ENDC}")
  raise e