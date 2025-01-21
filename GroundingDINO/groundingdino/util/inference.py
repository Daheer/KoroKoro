from typing import Tuple, List

import cv2
import numpy as np
import torch
from PIL import Image
from torchvision.ops import box_convert
import bisect

import groundingdino.datasets.transforms as T
from groundingdino.models import build_model
from groundingdino.util.misc import clean_state_dict
from groundingdino.util.slconfig import SLConfig
from groundingdino.util.utils import get_phrases_from_posmap

# ----------------------------------------------------------------------------------------------------------------------
# OLD API
# ----------------------------------------------------------------------------------------------------------------------


def preprocess_caption(caption: str) -> str:
    result = caption.lower().strip()
    if result.endswith("."):
        return result
    return result + "."


def load_model(
    model_config_path: str, model_checkpoint_path: str, device: str = "cuda"
):
    args = SLConfig.fromfile(model_config_path)
    args.device = device
    model = build_model(args)
    checkpoint = torch.load(model_checkpoint_path, map_location="cpu")
    model.load_state_dict(clean_state_dict(checkpoint["model"]), strict=False)
    model.eval()
    return model


def load_image(image_path: str) -> Tuple[np.array, torch.Tensor]:
    transform = T.Compose(
        [
            T.RandomResize([800], max_size=1333),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    image_source = Image.open(image_path).convert("RGB")
    image = np.asarray(image_source)
    image_transformed, _ = transform(image_source, None)
    return image, image_transformed


def predict(
    model,
    image: torch.Tensor,
    caption: str,
    box_threshold: float,
    text_threshold: float,
    device: str = "cuda",
    remove_combined: bool = False,
) -> Tuple[torch.Tensor, torch.Tensor, List[str]]:
    caption = preprocess_caption(caption=caption)

    model = model.to(device)
    image = image.to(device)

    with torch.no_grad():
        outputs = model(image[None], captions=[caption])

    prediction_logits = (
        outputs["pred_logits"].cpu().sigmoid()[0]
    )  # prediction_logits.shape = (nq, 256)
    prediction_boxes = outputs["pred_boxes"].cpu()[
        0
    ]  # prediction_boxes.shape = (nq, 4)

    mask = prediction_logits.max(dim=1)[0] > box_threshold
    logits = prediction_logits[mask]  # logits.shape = (n, 256)
    boxes = prediction_boxes[mask]  # boxes.shape = (n, 4)

    tokenizer = model.tokenizer
    tokenized = tokenizer(caption)

    if remove_combined:
        sep_idx = [
            i
            for i in range(len(tokenized["input_ids"]))
            if tokenized["input_ids"][i] in [101, 102, 1012]
        ]

        phrases = []
        for logit in logits:
            max_idx = logit.argmax()
            insert_idx = bisect.bisect_left(sep_idx, max_idx)
            right_idx = sep_idx[insert_idx]
            left_idx = sep_idx[insert_idx - 1]
            phrases.append(
                get_phrases_from_posmap(
                    logit > text_threshold, tokenized, tokenizer, left_idx, right_idx
                ).replace(".", "")
            )
    else:
        phrases = [
            get_phrases_from_posmap(
                logit > text_threshold, tokenized, tokenizer
            ).replace(".", "")
            for logit in logits
        ]

    return boxes, logits.max(dim=1)[0], phrases
