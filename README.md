# gemma-api
Fast API wrapper for gemma_pytorch

## Build the docker image.
```
TAG=`date "+%Y%m%d-%H%M%S"`
DOCKER_URI=gemma-api:${TAG}

docker build -f Dockerfile ./ -t ${DOCKER_URI}
```

## Setup config
```
mkdir config
cp ./config/config.json.template ./config/config.json
```

## Run API
```
CNFG_PATH=./config
CKPT_PATH=./ckpt

docker run -it --rm \
    --gpus all \
    -v ${CNFG_PATH}:/tmp/config \
    -v ${CKPT_PATH}:/tmp/ckpt \
    -p 8000:8000 \
    ${DOCKER_URI} \
    uvicorn main:app --host 0.0.0.0
```
