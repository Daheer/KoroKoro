import os
import subprocess

from KoroKoro.utils import bin_colors, read_config
from KoroKoro.logger import logger
from KoroKoro.entity import ProductConfig
from KoroKoro.utils.constants import CONFIG_FILE_PATH
from KoroKoro.utils import create_directory, extract_frames
from KoroKoro.config.configuration import ConfigurationManager

from torch.cuda import is_available as gpu_ready


class DataProcessing:
    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        self.config_manager = ConfigurationManager(config_file_path)
        self.config = self.config_manager.get_config()

    def process_data(self) -> None:
        try:
            logger.info(
                f"{bin_colors.INFO}Processing video for {self.config.unique_id}{bin_colors.ENDC}"
            )
            if not os.path.exists(self.config.colmap_output):
                create_directory(self.config.colmap_output)
            if not os.path.exists(self.config.frames_path):
                create_directory(self.config.frames_path)

            extract_frames(
                video_path=self.config.video_output, frames_path=self.config.frames_path
            )

            if gpu_ready():
                subprocess.run(
                    f"ns-process-data images --data {self.config.frames_path} --output-dir {self.config.colmap_output} --gpu --no-verbose --num-downscales 0",
                    check=True,
                    shell=True,
                )
            else:
                subprocess.run(
                    f"ns-process-data images --data {self.config.frames_path} --output-dir {self.config.colmap_output} --no-verbose --num-downscales 0",
                    check=True,
                    shell=True,
                )
        except Exception as e:
            logger.error(
                f"{bin_colors.ERROR}Error while processing data {e}{bin_colors.ENDC}"
            )
            raise e
