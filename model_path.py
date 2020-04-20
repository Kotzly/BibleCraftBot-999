import json
import os
import re
from os.path import join

with open("config.json", "r") as json_file:
    config = json.load(json_file)

SAMPLE_DIR = config["sample_dir"]
MODEL_DIR = config["model_dir"]
MODEL_NAME = config["model_name"]
CHECKPOINT_DIR = config["checkpoint_dir"]

def get_epoch_from_model_name(name):
    return int(re.search("\-([0-9]+)\.", name).group(1))

def get_checkpoints(folder):
    files = os.listdir(folder)
    model_files = [file for file in files if file.endswith(".meta")]
    epochs = [get_epoch_from_model_name(model_file) for model_file in model_files]
    return epochs

def get_latest_checkpoint(folder):
    epochs = get_checkpoints(folder)
    return max(epochs)

def get_checkpoint_name(checkpoint, checkpoint_dir, bot_name):
    if checkpoint == "latest":
        checkpoint = get_latest_checkpoint(join(checkpoint_dir, bot_name))
    elif isinstance(checkpoint, int):
        checkpoint = str(checkpoint)
    checkpoint = "model-{}".format(checkpoint)
    return checkpoint
