import gpt_2_simple as gpt2
import os
from tensorflow.python.framework import ops
from model_path import get_checkpoint_name
from model_path import SAMPLE_DIR, MODEL_DIR, MODEL_NAME, CHECKPOINT_DIR

def restart_session():
    ops.reset_default_graph()
    session = gpt2.start_tf_sess()
    return session

def start_session():
    session = gpt2.start_tf_sess()
    return session

def load_model_into_graph(session, bot_name, checkpoint="latest", sample_dir=SAMPLE_DIR, model_dir=MODEL_DIR, model_name=MODEL_NAME, checkpoint_dir=CHECKPOINT_DIR):
    run_name = bot_name
    checkpoint = get_checkpoint_name(checkpoint, checkpoint_dir, bot_name)
    gpt2.load_gpt2(session,
                   run_name=run_name,
                   checkpoint_dir=checkpoint_dir,
                   model_name=None, # To use checkpoint path. This parameter is ambiguous in gpt-2-simple.
                   model_dir=model_dir,
                   checkpoint=checkpoint)

def generate(session, bot_name, checkpoint="latest", sample_dir=SAMPLE_DIR, model_dir=MODEL_DIR, model_name=MODEL_NAME, checkpoint_dir=CHECKPOINT_DIR, **generate_kwargs):
    checkpoint = get_checkpoint_name(checkpoint, checkpoint_dir, bot_name)
    run_name = bot_name
    model_path = os.path.join(model_dir, model_name)    
    texts = gpt2.generate(session,
                          run_name=run_name,
                          checkpoint_dir=checkpoint_dir,
                          model_name=model_path,
                          model_dir=model_dir,
                          sample_dir=sample_dir,
                          return_as_list=True,
                          prefix=generate_kwargs["prefix"] if "prefix" in generate_kwargs else None,
                          seed=generate_kwargs["seed"] if "seed" in generate_kwargs else None,
                          nsamples=generate_kwargs["nsamples"] if "nsamples" in generate_kwargs else 1,
                          batch_size=generate_kwargs["batch_size"] if "batch_size" in generate_kwargs else 1,
                          length=generate_kwargs["length"] if "length" in generate_kwargs else 100,
                          temperature=generate_kwargs["temperature"] if "temperature" in generate_kwargs else 0.7,
                          top_k=generate_kwargs["top_k"] if "top_k" in generate_kwargs else 40,
                          top_p=generate_kwargs["top_p"] if "top_p" in generate_kwargs else 0.0)
    return texts
