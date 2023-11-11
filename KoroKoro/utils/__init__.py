from typing import List, Dict, Any
import yaml
from pathlib import Path
from ensure import ensure_annotations
from box import ConfigBox
import os

from KoroKoro.logging import logger

def sort_product_listings(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
  return sorted(data, key=lambda x: {'IDLE': 1, 'FAILED': 2, 'PROCESSING': 3, 'DONE': 4}.get(x['status'], float('inf')))

class bin_colors:
  HEADER = '\033[95m'
  INFO = '\033[94m'
  OKCYAN = '\033[96m'
  SUCCESS = '\033[92m'
  WARNING = '\033[93m'
  ERROR = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

def save_config(config: Dict[str, str], file_path: Path) -> None:
  """
  Save a dictionary to a yaml file.
  """
  try:
    with open(file_path, 'w') as file:
      yaml.dump(config, file)
      logger.info(f"{bin_colors.INFO}{file_path} saved successfully.{bin_colors.ENDC}")
  except Exception as e:
    logger.error(f"{bin_colors.ERROR}Error saving yaml file at {file_path}.{bin_colors.ENDC}")
    raise e

@ensure_annotations
def read_config(path_to_yaml: Path) -> ConfigBox:
  """
  Read a yaml file and return a ConfigBox object.
  """
  try:
    with open(path_to_yaml, "r") as yaml_file:
      yaml_dict = yaml.safe_load(yaml_file)
      logger.info(f"{bin_colors.INFO}{yaml_file.name} read successfully.{bin_colors.ENDC}")
      return ConfigBox(yaml_dict)
  except Exception as e:
    raise e
    logger.error(f"{bin_colors.ERROR}Error reading yaml file at {path_to_yaml}.{bin_colors.ENDC}")
  
def create_directory(path: Path) -> None:
  """
  Create a directory if it does not exist.
  """
  try:
    if not os.path.exists(path):
      os.makedirs(path)
      logger.info(f"{bin_colors.INFO}Directory created at {path}.{bin_colors.ENDC}")
  except Exception as e:
    logger.error(f"{bin_colors.ERROR}Error creating directory at {path}.{bin_colors.ENDC}")
    raise e