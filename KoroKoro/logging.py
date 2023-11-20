import os
import logging
import sys
from datetime import datetime

logging_str = "[%(asctime)s: %(levelname)s: %(lineno)d:] %(message)s: --> %(pathname)s:"
logger_file_name = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"	

log_dir = os.path.join(os.getcwd(), "logs")
log_filepath = os.path.join(log_dir, logger_file_name)
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
  level=logging.INFO, 
  format=logging_str, 
  handlers=[
    logging.StreamHandler(sys.stdout),
    logging.FileHandler(log_filepath)
  ]
)

logger = logging.getLogger(__name__)
