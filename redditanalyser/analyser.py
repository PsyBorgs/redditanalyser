#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
from collections import defaultdict, Counter

import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize
from snudown import markdown
from sqlalchemy.orm import joinedload
from tqdm import tqdm

from . import cfg, logger
from .database import create_db_session
from .models import Submission
from .utils import ContractionExpander, strip_punct


# contraction handling
contraction_expander = ContractionExpander()


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

    # expand contractions
    text = contraction_expander.replace(text)

    # remove remaining punctuation
    text = strip_punct(text)

    # convert text to lowercase
    text = text.lower()

    for token in wordpunct_tokenize(text):
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
    # setup DB session
    session = create_db_session(cfg.SQLALCHEMY_DATABASE_URI)

    # get submissions
    submissions = session.query(Submission).\
        options(joinedload("comments")).\
        all()

    # generate master word frequency dict from submission comments
    all_words = Counter()
    for submission in tqdm(submissions, desc="Submissions"):
        for comment in submission.comments:
            comment_wfs = extract_word_frequencies(comment.body)
            all_words.update(comment_wfs)

    # save master word frequency dict to CSV
    all_words_series = pd.Series(all_words)
    all_words_series.\
        sort_values(ascending=False).\
        to_csv(os.path.join(cfg.PROJECT_ROOT, 'data', 'all_freqs.csv'))


if __name__ == '__main__':
    main()
