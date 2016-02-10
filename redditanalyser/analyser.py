#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict, Counter

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from snudown import markdown

from . import cfg, logger
from .database import create_db_session


def strip_markdown(text):
    """Extract text from a markdown string.
    """
    html = markdown(text.encode('utf-8'))
    soup = BeautifulSoup(
        html,
        "html.parser",
        from_encoding='utf8'
        )
    return "".join(soup.findAll(text=True))


def extract_word_frequencies(text, is_markdown=True):
    """Parse given text and return a dictionary of word frequencies.

    :param is_markdown: if True, parse text from markdown
    """
    word_freqs = defaultdict(int)

    if is_markdown:
        text = strip_markdown(text)

    # convert text to lowercase
    text = text.lower()

    for token in word_tokenize(text):
        # stem token
        token = WordNetLemmatizer().lemmatize(token)

        if token not in stopwords.words('english') and len(token) > 2:
            word_freqs[token] += 1

    return word_freqs


def combine_word_frequencies(master_freqs, new_freqs):
    """Combine a new list of word frequencies to a master list.
    Return master dict.

    :param master_freqs: Master list of word frequencies

    :param new_freqs: New list of word frequencies to be added to master list
    """
    return (Counter(master_freqs) + Counter(new_freqs))


def main():
    pass

if __name__ == '__main__':
    main()
