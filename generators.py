import contextlib
import random

import numpy as np
import torch
from gemma import config as gemma_config
from gemma import model as gemma_model

import schemas
from apps import config

CHAT_TEMPLATE = "<start_of_turn>{role}\n{prompt}<end_of_turn>\n"
MODEL_START = "<start_of_turn>model\n"
MODEL_END = "<end_of_turn>"


@contextlib.contextmanager
def _set_default_tensor_type(dtype: torch.dtype):
    """Sets the default torch dtype to the given dtype."""
    torch.set_default_dtype(dtype)
    yield
    torch.set_default_dtype(torch.float)


def generate(messages: list[schemas.Message]):
    variant = config.variant
    ckpt_path = config.ckpt_path
    device = config.device
    model_config = gemma_config.get_model_config(variant)
    model_config.dtype = "float32" if device == "cpu" else "float16"
    model_config.dtype = config.tensor_dtype or model_config.dtype
    model_config.quant = False
    device = torch.device(device)
    with _set_default_tensor_type(model_config.get_dtype()):
        model = gemma_model.GemmaForCausalLM(model_config)
        model.load_weights(ckpt_path)
        model = model.to(device).eval()
    origin_prompt = format_prompt(messages)

    prompt = origin_prompt
    full_result = ""

    for _ in range(3):
        result = model.generate(
            prompt,
            device=device,
            output_len=config.output_len,
        )
        if MODEL_END in result:
            full_result += result.split(MODEL_END)[0]
            break
        else:
            full_result += result
            prompt = origin_prompt + full_result
            continue
    return full_result


def format_prompt(messages: list[schemas.Message]):
    prompt = ""
    for message in messages:
        prompt += f"{message.role}: {message.content}\n"
    prompt += MODEL_START
    return prompt
