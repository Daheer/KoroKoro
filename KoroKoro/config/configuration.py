from KoroKoro.utils import bin_colors, read_config
from KoroKoro.utils.constants import CONFIG_FILE_PATH
from KoroKoro.entity import ProductConfig

class ConfigurationManager:
  def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
    self.config = read_config(config_file_path)

  def get_config(self) -> ProductConfig:
    product_config = ProductConfig.from_dict(self.config)
    return product_config