import schedule    
from models import start_session, restart_session
import facebook
import json
from generation import generate_texts
from models import restart_session
from bots import BIBLEBOT, BIBLECRAFTBOT, LOVECRAFTBOT, QURANBOT
import time
from datetime import datetime as dt

def get_tokens():
    with open("token.json", "r") as json_file:
        tokens = json.load(json_file)
    return tokens

def any_element_in(elements, obj):
    for element in elements:
        if element.lower() in obj.lower():
            return True
    return False

def get_forbidden_words():
    with open("forbidden.json", "r") as file:
        content = json.load(file)
        forbidden_words = content["words"]
    return forbidden_words

# bots = [BIBLECRAFTBOT, QURANBOT, LOVECRAFTBOT, BIBLEBOT]
bots = [QURANBOT, LOVECRAFTBOT, BIBLEBOT]
bots_texts = {bot["name"]:[] for bot in bots}

def job():
    global bots, bots_texts
    session = None
    for bot in bots:
        tokens = get_tokens()
        bot_name = bot["name"]
        if len(bots_texts[bot_name]) == 0:
            texts, _ = generate_texts(bot, session, top_k=30, temperature=.75, nsamples=48)
            forbidden_words = get_forbidden_words()
            texts = [x for x in texts if not any_element_in(forbidden_words, x)]
            bots_texts[bot_name] = texts
            print("GENERATED", len(texts), "TEXTS FOR", bot_name)
        graph = facebook.GraphAPI(tokens[bot_name])
        message = bot["template"].format(bots_texts[bot_name].pop())
        try:
            post = graph.put_object(parent_object='me', message=message, connection_name="feed")
            print(f"({len(bots_texts[bot_name])+1}/300) POST FOR", bot_name,"\nID: {}".format(post["id"]), "\nMessage:", message)
        except Exception as e:
            print("ERROR POSTING FOR", bot_name, "at", dt.now().isoformat(), str(e))
    restart_session()

def start(delay, batch=100):
    schedule.every().hour.at(":54").do(job)
    # schedule.every(5).seconds.do(job).run()
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start(delay=None)
