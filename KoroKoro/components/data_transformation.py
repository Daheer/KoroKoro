from KoroKoro.utils import bin_colors, read_config
from KoroKoro.logging import logger
from KoroKoro.entity import ProductConfig

class DataTransformation:
  def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
    self.config = read_config(config_file_path)
  
  def transform_data(self) -> None:
    logger.info(f"{bin_colors.INFO}Transforming colmap data for {self.config.unique_id}{bin_colors.ENDC}")

    