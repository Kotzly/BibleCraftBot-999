import schedule    
from models import start_session, restart_session
import facebook
import json
from generation import generate_texts
from models import restart_session
import time
from datetime import datetime as dt
from bots import QuranBot, BibleBot, LoveCraftBot
import warnings

warnings.filterwarnings("ignore")

bots = [QuranBot(post=True), LoveCraftBot(post=True), BibleBot(post=True)]

def post():
    for bot in bots:
        bot.post()
    restart_session()

def create():
    for bot in bots:
        bot.buffer_texts(nsamples=48, length=75, temperature=0.75, top_k=35)
    restart_session()

def start(delay, batch=100):
    schedule.every().hour.at(":18").do(create)
    schedule.every().hour.at(":38").do(post)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start(delay=None)
