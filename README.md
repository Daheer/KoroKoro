# KoroKoro 👀

A novel to view products for sale!

https://github.com/Daheer/KoroKoro/assets/34832399/b78e3e87-4cf8-449f-9b87-ea39351f3cfa

## Introduction
Ever wished you could spice up your online shopping experience? With KoroKoro, sellers can casually snap a 360-degree video of their product, and voila, we turn it into a nifty 3D version. What makes KoroKoro chill is that it's all about showcasing products in this cool 3D space for a laid-back online shopping vibe. Check it out and add some playful zest to your e-commerce journey!
Welcome to the technical details of KoroKoro backend implementation.

For the front-end, check [here](https://github.com/Daheer/KoroKoro_Front_End)

## Prerequisites
- Docker
- NVIDIA Graphics Card
- Supabase
### OR 
- Google Colab
- Supabase

## Installation

### Option 1 - Self build

```
# Clone this repo
git clone https://github.com/KoroKoro.git
cd KoroKoro

# Build with docker
docker build -t korokoro:latest .

# Run image
docker run -it --gpus all korokoro:latest
```
Running the image will fetch products from the queue in Supabase and generate 3D models

### Option 2 - Image pull from Docker Hub

```
# Clone image from Docker Hub
docker pull daheer/korokoro:v0

# Run image
docker run -it --gpus all daheer/korokoro:v0
```

### Option 3 - Google Colab
```
!git clone https://github.com/KoroKoro.git 
```

#### Install condacolab

```
!pip install condacolab
```

```
import condacolab
condacolab.install()
```

#### Make conda commands available in shell

```
!sudo ln -s /opt/conda/root/etc/profile.d/conda.sh /etc/profile.d/conda.s
```

```
%cd KoroKoro
```

#### Install dependencies: InstantNGP, NerfStudio etc.

```
!bash setup.sh
```

#### Run stages 1 and 2 of the pipeline
```
%%shell 
eval "$(/usr/local/condabin/conda shell.bash hook)" 
conda activate korokoro 
python KoroKoro/pipeline/stage_01.py 
python KoroKoro/pipeline/stage_02.py
```

## Project Structure
```
📦KoroKoro
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
│  ├─ logging.py
│  ├─ pipeline
│  │  ├── __init__.py
│  │  ├── stage_01.py
│  │  └── stage_02.py
│  └─ utils
│     ├─ __init__.py
│     └─ constants.py
├─ config
│  └── config.yaml
├─ docker-compose.yml
├─ setup.py
└─ setup.sh
```

## Data Preparation
After recording a 360-degree video around a subject product, I leverage [NerfStudio's video-data processor](https://docs.nerf.studio/quickstart/custom_dataset.html#images-or-video) to generate a NeRF-compatible dataset. This dataset comprises extracted frames from the video and Colmap data, including the essential transforms.json file. This file encompasses rotation and translation data along with camera intrinsics, all crucial for NeRF rendering.

To isolate the subject object (pun intended), I use various techniques including [YOLOv8](https://github.com/ultralytics), [Segment-Anything(SAM)](https://segment-anything.com/), [OWL-ViT](https://huggingface.co/docs/transformers/model_doc/owlvit) & the more traditional [OpenCV](https://opencv.org/). See algorithm below

```
if object in coco_classes:
  detect_with_yolo()
  if successful():
    segment_with_sam()
  else:
    detect_with_owlvit()
    if successful():
      segment_with_sam()
    else:
      process_with_cv2()
else:
  detect_with_owlvit()
  if successful:
    segment_with_sam()
  else:
    process_with_cv2()
```

## Training / Rendering

I utilize [NVIDIA's Instant NGP](https://github.com/NVlabs/instant-ngp) to train and render a MLP with multiresolution hash input encoding using the tiny-cuda-nn framework and afterwards, save the resulting .obj file.

## Database

Supabase is the platform of choice due to it's rich features that allow for maximum productivity. 

### Sharding
Every product is assigned a unique_id which serves as a reference through out the system. I split every resulting .obj file into parts on the back-end to efficiently store them on KoroKoro's Supabase Bucket and piece the parts together in the front-end.

## Results

## Contributing

There are many areas where this project needs improvement. And I shall utilize weekends to have fun checking the following:
- [x] Lighterweight .obj files -> right now, the resulting obj models are heavy (> 100MB) and I have to use sharding to save them in Supabase's storage bucket which limits file uploads to 50MB

- [ ] Better quality models -> I'm still experimenting with multiple ways of performing Colmap to do better Sift Extraction and would welcome any help. I'm also looking at other NeRF render options

- [x] Use Segment Anything to improve segmentation

- [ ] More features on the frontend are always welcome if that's what you're into!

Please reach out to me @ suhayrid6@gmail.com, I'd be happy to walk you through the project, including the Supabase database configuration
