#!/bin/bash

# Make sure conda is installed
source /path/to/your/conda/bin/activate

# Create conda environment
conda create --name korokoro -y python=3.10
source /path/to/your/conda/bin/activate korokoro

# Install cuda dependencies
conda install -c "nvidia/label/cuda-12.1.0" cuda-toolkit -y
conda install -c conda-forge colmap -y

# Install additional requirements
pip install -r requirements.txt
gdown "https://drive.google.com/u/1/uc?id=1-7x7qQfB7bIw2zV4Lr6-yhvMpjXC84Q5&confirm=t" 
pip install tinycudann-1.7-cp310-cp310-linux_x86_64.whl 

# Install system dependencies
apt update && apt install build-essential git python3-dev python3-pip libopenexr-dev libxi-dev libglfw3-dev libglew-dev libomp-dev libxinerama-dev libxcursor-dev
pip install --upgrade cmake

# Clone and build instant-ngp
git clone --recursive https://github.com/nvlabs/instant-ngp
cd instant-ngp
cmake . -B build -DNGP_BUILD_WITH_GUI=OFF
cmake --build build --config RelWithDebInfo -j `nproc`
pip3 install -r requirements.txt

# Create folder to store result .obj files
mkdir results