# Use an official PyTorch image based on CUDA                                                                        
FROM nvidia/cuda:11.2.2-cudnn8-devel-ubuntu20.04 AS build-image                                                      
                                                                                                                     
# Set the working directory in the container                                                                         
WORKDIR /KoroKoro

# Copy the current directory contents into the container at /KoroKoro
COPY . .

# Install Miniconda
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

ENV DEBIAN_FRONTEND=noninteractive 

# Add conda to PATH and create the conda environment
ENV PATH="/opt/conda/bin:${PATH}"
RUN conda create --name korokoro -y python=3.10 && \
    conda init bash

# Activate the conda environment and install dependencies
# SHELL ["/bin/bash", "-c"]
RUN CONDA_BASE=$(which conda) && \
    eval "$($CONDA_BASE shell.bash hook)" && \
    conda activate korokoro && \
    # conda install -c "nvidia/label/cuda-12.1.0" cuda-toolkit -y && \
    # conda install -c conda-forge colmap -y && \
    apt install colmap -y && \
    apt-get update && \
    apt-get install -y build-essential git ffmpeg python3-dev python3-pip libopenexr-dev libxi-dev libglfw3-dev libglew-dev libomp-dev libxinerama-dev libxcursor-dev && \
    pip install --upgrade cmake && \
    pip install -r requirements.txt && \
    gdown "https://drive.google.com/u/1/uc?id=1-7x7qQfB7bIw2zV4Lr6-yhvMpjXC84Q5&confirm=t" && \
    pip install tinycudann-1.7-cp310-cp310-linux_x86_64.whl && \
    git clone --recursive https://github.com/nvlabs/instant-ngp && \
    cd instant-ngp && \
    cmake . -B build -DNGP_BUILD_WITH_GUI=OFF && \
    cmake --build build --config RelWithDebInfo -j `nproc` && \
    pip3 install -r requirements.txt && \
    cd ..

# Create folder to store result .obj files
#RUN mkdir results

#RUN setup.sh

# Run Stage 01
RUN ["conda", "run", "--no-capture-output", "-n", "korokoro", "python", "KoroKoro/pipeline/stage_01.py"]

# Run Stage 02
CMD ["conda", "run", "--no-capture-output", "-n", "korokoro", "python", "KoroKoro/pipeline/stage_02.py"]
