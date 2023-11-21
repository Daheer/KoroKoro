FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04 AS build-image

ENV QT_XCB_GL_INTEGRATION=offscreen
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    cmake \
    ninja-build \
    build-essential \
    libboost-program-options-dev \
    libboost-filesystem-dev \
    libboost-graph-dev \
    libboost-system-dev \
    libeigen3-dev \
    libflann-dev \
    libfreeimage-dev \
    libmetis-dev \
    libgoogle-glog-dev \
    libgtest-dev \
    libsqlite3-dev \
    libglew-dev \
    qtbase5-dev \
    libqt5opengl5-dev \
    libcgal-dev \
    libceres-dev

WORKDIR /KoroKoro

COPY . .

RUN git clone https://github.com/clintlombard/colmap.git
RUN cd colmap && \
    git fetch https://github.com/clintlombard/colmap.git 0aee40de52e378aee96147f2df4c54e44b2b3e8a && \
    git checkout FETCH_HEAD && \
    mkdir build && \
    cd build && \
    cmake .. -GNinja -DCMAKE_CUDA_ARCHITECTURES=native && \
    ninja && \
    ninja install && \
    cd .. && rm -rf colmap && cd ..

RUN apt-get install -y build-essential git ffmpeg python3-dev python3-pip libopenexr-dev libxi-dev libglfw3-dev libglew-dev libomp-dev libxinerama-dev libxcursor-dev

ENV QT_QPA_PLATFORM=offscreen
ENV PATH="/opt/conda/bin:${PATH}" 

RUN apt-get update && \
    apt-get install -y wget && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh
    
RUN eval "$($(which conda) shell.bash hook)" && \
    conda create --name korokoro -y python=3.10 && \
    conda init bash && \
    conda activate korokoro && \
    pip3 install --upgrade cmake && \
    pip3 install -r requirements.txt && \
    gdown "https://drive.google.com/u/1/uc?id=1-7x7qQfB7bIw2zV4Lr6-yhvMpjXC84Q5&confirm=t" && \
    pip install tinycudann-1.7-cp310-cp310-linux_x86_64.whl && \
    git clone --recursive https://github.com/nvlabs/instant-ngp && \
    cd instant-ngp && \
    cmake . -B build -DNGP_BUILD_WITH_GUI=OFF && \
    cmake --build build --config RelWithDebInfo -j $(nproc) && \
    pip3 install -r requirements.txt && \
    apt install libxcb-* -y && \
    mkdir results && \
    cd ..

# pip3 uninstall opencv-python -y && \
# pip3 install opencv-python-headless 
# conda install -c conda-forge colmap -y && \
    

CMD conda run --no-capture-output -n korokoro python3 KoroKoro/pipeline/stage_01.py && \
    conda run --no-capture-output -n korokoro python3 KoroKoro/pipeline/stage_02.py
