from dataclasses import dataclass
from pathlib import Path
from typing import Dict


class ProductConfig:
    id: int
    title: str
    category: str
    price: int
    video_link: str
    image_link: str
    status: str
    unique_id: str
    output_dir: Path = Path("artifacts")
    video_output: Path
    frames_path: Path
    colmap_output: Path
    obj_output: Path

    def __init__(
        self,
        id: int,
        title: str,
        category: str,
        price: int,
        video_link: str,
        image_link: str,
        status: str,
        unique_id: str,
    ):
        self.id = id
        self.title = title
        self.category = category
        self.price = price
        self.video_link = video_link
        self.image_link = image_link
        self.status = status
        self.unique_id = unique_id
        self.video_output = f"{self.output_dir}/{self.unique_id}.mp4"
        self.colmap_output = f"{self.output_dir}/{self.unique_id}"
        self.frames_path = f"{self.output_dir}/{self.unique_id}/frames"
        self.obj_output = f"{self.output_dir}/{self.unique_id}.obj"

    @classmethod
    def from_dict(cls, data: Dict[str, str]):
        return cls(
            id=data["id"],
            title=data["title"],
            category=data["category"],
            price=data["price"],
            video_link=data["video_link"],
            image_link=data["image_link"],
            status=data["status"],
            unique_id=data["unique_id"],
        )

    @classmethod
    def from_yaml_file(cls, path: str):
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)
