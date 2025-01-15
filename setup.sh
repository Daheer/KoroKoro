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

# Install system dependencies
sudo apt update
sudo apt install build-essential git ffmpeg python3-dev python3-pip libopenexr-dev libxi-dev libglfw3-dev libglew-dev libomp-dev libxinerama-dev libxcursor-dev
pip install --upgrade cmake

# Install additional requirements
pip install -r requirements.txt
gdown "https://drive.google.com/u/1/uc?id=1-7x7qQfB7bIw2zV4Lr6-yhvMpjXC84Q5&confirm=t" 
pip install tinycudann-1.7-cp310-cp310-linux_x86_64.whl 

# Create folder to store result .obj files
mkdir results
