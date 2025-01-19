import warnings
warnings.filterwarnings("ignore")

import cv2
import os
from ultralytics import YOLO
from ultralytics import SAM
from PIL import Image
import numpy as np
import torch
from torch.cuda import is_available as gpu_ready

import sys
sys.path.append("../../GroundingDINO")
from groundingdino.util.inference import load_model, load_image, predict, annotate

from KoroKoro.utils import bin_colors, read_config
from KoroKoro.logger import logger
from KoroKoro.entity import ProductConfig
from KoroKoro.config.configuration import ConfigurationManager
from KoroKoro.utils.constants import CONFIG_FILE_PATH, COCO_NAMES

class DataTransformation:
  def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
    self.config_manager = ConfigurationManager(config_file_path)
    self.config = self.config_manager.get_config()
    self.YOLO_ = YOLO('yolov8x.pt')
    self.object_category = self.config.category
    self.object_desc = self.config.title
    self.object_index = COCO_NAMES[self.object_category] if self.object_category != 'others' else None
    self.root_data = self.config.colmap_output
    self.device = 'cuda' if gpu_ready() else 'cpu'
    self.folders = [
      f"{self.root_data}/images",
      # f"{self.root_data}/images_2",
      # f"{self.root_data}/images_4",
      # f"{self.root_data}/images_8",
    ]

    self.GROUNDING_DINO_BOX_TRESHOLD = 0.35
    self.GROUNDING_DINO_TEXT_TRESHOLD = 0.25

    self.groundingdino_model = load_model("../../GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py", "../../GroundingDINO/weights/groundingdino_swint_ogc.pth")

    self.SAM_ = SAM('sam_b.pt')
    

  def get_bbox_w_yolo(self, img_path: str):
    res = self.YOLO_.predict(img_path, classes = [self.object_index - 1], verbose = False)[0]
    return res.boxes.xyxy.cpu().numpy()[0] if len(res.boxes.data != 0) else None

  def get_bbox_w_groundingdino(self, img_path: str, text_prompt: str):
    _, image = load_image(img_path)
    boxes, _, _ = predict(
        model=self.groundingdino_model,
        image=image,
        caption=text_prompt,
        box_threshold=self.GROUNDING_DINO_BOX_TRESHOLD,
        text_threshold=self.GROUNDING_DINO_TEXT_TRESHOLD
    )
    return boxes[0] if len(boxes) != 0 else None

  def get_mask_w_sam(self, bbox, img_path: str):
    masks = self.SAM_(img_path, bboxes = bbox, verbose = False)[0].masks.data
    return masks[0].cpu().numpy() if len(masks != 0) else None

  def apply_mask_n_save(self, img_path: str, mask: np.ndarray):
    image = cv2.imread(img_path)
    resized_mask = cv2.resize(mask.astype(np.uint8), (image.shape[1], image.shape[0]), interpolation=cv2.INTER_AREA)
    masked_img = cv2.bitwise_and(image, image, mask = resized_mask)
    cv2.imwrite(img_path, masked_img)
    image = Image.open(img_path)
    image = image.convert("RGBA")
    data = image.getdata()
    new_data = []
    for item in data:
      if item[:3] == (0, 0, 0):
        new_data.append((0, 0, 0, 0))
      else:
        new_data.append(item)
    image.putdata(new_data)
    image.save(img_path, "PNG")

  def process_with_cv2(self, img_path: str):
    image = cv2.imread(img_path)
    image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret,baseline = cv2.threshold(image_grey,127,255,cv2.THRESH_TRUNC)
    ret,background = cv2.threshold(baseline,126,255,cv2.THRESH_BINARY)
    ret,foreground = cv2.threshold(baseline,126,255,cv2.THRESH_BINARY_INV)
    src = cv2.bitwise_and(image,image, mask=foreground)
    tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
    b, g, r = cv2.split(src)
    rgba = [b, g, r, alpha]
    dst = cv2.merge(rgba, 4)
    cv2.imwrite(img_path, dst)
  
  def transform_data(self) -> None:
    logger.info(f"{bin_colors.INFO}Further processing colmap output for {self.config.unique_id}{bin_colors.ENDC}")
    try:
      for folder in self.folders:
        for image_path in os.listdir(folder):
            if image_path.endswith(".png"):
              _image_path = os.path.join(folder, image_path)
              if self.object_index:
                bbox = self.get_bbox_w_yolo(_image_path)
                if bbox is not None:
                  logger.info(f"{bin_colors.OKCYAN}YOLO successfully detected {self.object_category} in {image_path} {bin_colors.ENDC}")
                  mask = self.get_mask_w_sam(bbox, _image_path)
                  self.apply_mask_n_save(_image_path, mask)
                  logger.info(f"{bin_colors.OKCYAN}SAM successfully segmented {self.object_category} in {image_path} {bin_colors.ENDC}")
                else: 
                  logger.info(f"{bin_colors.INFO}YOLO failed to detect, using GroundingDINO instead {bin_colors.ENDC}")
                  bbox = self.get_bbox_w_groundingdino(_image_path)
                  if bbox is not None:
                    logger.info(f"{bin_colors.OKCYAN}GroundingDINO successfully detected {self.object_category} in {image_path} {bin_colors.ENDC}") 
                    mask = self.get_mask_w_sam(bbox, _image_path)
                    self.apply_mask_n_save(_image_path, mask)
                    logger.info(f"{bin_colors.OKCYAN}SAM successfully segmented {self.object_category} in {image_path} {bin_colors.ENDC}")
                  else:
                    # TODO - Change this to use Trellis
                    logger.info(f"{bin_colors.INFO}YOLO and GroundingDINO failed to detect, applying OpenCV thresholding instead {bin_colors.ENDC}")
                    self.process_with_cv2(_image_path)
              else:
                bbox = self.get_bbox_w_groundingdino(_image_path)
                if bbox is not None:
                  logger.info(f"{bin_colors.OKCYAN}GroundingDINO successfully detected {self.object_desc} in {image_path} {bin_colors.ENDC}") 
                  mask = self.get_mask_w_sam(bbox, _image_path)
                  self.apply_mask_n_save(_image_path, mask)
                  logger.info(f"{bin_colors.OKCYAN}SAM successfully segmented {self.object_desc} in {image_path} {bin_colors.ENDC}")
                else:
                  # TODO - Change this to use Trellis
                  logger.info(f"{bin_colors.WARNING}Using CV2 to detect {self.object_desc.capitalize()} in {image_path}, may not be accurate{bin_colors.ENDC}")
                  self.process_with_cv2(_image_path)
    except Exception as e:
      logger.error(f"{bin_colors.ERROR}Error processing colmap output for {self.config.unique_id}{bin_colors.ENDC}")
      raise e
    logger.info(f"{bin_colors.SUCCESS}Further processing of {self.config.unique_id} completed!{bin_colors.ENDC}")

if __name__ == "__main__":
  DataTransformation().transform_data()
