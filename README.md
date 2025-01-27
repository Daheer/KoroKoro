# KoroKoro 👀

KoroKoro is an automated pipeline for converting 2D videos into detailed 3D models using advanced techniques.

## Introduction

KoroKoro uses a mix of advanced deep learning techniques to convert 30-second videos around an object to a fully interactive 3D object.

View live demo [here](https://daheer.github.io/korokoro-web-v2)

## How does it work?
![korokoro-proecess](https://github.com/user-attachments/assets/e68ff034-fae4-4e54-8bcc-88be92c7a4a3)
#### Video Ingestion & Processing

Given an input video, 40 frames are extracted [default, can be changed in [extract_frames](KoroKoro/utils/__init__.py)], these 40 frames are processed using the process_data method in [DataProcessing](KoroKoro/components/data_processing.py) class to generate a NeRF-compatible dataset that includes a `transforms.json` file.

#### Image Transformation

Given a frame, if the `object of interest` is among the [80 COCO classes](https://cocodataset.org/), [YOLOv8](https://yolov8.com/) predicts the bounding box coordinates of the object otherwise [GroundingDINO](https://github.com/IDEA-Research/GroundingDINO) handles the bounding box prediction taking a natural language prompt — the description/title of the object. This title is set in [config/config.yaml](config/config.yaml).

Given a frame and the `xy` coordinates of the bounding box around the object, [SegmentAnythingv2](https://segment-anything.com/) creates an accurate mask of the object, the mask is then used to extract only the object leaving the other areas/background empty.

See algorithm below

```
if object in coco_classes:
  detect_with_yolov8()
  if successful():
    segment_with_sam2()
  else:
    detect_with_groundingdino()
    if successful():
      segment_with_sam2()
else:
  detect_with_groundingdino()
  if successful:
    segment_with_sam()
```

#### 3D Reconstruction

Processed inputs from the previous steps are fed to Nerfstudio's implementation of Gaussian Splat — [splatfacto](https://docs.nerf.studio/nerfology/methods/splat.html).

The resulting splats are finally exported to a `.ply` file

## Prerequisites

- Conda / Miniconda

NB: Tested on GPU compute with A10 (24GB) & Google Colab T4 (16GB)

## Installation

### Install conda if not installed

```
sudo apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6

curl -sL \
  "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh" > \
  "Miniconda3.sh"

bash Miniconda3.sh

source /root/miniconda3/bin/activate
```

### General setup
```
git clone https://github.com/KoroKoro.git
cd KoroKoro

# This will setup the environment
bash setup.sh

# Activate the environment
conda activate korokoro
```

#### Run Locally 

Configure the `category`, `title` & `video_output` fields in [config.yaml](config/config.yaml)

- `category`: MS COCO class name if available e.g. `book`, otherwise set to `others`
- `title`: natural language of the object e.g. `blue backpack`
- `video_output`: path to the input video

Run local pipeline
```bash
python KoroKoro/pipeline/local.py
```

#### Run with Supabase Database Connection

Simply run the command below, it will fetch products from the queue in Supabase and generate 3D models

```bash
python KoroKoro/pipeline/stage_01.py
python KoroKoro/pipeline/stage_02.py
```

### Google Colab

Install xterm

```
!pip install colab-xterm
```

Launch xterm
```
%load_ext colabxterm
```

Continue from [start of Installation instructions](#installation)

## Project Structure
```
📦KoroKoro
├─ .gitignore
├─ Dockerfile
├─ KoroKoro
│  ├─ __init__.py
│  ├─ components
│  │  ├─ __init__.py
│  │  ├─ data_ingestion.py
│  │  ├─ data_processing.py
│  │  ├─ data_transformation.py
│  │  ├─ initialization.py
│  │  ├─ model_trainer.py
│  │  └─ post_processing.py
│  ├─ config
│  │  ├─ __init__.py
│  │  └─ configuration.py
│  ├─ entity
│  │  └── __init__.py
│  ├─ logger.py
│  ├─ pipeline
│  │  ├── __init__.py
│  │  ├── local.py
│  │  ├── stage_01.py
│  │  └── stage_02.py
│  └─ utils
│     ├─ __init__.py
│     └─ constants.py
├─ GroundingDINO
│  ├─ groundingdino
│  │  ├─ __init__.py
│  │  ├─ config
│  │  ├─ datasets
│  │  ├─ models
│  │  └─ util
│  ├─ LICENSE
├─ config
│  └── config.yaml
├─ docker-compose.yml
├─ README.md
├─ requirements.txt
├─ setup.py
└─ setup.sh
```

## Improvements from v1 to v2

| Input | KoroKoro Version 1 | KoroKoro Version 2 |
|----------|----------|----------|
| ![chair](https://github.com/user-attachments/assets/7a1162f3-b01b-44d6-981c-e0b6707e0e08) | ![result-v1](https://github.com/user-attachments/assets/a3ea73bf-adcb-4803-83e0-06b7594bcdf0) | ![result-v2](https://github.com/user-attachments/assets/d4228198-dc0c-40cf-8594-503be5d81ffe) |
| Setup Time | 45 minutes | 15 minutes |
| Processing Time | 25 minutes | 5 minutes |
| Training Time | 5 minutes | 5 minutes |
## Contributing

There are areas where this project can be improved including

- [ ] Incorporate Trellis 


- [x] Lighterweight .obj files -> right now, the resulting obj models are heavy (> 100MB) and I have to use sharding to save them in Supabase's storage bucket which limits file uploads to 50MB

- [x] Use Segment Anything to improve segmentation

Please reach out to me @ suhayrid6@gmail.com, I'd be happy to walk you through the project, including the Supabase database configuration
