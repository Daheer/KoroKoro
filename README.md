# KoroKoro 👀

A novel to view products for sale!

## Getting Started
Welcome to the technical details of KoroKoro backend implementation.

For the front-end, check [here](https://github.com/KoroKoro_Front_End)

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
docker push daheer/korokoro:v0

# Run image
docker run -it --gpus all daheer/korokoro:v0
```

### Option 3 - Google Colab
> !git clone https://github.com/KoroKoro.git 

#### Install condacolab

> !pip install condacolab

> import condacolab <br> condacolab.install()

#### Make conda commands available in shell

> !sudo ln -s /opt/conda/root/etc/profile.d/conda.sh /etc/profile.d/conda.s

> %cd KoroKoro

#### Install dependencies: InstantNGP, NerfStudio etc.

> !bash setup.sh

#### Run stages 1 and 2 of the pipeline
> %%shell <br> 
eval "$(/usr/local/condabin/conda shell.bash hook)" <br> 
conda activate korokoro <br>
python KoroKoro/pipeline/stage_01.py <br>
python KoroKoro/pipeline/stage_02.py

## Project Structure
```
.
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

To refine the dataset further, I employ YOLOv8 from [Ultralytics](https://github.com/ultralytics) for pixel segmentation related to the subject product, particularly if the object falls under the COCO Dataset classes. In cases where the object is not part of COCO Dataset classes, I resort to a more traditional approach, utilizing OpenCV to precisely segment out the object.

## Training / Rendering

I utilize [NVIDIA's Instant NGP](https://github.com/NVlabs/instant-ngp) to train and render a MLP with multiresolution hash input encoding using the tiny-cuda-nn framework and afterwards, save the resulting .obj file.

## Results

## Contributing

There are many areas where this project needs improvement. And I shall utilize weekends to have fun checking the following:
- [ ] Lighterweight .obj files -> right now, the resulting obj models are heavy (> 100MB) and I have to use sharding to save them in Supabase's storage bucket which limits file uploads to 50MB

- [ ] Better quality models -> I'm still experimenting with multiple ways of performing Colmap to do better Sift Extraction and would welcome any help. I'm also looking at other NeRF render options

- [ ] More features on the frontend are always welcome if that's what you're into!