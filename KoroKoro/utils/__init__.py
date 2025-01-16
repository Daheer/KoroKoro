from typing import List, Dict, Any
import yaml
from pathlib import Path
from ensure import ensure_annotations
from box import ConfigBox
import os
import random
import cv2

from KoroKoro.logger import logger


def sort_product_listings(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return sorted(
        data,
        key=lambda x: {"IDLE": 1, "FAILED": 2, "PROCESSING": 3, "DONE": 4}.get(
            x["status"], float("inf")
        ),
    )


class bin_colors:
    HEADER = "\033[95m"
    INFO = "\033[94m"
    OKCYAN = "\033[96m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def save_config(config: Dict[str, str], file_path: Path) -> None:
    """
    Save a dictionary to a yaml file.
    """
    try:
        with open(file_path, "w") as file:
            yaml.dump(config, file)
            logger.info(
                f"{bin_colors.INFO}{file_path} saved successfully.{bin_colors.ENDC}"
            )
    except Exception as e:
        logger.error(
            f"{bin_colors.ERROR}Error saving yaml file at {file_path}.{bin_colors.ENDC}"
        )
        raise e


@ensure_annotations
def read_config(path_to_yaml: Path) -> ConfigBox:
    """
    Read a yaml file and return a ConfigBox object.
    """
    try:
        with open(path_to_yaml, "r") as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)
            logger.info(
                f"{bin_colors.INFO}{yaml_file.name} read successfully.{bin_colors.ENDC}"
            )
            return ConfigBox(yaml_dict)
    except Exception as e:
        logger.error(
            f"{bin_colors.ERROR}Error reading yaml file at {path_to_yaml}.{bin_colors.ENDC}"
        )
        raise e


def create_directory(path: Path) -> None:
    """
    Create a directory if it does not exist.
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            logger.info(
                f"{bin_colors.INFO}Directory created at {path}.{bin_colors.ENDC}"
            )
    except Exception as e:
        logger.error(
            f"{bin_colors.ERROR}Error creating directory at {path}.{bin_colors.ENDC}"
        )
        raise e


def split_obj_file(
    input_obj_path: Path, output_path: Path, lines_per_part: int = 1000000
) -> None:
    """
    Split the resulting obj file into multiple parts.
    """
    try:
        logger.info(
            f"{bin_colors.INFO}Splitting {input_obj_path} into parts.{bin_colors.ENDC}"
        )
        n_splits = 0
        with open(input_obj_path, "r") as input_file:
            part_number = 1
            line_count = 0

            os.makedirs(output_path, exist_ok=True)

            output_file_path = os.path.join(output_path, f"part{part_number}.txt")

            with open(output_file_path, "w") as output_file:
                for line in input_file:
                    output_file.write(line)
                    line_count += 1

                    if line_count >= lines_per_part:
                        line_count = 0
                        part_number += 1
                        output_file_path = os.path.join(
                            output_path, f"part{part_number}.txt"
                        )
                        output_file.close()
                        output_file = open(output_file_path, "w")

            n_splits = part_number

        logger.info(
            f"{bin_colors.INFO}Done splitting {input_obj_path} into {n_splits} parts.{bin_colors.ENDC}"
        )
    except Exception as e:
        logger.error(
            f"{bin_colors.ERROR}Error splitting obj file at {input_obj_path}.{bin_colors.ENDC}"
        )
        raise e


def stitch_obj_files(output_path: Path, output_obj_path: Path):
    pass


def extract_frames(video_path, num_frames=20):
    """
    Randomly sample frames from the input video.

    Args:
        num_frames (int, optional): Number of frames to extract. Defaults to 20.
    """
    logger.info(
        f"{bin_colors.INFO}Extracting {num_frames} from {video_path}.{bin_colors.ENDC}"
    )
    cap = cv2.VideoCapture(video_path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames < num_frames:
        logger.error(
            f"{bin_colors.ERROR}Video has fewer frames than the requested number..{bin_colors.ENDC}"
        )
        raise ValueError("Video has fewer frames than the requested number.")

    frame_indices = sorted(random.sample(range(total_frames), num_frames))

    for i, frame_num in enumerate(frame_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

        ret, frame = cap.read()
        if ret:
            output_filename = os.path.join(f"{video_path}/frames", f"{i:04d}.png")
            cv2.imwrite(output_filename, frame)

    cap.release()

    logger.info(
        f"{bin_colors.INFO}Done extracting frames from {video_path}.{bin_colors.ENDC}"
    )
