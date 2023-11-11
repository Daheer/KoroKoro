from KoroKoro.utils import bin_colors, read_config
from KoroKoro.logging import logger
from KoroKoro.entity import ProductConfig
import torch.cuda.is_available as gpu_ready

class DataProcessing:
  def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
    self.config = read_config(config_file_path)
  
  def process_data(self) -> None:
    logger.info(f"{bin_colors.INFO}Processing video for {self.config.unique_id}{bin_colors.ENDC}")
    if not os.path.exists(self.config.colmap_output):
      if gpu_ready():
        os.system(f"ns-process-data video --data {self.config.video_output} --output-dir {self.config.colmap_output} --gpu")
      else:
        os.system(f"ns-process-data video --data {self.config.video_output} --output-dir {self.config.colmap_output}")