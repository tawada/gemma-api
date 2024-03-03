# Gemma API
This project provides an API wrapper around the Gemma model for natural language generation. It's built using FastAPI, and is designed to be easily deployable as a Docker container.

## Features
- Generate text based on a sequence of messages using the Gemma model.
- Docker support for easy deployment and scaling.
- Configurable model parameters and API settings through a JSON file.
- Authorization via API keys to secure access.

## Prerequisites
Before you can run the Gemma API, you need to have Docker installed on your machine. If you plan to run the API on a machine with GPUs, make sure Docker is set up to use them.

## Setup
Follow these steps to set up and run the Gemma API.

### 1. Build the Docker Image
First, build the Docker image for the Gemma API. You can tag it with the current date and time for versioning.

```bash
TAG=`date "+%Y%m%d-%H%M%S"`
DOCKER_URI=gemma-api:${TAG}

docker build -f Dockerfile ./ -t ${DOCKER_URI}
```

### 2. Download the Model File
Create a directory for the model checkpoints and download the Gemma model files into it. You'll need to obtain these files from the official Gemma or related sources.

```bash
mkdir -p ckpt
# Download the Gemma model checkpoints into the `ckpt` directory
```

### 3. Setup Configuration
Copy the configuration template to create your own configuration file. You'll need to edit `config.json` to set up API keys, model parameters, and other settings.

```bash
cp ./config/config.json.template ./config/config.json
# Edit config.json as needed
```

### 4. Run the API
Use the following command to run the Docker container with the Gemma API. Adjust the paths to your config and checkpoint directories as needed. If you're using a GPU, make sure Docker is configured to access it.

```bash
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

This command runs the API on port 8000. You can test it by sending a POST request to `/api/create-content` with a JSON body containing messages.

## API Reference
### POST /api/create-content
Generates text based on the provided sequence of messages.

**Request Body:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hello, Gemma!"
    },
    {
      "role": "model",
      "content": "Hello, how can I assist you today?"
    }
  ]
}
```

**Response:**
```json
{
  "content": "<Generated text>"
}
```

## Security
The Gemma API uses API keys for authorization. Be sure to include a valid API key in the `Authorization` header of your requests.

## License
Specify your license or that it's available as open-source.

## Acknowledgements
- Gemma PyTorch for the underlying model.
- FastAPI for the web framework.
