import re
from os import getcwd, listdir
from os.path import isfile, join, isdir
from math import log

def split_words(text:str):
    return re.findall(r'\w+', text)