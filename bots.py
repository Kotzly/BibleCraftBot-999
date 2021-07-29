from abc import ABC, abstractmethod
from generation import generate_texts
import facebook
import json
import numpy as np
import re
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

def get_forbidden_words(forbidden_json="forbidden.json"):
    with open(forbidden_json, "r") as file:
        content = json.load(file)
        forbidden_words = content["words"]
    return forbidden_words

class GPT2Bot(ABC):

    def __init__(self, name="Bot", checkpoint="latest", post_to_facebook=True, **generation_kwargs):
        self.generation_kwargs = generation_kwargs
        self.name = name
        self.checkpoint = checkpoint
        self.texts = []
        self.post_to_facebook = post_to_facebook
        self.min_post_size = 50
        try:
            self.token = get_tokens()[name]
        except:
            self.post_to_facebook = False
            print(f"No token found for {name}. Bot will not post to facebook.")
        print(f"Create bot {name} with\n{generation_kwargs}")

    def generate_texts(self, **generation_kwargs):
        texts, _ = generate_texts(self.name, 
                                    checkpoint=self.checkpoint,
                                    **generation_kwargs)
        return texts

    def clean_texts(self, texts=[]):
        if not texts:
            texts = self.texts
        forbidden_words = get_forbidden_words()
        texts = [x for x in texts if not any_element_in(forbidden_words, x)]
        return texts

    @abstractmethod
    def format_text(self, text):
        return text

    def buffer_texts(self, force=False, **generation_kwargs):
        if not generation_kwargs: generation_kwargs = self.generation_kwargs
        if not self.texts or force:
            texts = self.generate_texts(**generation_kwargs)
            self.texts = self.clean_texts(texts)
            print("CREATED {} TEXTS FOR {}".format(len(texts), self.name))
        
    def get_text(self):
        if not self.texts:
            self.buffer_texts(self.generation_kwargs)
        return self.texts.pop()

    def get_post_text(self):
        text = ""
        while len(text) < self.min_post_size:
            text = self.format_text(self.get_text())
        return text

    def buffer_images(self, *args, **kwargs):
        pass

    def get_image(self):
        return None
    
    def format_image(self, image):
        if image is None:
            return None
        return image

    def get_post_image(self):
        return None

    def log(self, message):
        with open(f"logs/bot_{self.name}.log", "a", encoding="utf-8") as file:
            file.write(message + "\n")
        return

    def post(self, **generation_kwargs):
        message = self.get_post_text()
        image = self.get_post_image()
        graph = facebook.GraphAPI(self.token)
        post_time = dt.now().isoformat()
        try:
            if self.post_to_facebook:
                post_id = graph.put_object(parent_object='me', message=message, image=image, connection_name="feed")["id"]
            else:
                post_id = "NOT_POSTED"
            log_message = f"{post_time}:\n({len(self.texts) + 1}) POST FOR " + self.name + "\nID: {}".format(post_id) + "\nMessage:\n" + message + "\n"
        except Exception as e:
            log_message = "ERROR POSTING FOR " + self.name + " at " + post_time + "\n" + str(e)
        self.log(log_message)

class BibleBot(GPT2Bot):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, name="BibleBot", **kwargs)
        self.books = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"]
        
    def format_text(self, text):
        def prob(size):
            p = np.linspace(1, 0, size)
            return p/sum(p)
        try:
            end = list(re.finditer("[.;\n”\"\?]", text))[-1].start()
        except:
            end = len(text)
        book = np.random.choice(self.books)
        chapter = np.random.choice(range(1, 81), p=prob(80))
        verse = np.random.choice(range(1, 51), p=prob(50))
        header = f"{book}\nChapter {chapter}\n{verse}. "
        message = text[:end+1]
        return header + message

class QuranBot(GPT2Bot):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, name="QuranBot", **kwargs)
        self.books = ['Al-Fatihah', 'Al-Baqarah', "Al-'Imran", "An-Nisa'", "Al-Ma'idah", "Al-An'am", "Al-A'raf", 'Al-Anfal', 'Yunus', 'Hud', 'Yusuf', "Ar-Ra'd", 'Ibrahim', 'Al-Hijr', 'An-Nahl', "Isra'il", 'Al-Kahf', 'Maryam', 'Ha', "Al-Anbiya'", 'Al-Hajj', "Al-Mu'minun", 'An-Nur', 'Al-Furqan', "Ash-Shu'ara'", 'An-Naml', 'Al-Qasas', "Al-'Ankabut", 'Ar-Rum', 'Luqman', 'As-Sajdah', 'Al-Ahzab', "Al-Saba'", 'Al-Fatir', 'Sin', 'As-Saffat', 'Sad', 'Az-Zumar', "Al-Mu'min", 'Mim', 'Ash-Shura', 'Az-Zukhruf', 'Ad-Dukhan', 'Al-Jathiyah', 'Al-Ahqaf', 'Muhammad', 'Al-Fath', 'Al-Hujurat', 'Qaf', 'Ad-Dhariyat', 'At-Tur', 'An-Najm', 'Al-Qamar', 'Ar-Rahman', "Al-Waqi'ah", 'Al-Hadid', 'Al-Mujadilah', 'Al-Hashr', 'Al-Mumtahanah', 'As-Saff', "Al-Jumu'ah", 'Al-Munafiqun', 'At-Taghabun', 'At-Talaq', 'At-Tahrim', 'Al-Mulk', 'Al-Qalam', 'Al-Haqqah', "Al-Ma'arij", 'Nuh', 'Al-Jinn', 'Al-Muzzammil', 'Al-Muddaththir', 'Al-Qiyamah', 'Al-Insan', 'Al-Mursalat', "An-Naba'", "An-Nazi'at", "'Abasa", 'At-Takwir', 'Al-Infitar', 'At-Tatfif', 'Al-Inshiqaq', 'Al-Buruj', 'At-Tariq', "Al-A'la", 'Al-Ghashiyah', 'Al-Fajr', 'Al-Balad', 'Ash-Shams', 'Al-Lail', 'Ad-Duha', 'Al-Inshirah', 'At-Tin', "Al-'Alaq", 'Al-Qadr', 'Al-Bayyinah', 'Al-Zilzal', "Al-'Adiyat", "Al-Qari'ah", 'At-Takathur', "Al-'Asr", 'Al-Humazah', 'Al-Fil', 'Al-Quraish', "Al-Ma'un", 'Al-Kauthar', 'Al-Kafirun', 'An-Nasr', 'Al-Lahab', 'Al-Ikhlas', 'Al-Falaq', 'An-Nas']
        
    def format_text(self, text):
        def prob(size):
            p = np.linspace(1, 0, size)
            return p/sum(p)
        try:
            end = list(re.finditer("[.;\n”\"\?]", text))[-1].start()
        except:
            end = len(text)
        book = np.random.choice(self.books)
        verse = np.random.choice(range(1, 51), p=prob(50))
        header = f"{book}\nVerse {verse}\n"
        message = text[:end+1]
        return header + message

class LoveCraftBot(GPT2Bot):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, name="LoveCraftBot", **kwargs)

    def format_text(self, text):
        try:
            end = list(re.finditer("[.;\n”\"\?]", text))[-1].start()
        except:
            end = len(text)
        message = text[:end+1]
        if message.startswith("“"): message = message[1:]
        if message.endswith("”") or message.endswith("\n"): message = message[:-1]
        message = "“...{}...”".format(message)
        return message

class EquationGenBot(GPT2Bot):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, name="EquationGen", **kwargs)

    def check_lr(self, text):
        lefts = re.finditer("\\left", text)
        rights = re.finditer("\\right", text)
        if (len(lefts) == 0 and len(rights) != 0) or (len(rights) == 0 and len(lefts) != 0):
            return False
        if list(lefts)[0].start() > list(rights)[0].start():
            return False
        return True
    def format_text(self, text):
        
        text = text.split("\n\n")
        message = text[:end+1]
        if message.startswith("“"): message = message[1:]
        if message.endswith("”") or message.endswith("\n"): message = message[:-1]
        message = "“...{}...”".format(message)
        return message

# “”
BIBLECRAFTBOT = {"name": "BibleCraftBot",
                 "dataset": "dataset_won_300space_bible_won_nor_lb.txt",
                 "default_checkpoint": "latest",
                 "template": "{}"}
BIBLEBOT = {"name": "BibleBot",
            "dataset": "bible_cropped_wo_numbers_nor_lb.txt",
            "default_checkpoint": "latest",
            "template": "This is the word of God:\n\n{}"}
LOVECRAFTBOT = {"name": "LoveCraftBot",
                "dataset": "lovecraft.txt",
                "default_checkpoint": "latest",
                "template": "An old manuscript found in 1817 had the following words:\n\n{}"}
QURANBOT = {"name": "QuranBot",
            "dataset": "quran.txt",
            "default_checkpoint": "latest",
            "template": "In the name of God, the Gracious, the Merciful.\n\n{}"}

        
