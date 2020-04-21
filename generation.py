from models import start_session, restart_session, generate, load_model_into_graph
from dataset import get_random_prefix

def generate_texts(bot_name, session=None, checkpoint="latest", **generation_kwargs):
    if session is None:
        session = restart_session()
    load_model_into_graph(session, bot_name, checkpoint=checkpoint)
    texts = generate(session, bot_name, checkpoint=checkpoint, **generation_kwargs)
    return texts, session

