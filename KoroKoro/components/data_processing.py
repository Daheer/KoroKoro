import os

from KoroKoro.utils import bin_colors, read_config
from KoroKoro.logging import logger
from KoroKoro.entity import ProductConfig
from KoroKoro.utils.constants import CONFIG_FILE_PATH
from KoroKoro.utils import create_directory
from KoroKoro.config.configuration import ConfigurationManager

from torch.cuda import is_available as gpu_ready

class DataProcessing:
  def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
    self.config_manager = ConfigurationManager(config_file_path)
    self.config = self.config_manager.get_config()
  
  def process_data(self) -> None:
    try
      logger.info(f"{bin_colors.INFO}Processing video for {self.config.unique_id}{bin_colors.ENDC}")
      if not os.path.exists(self.config.colmap_output):
        create_directory(self.config.colmap_output)
      if gpu_ready():
        os.system(f"ns-process-data video --data {self.config.video_output} --output-dir {self.config.colmap_output} --gpu")
      else:
        os.system(f"ns-process-data video --data {self.config.video_output} --output-dir {self.config.colmap_output}")
    except SystemExit as e:
      logger.error(f"{bin_colors.ERROR}Error while processing data {e}{bin_colors.ENDC}")
      raise e
    except Exception as e:
      logger.error(f"{bin_colors.ERROR}Error while processing data {e}{bin_colors.ENDC}")
      raise e