import os

from KoroKoro.components.data_processing import DataProcessing

from KoroKoro.utils import bin_colors, read_config, save_config
from KoroKoro.utils.constants import CONFIG_FILE_PATH, GROUNDING_DINO_PATH
from KoroKoro.logger import logger

import sys

sys.path.append(GROUNDING_DINO_PATH)

from KoroKoro.components.data_transformation import DataTransformation
from KoroKoro.components.model_trainer import ModelTrainer

config = read_config(CONFIG_FILE_PATH)
config.unique_id = config.video_output.split("/")[-1].split(".")[0]
save_config(dict(config), CONFIG_FILE_PATH)

try:
    logger.info(f"{bin_colors.INFO}Starting reconstruction pipeline{bin_colors.ENDC}")
    config = read_config(CONFIG_FILE_PATH)

    DataProcessing().process_data()
    logger.info(
        f"{bin_colors.SUCCESS}Stage 01 of reconstruction pipeline executed successfully!{bin_colors.ENDC}"
    )
    DataTransformation().transform_data()
    ModelTrainer().train_model()
    logger.info(
        f"{bin_colors.SUCCESS} Congratulations! Your 3D asset can be found at {os.path.join(config.output_dir, config.unique_id, 'splat.ply')} {bin_colors.ENDC}"
    )
    logger.info(
        f"{bin_colors.SUCCESS}Stage 02 of reconstruction pipeline executed successfully!{bin_colors.ENDC}"
    )

except Exception as e:
    logger.error(
        f"{bin_colors.ERROR}Error while running pipeline: {e}{bin_colors.ENDC}"
    )
    raise e
finally:
    config = read_config(CONFIG_FILE_PATH)
    if not os.path.exists(f"artifacts/{config.unique_id}/splat.ply"):
        logger.error(f"{bin_colors.ERROR}Error while running pipeline{bin_colors.ENDC}")
