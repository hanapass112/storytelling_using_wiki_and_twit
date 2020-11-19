

import os
import cv2
import gzip
import pickle
import sys
import time
import datetime
import copy
import random
import numpy as np
import pandas as pd
import json
import spacy
from neo4j import GraphDatabase
import threading
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup as bsoup




# ==================================================================================
# Basic Functions


def save_data(obj, file_name):
    file = gzip.GzipFile(file_name, 'wb')
    pickle.dump(obj, file)
    return



def load_data(file_name):
    file = gzip.GzipFile(file_name, 'rb')
    obj = pickle.load(file)
    return obj




def randomChoice(list):
    if len(list) == 0:
        return
    return list[random.randint(0, len(list) - 1)]



def is_story_exception(docs, sent_text):
    is_exception = False
    poses = [t.pos_ for t in docs]
    if 'VERB' not in poses \
            or 'RT @' in sent_text or '@MLB @Dodgers' == sent_text:
        is_exception = True
    return is_exception



def get_paragraphs(contents, KEYS):
    content_list = []
    for content in contents.split('\n'):
        if content == '' or '==' in content:
            continue
        entities, keywords_noun, keywords_verb, docs = my_nlp.get_entities(content, KEYS)
        if is_story_exception(docs, content):  # no VERB
            continue
        content_list.append(content)
    return content_list


