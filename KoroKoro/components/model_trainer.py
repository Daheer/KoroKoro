import os
import sys
import subprocess

from KoroKoro.utils import bin_colors, create_directory
from KoroKoro.logger import logger
from KoroKoro.config.configuration import ConfigurationManager
from KoroKoro.utils.constants import CONFIG_FILE_PATH


class ModelTrainer:
    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        self.config_manager = ConfigurationManager(config_file_path)
        self.config = self.config_manager.get_config()

    def train_model(self) -> None:
        logger.info(
            f"{bin_colors.INFO}Running model for {self.config.unique_id}{bin_colors.ENDC}"
        )
        result_folder = os.path.join(self.config.output_dir, self.config.unique_id)
        if not os.path.exists(result_folder):
            create_directory(result_folder)
        try:
            subprocess.run(
                f"ns-train splatfacto --data {self.config.colmap_output} --output-dir {result_folder} --viewer.quit-on-train-completion True",
                check=True,
                shell=True,
            )
            runs_folder = os.path.join(result_folder, "splatfacto")
            runs = [
                d
                for d in os.listdir(runs_folder)
                if os.path.isdir(os.path.join(runs_folder, d))
            ]
            latest_run = max(
                runs, key=lambda x: os.path.getctime(os.path.join(runs_folder, x))
            )
            subprocess.run(
                f"ns-export gaussian-splat --load-config {os.path.join(runs_folder, latest_run, 'config.yml')} --output-dir {result_folder}",
                check=True,
                shell=True,
            )

            # os.system(f"python3 instant-ngp/scripts/run.py --scene {self.config.colmap_output} --n_steps 5000 --save_mesh {self.config.obj_output}")
            # subprocess.run(f"python3 instant-ngp/scripts/run.py --scene {self.config.colmap_output} --n_steps 5000 --save_mesh {self.config.obj_output}", check = True, shell = True)
            logger.info(
                f"{bin_colors.SUCCESS}Model trained successfully!{bin_colors.ENDC}"
            )
            logger.info(
                f"{bin_colors.SUCCESS}Model successfully saved at {self.config.obj_output}{bin_colors.ENDC}"
            )
        except Exception as e:
            logger.error(
                f"{bin_colors.ERROR}Error while running model {e}{bin_colors.ENDC}"
            )
            raise e
