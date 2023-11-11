import os
import sys

from KoroKoro.utils import bin_colors
from KoroKoro.logging import logger
from KoroKoro.config.configuration import ConfigurationManager
from KoroKoro.utils.constants import CONFIG_FILE_PATH

class ModelTrainer:
  def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
    self.config_manager = ConfigurationManager(config_file_path)
    self.config = self.config_manager.get_config()

  def train_model(self) -> None:
    logger.info(f"{bin_colors.INFO}Running model for {self.config.unique_id}{bin_colors.ENDC}")
    try:
      os.system(f"python3 instant-ngp/scripts/run.py --scene {self.config.colmap_output} --n_steps 5000 --save_mesh {self.config.obj_output}")
    except Exception as e:
      logger.error(f"{bin_colors.ERROR}Error while running model {e}{bin_colors.ENDC}")
      sys.exit(1)
    logger.info(f"{bin_colors.SUCCESS}Model trained successfully!{bin_colors.ENDC}"
    logger.info(f"{bin_colors.SUCCESS}Model successfully saved at {self.config.obj_output}{bin_colors.ENDC}")

if __name__ == "__main__":
  model_trainer = ModelTrainer()
  model_trainer.train_model()