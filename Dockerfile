# This file is based on https://github.com/google/gemma_pytorch/blob/main/docker/Dockerfile
#
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM pytorch/pytorch:2.1.2-cuda11.8-cudnn8-runtime

USER root

# Install tools.
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y --no-install-recommends curl
RUN apt-get install -y --no-install-recommends wget
RUN apt-get install -y --no-install-recommends git

# Install libraries.
ENV PIP_ROOT_USER_ACTION=ignore
RUN python -m pip install --upgrade pip
RUN pip install fairscale==0.4.13
RUN pip install numpy==1.24.4
RUN pip install immutabledict==4.1.0
RUN pip install sentencepiece==0.1.99
RUN pip install fastapi
RUN pip install uvicorn

# Install from source.
WORKDIR /workspace/
RUN git clone https://github.com/google/gemma_pytorch.git
RUN pip install -e gemma_pytorch
COPY . /workspace/gemma_pytorch/
WORKDIR /workspace/gemma_pytorch/

EXPOSE 8000
