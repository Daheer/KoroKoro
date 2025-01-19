#!/bin/bash

# Create conda environment

# Activate conda environment
CONDA_BASE=$(which conda)
eval "$($CONDA_BASE shell.bash hook)"
conda create --name korokoro -y python=3.10
conda activate korokoro

# Install cuda dependencies
conda install -c "nvidia/label/cuda-11.8.0" cuda-toolkit -y
conda install -c conda-forge colmap==3.8 -y

gdown "https://drive.google.com/u/1/uc?id=1-7x7qQfB7bIw2zV4Lr6-yhvMpjXC84Q5&confirm=t" 
pip install tinycudann-1.7-cp310-cp310-linux_x86_64.whl 

# Setup Grounding DINO
git clone https://github.com/IDEA-Research/GroundingDINO.git
cd GroundingDINO/
pip install -e .

mkdir weights
cd weights
wget -q https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth
cd ../..

# Install additional requirements
pip install -r requirements.txt

# Create folder to store result .obj files
mkdir results
