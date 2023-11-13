import dotenv
import os
import sys
from supabase import create_client, Client

from KoroKoro.logging import logger
from KoroKoro.utils import bin_colors, sort_product_listings, save_config
from KoroKoro.utils.constants import CONFIG_FILE_PATH
from KoroKoro.entity import ProductConfig

dotenv.load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

try:
  supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
  products = supabase.table('products').select("*").execute()
  logger.info(f"{bin_colors.SUCCESS}Supabase connection successful{bin_colors.ENDC}")
except Exception as e:
  logger.error(f"{bin_colors.ERROR}Supabase connection failed: {e}{bin_colors.ENDC}")
  raise e

products = sort_product_listings(products.data)

product = next((p for p in products if p['status'] != "PROCESSING"), None)

if product is None:
  logger.info(f"{bin_colors.OKCYAN}No products to process! Toodles Exiting...{bin_colors.ENDC}")
  sys.exit(0)

try:
  logger.info(f"{bin_colors.INFO}Processing product: {product['unique_id']}{bin_colors.ENDC}")
  supabase.table('products').update({'status': 'PROCESSING'}).eq('unique_id', product['unique_id']).execute()
  save_config(product, CONFIG_FILE_PATH)
except Exception as e:
  logger.error(f"{bin_colors.ERROR}Failed to update product status: {e}{bin_colors.ENDC}")
  raise e