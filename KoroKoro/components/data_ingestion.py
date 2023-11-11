import os
import requests

from KoroKoro.utils import bin_colors, read_config, create_directory
from KoroKoro.logging import logger
from KoroKoro.entity import ProductConfig
from KoroKoro.utils.constants import CONFIG_FILE_PATH
from KoroKoro.config.configuration import ConfigurationManager

class DataIngestion:
  def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
    self.config_manager = ConfigurationManager(config_file_path)
    self.config = self.config_manager.get_config()
    create_directory(self.config.output_dir)

  def download_data(self) -> None:
    logger.info(f"{bin_colors.INFO}Downloading data for {self.config.unique_id}{bin_colors.ENDC}")   
    response = requests.get(self.config.video_link)
    if response.status_code == 200:
      if not os.path.exists(self.config.video_output):
        with open(self.config.video_output, 'wb') as file:
            file.write(response.content)
        logger.info(f"{bin_colors.SUCCESS}Successfully downloaded file at {self.config.video_output}{bin_colors.ENDC}")
      else:
        logger.info(f"{bin_colors.WARNING}File already exists at {self.config.video_output}{bin_colors.ENDC}")
    else:
      logger.error(f"{bin_colors.ERROR}Failed to download file{bin_colors.ENDC}")
      raise e