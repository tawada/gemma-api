# gemma-api
Fast API wrapper for gemma_pytorch

## Build the docker image.
```
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

docker run -t --rm \
    --gpus all \
    -v ${CNFG_PATH}:/tmp/config \
    -v ${CKPT_PATH}:/tmp/ckpt \
    ${DOCKER_URI} \
    python uvicorn main:app
```
