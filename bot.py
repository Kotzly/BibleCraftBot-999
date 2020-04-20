# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 23:38:15 2020

@author: Paulo
"""

import requests
import shutil
from bs4 import BeautifulSoup
import pandas as pd
import os
from os.path import join
import re

# re.findall("<math>[^/]*</math>", soup.text)
# link : soup.find_all("a").attrs["href"]

lovecraft_folder = "C:/Users/Paulo/Documents/GIT/BibleCraftBot-999/lovecraft_books"
quran_folder = "C:/Users/Paulo/Documents/GIT/BibleCraftBot-999/quran"
save_folder = "C:/Users/Paulo/Documents/GIT/BibleCraftBot-999/datasets"

# Getting Lovecraft books
root_url = "http://www.hplovecraft.com/writings/texts/"
resp = requests.get(root_url, stream=True)
soup = BeautifulSoup(resp.content, "lxml")
images_td = soup.find_all("li")

fiction_li = [str(x) for x in images_td if "fiction/" in str(x)]
pages = [x.split("\"")[1] for x in fiction_li]
links = [join(root_url, page) for page in pages]

try:
    os.mkdir(save_folder)
except: pass

for link in links:
    resp = requests.get(link, stream=True)
    soup = BeautifulSoup(resp.content, "lxml")
    text = soup.find_all("div")
    text = text[1].text.replace("\r\n", " ").replace("\n", "\n\n") #.replace("\u2032", "°")  "\u2032" is ° char
    book_name = re.search("(\w+).aspx", link).group(1) + ".txt"
    with open(join(lovecraft_folder, book_name ), "w", encoding="utf-8") as file:
        file.write(text)

texts = []
for book in os.listdir(lovecraft_folder):
    with open(join(lovecraft_folder, book), "r", encoding="utf-8") as file:
        texts.append(file.read())
texts = "\n".join(texts)
texts = re.sub("[\n ][\n ]+", "\n\n", texts)
with open(join(save_folder, "lovecraft.txt"), "w", encoding="utf-8") as file:
    file.write(texts)



# Bible w/o numbers
# Getting the bible

resp = requests.get("http://www.gutenberg.org/ebooks/10.txt.utf-8", stream=True)
text = resp.content.decode("utf-8")
start = text.find("The First Book of Moses")
end_str = "22:21 The grace of our Lord Jesus Christ be with you all. Amen."
end = text.find(end_str)
text = text[start:end + len(end_str)]
text = text.replace("\r\n", "\n")
with open(join(save_folder, "bible_cropped.txt"), "w", encoding="utf-8") as file:
    file.write(text) # First charact is \ufeff

with open(join(save_folder, "bible_cropped.txt"), "r", encoding="utf-8") as file:
    text = file.read()
    text = re.sub("[0-9]+:[0-9]+", "", text)
    text = re.sub("([^\n])(\n)([^\n])", lambda x: " ".join(x.group(1, 3)), text)

    text = re.sub("  +", " ", text)
    text = re.sub("\n ", "\n", text)
    text = re.sub("\n\n+", "\n\n", text)
with open(join(save_folder, "bible_cropped_wo_numbers_nor_lb.txt"), "w", encoding="utf-8") as file:
    file.write(text)


fusion_files = [join(save_folder, "bible_cropped_wo_numbers_nor_lb.txt"), join(save_folder, "book.txt")]
text = ""
dataset_name = "dataset_won_300space_bible_won_nor_lb.txt"
for file in fusion_files:
    with open(file, "r", encoding="utf-8") as file:
        text_ = file.read()
        text_ = "".join([[" ", x][ord(x) < 300 or ord(x) == 65279] for x in text_])
        text_ = re.sub("  +", " ", text_)
        text_ = re.sub("\n ", "\n", text_)
        text_ = re.sub("\n\n+", "\n\n", text_)

        text += text_
    text += "\n"

with open(join(save_folder, dataset_name), "w", encoding="utf-8") as file:
    file.write(text)

# Quran

link_ = "https://m.clearquran.com/{}.html"
for i in range(1, 114 + 1):
    page = str(i).rjust(3, "0")
    link = link_.format(page)
    resp = requests.get(link, stream=True)
    soup = BeautifulSoup(resp.content, "lxml")
    texts = soup.find_all("p")
    texts = [text.text for text in texts[1:] if not "In the name of God, the Gracious, the Merciful." in text.text]
    texts = [re.sub("\n[0-9]+\. ", "", text) for text in texts]
    with open(join(quran_folder, "{}.txt".format(page)), "w", encoding="utf-8") as file:
        file.write("\n\n".join(texts))

texts = []
for i in range(1, 114 + 1):
    page = str(i).rjust(3, "0")
    with open(join(quran_folder, "{}.txt".format(page)), "r", encoding="utf-8") as file:
        texts.append(file.read())
texts = "\n".join(texts)
with open(join(save_folder, "quran.txt"), "w", encoding="utf-8") as file:
        file.write(texts)

forbidden_words = ["nig", "obama"]
def any_element_in(elements, obj):
    for element in elements:
        if element.lower() in obj.lower():
            return True
    return False

def crop_sentence(x):
    if "." in x:
        x = ".".join(x.split(".")[:-1]) + "."
    elif "\n" in x:
        x = "\n".join(x.split("\n")[:-1]) + "\n"
    return x
