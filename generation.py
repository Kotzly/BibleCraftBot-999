from models import start_session, restart_session, generate, load_model_into_graph
from dataset import get_random_prefix

def generate_texts(bot, session=None, random_prefix=True, prefix_from_dataset=False, **generation_kwargs):
    if session is None:
        session = restart_session()
    load_model_into_graph(session, bot["name"], checkpoint=bot["default_checkpoint"])
    # get_random_prefix(bot["dataset"], length=10)
    texts = generate(session, bot["name"], checkpoint=bot["default_checkpoint"], **generation_kwargs)
    return texts, session

