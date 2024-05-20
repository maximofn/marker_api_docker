FROM nvcr.io/nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

RUN apt-get update \
    && apt-get install -y git git-lfs python3 python3-pip \
    && curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash \
    && git lfs install \
    && rm cuda-keyring_1.0-1_all.deb \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

RUN apt-get update \
    && apt-get install -y libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 https://github.com/adithya-s-k/marker-api \
    && cd marker-api && pip3 install --no-cache-dir -e . 

WORKDIR /marker-api