#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
from collections import defaultdict, Counter

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize
from snudown import markdown
from sqlalchemy.orm import joinedload
from tqdm import tqdm

from app import cfg, logger, reddit, session
from app.models import Submission
from app.utils import ContractionExpander, strip_punct


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


def subreddit_frequency_csv(submissions, subreddit_id):
    """Generate a frequency table CSV given a subreddit name.
    """
    # generate master word frequency dict from submission comments
    subreddit_word_freqs = Counter()
    for submission in tqdm(submissions, desc="Processing submissions"):
        for comment in submission.comments:
            word_freqs = extract_word_frequencies(comment.body)
            subreddit_word_freqs.update(word_freqs)

    # save master word frequency dict to CSV
    csv_path = os.path.join(
        cfg.PROJECT_ROOT, 'data', 'freq_tables', '{}.csv'.format(subreddit_id))
    subreddit_wf_series = pd.Series(subreddit_word_freqs)
    subreddit_wf_series.\
        sort_values(ascending=False).\
        to_csv(csv_path, encoding='utf-8')


def subreddit_desc_stats(submissions):
    """Generate descriptive statistics for a given subreddit. Return dict.
    """
    num_submissions = len(submissions)
    num_comments = sum([len(s.comments) for s in submissions if s.comments])
    comments_per_submission = (float(num_comments) / num_submissions)

    # average sentiment scores
    polarities = [s.sentiment.polarity for s in submissions if s.sentiment]
    avg_polarity = np.mean(polarities) if polarities else None
    subjectivities = [
        s.sentiment.subjectivity for s in submissions if s.sentiment]
    avg_subjectivity = np.mean(subjectivities) if subjectivities else None

    return {
        'num_submissions': num_submissions,
        'num_comments': num_comments,
        'comments_per_submission': comments_per_submission,
        'sentiment_polarity_avg': avg_polarity,
        'sentiment_subjectivity_avg': avg_subjectivity
    }


def main():
    desc_stats = []
    for target in cfg.TARGETS:
        if target.startswith("/r/"):
            subreddit_name = target[3:]

            # get subreddit ID
            subreddit = reddit.get_subreddit(subreddit_name)
            subreddit_id = subreddit.fullname

            # get subreddit submissions
            submissions = session.query(Submission).\
                options(
                    joinedload(Submission.comments),
                    joinedload(Submission.sentiment)
                ).\
                filter_by(subreddit_id=subreddit_id).\
                all()

            logger.warning(
                "Generating frequency table and descriptive "
                "statistics for {} subreddit...".
                format(subreddit_name)
                )
            # generate frequency table
            subreddit_frequency_csv(submissions, subreddit_id)

            # append descriptive stats to list
            subreddit_stats = subreddit_desc_stats(submissions)
            subreddit_stats['subreddit_name'] = subreddit_name
            subreddit_stats['subreddit_id'] = subreddit_id
            desc_stats.append(subreddit_stats)

    # Save descriptive statistics to CSV
    desc_stats_csv = os.path.join(cfg.PROJECT_ROOT, 'data', 'desc_stats.csv')
    desc_stats_df = pd.DataFrame(desc_stats).\
        sort_values(by='comments_per_submission', ascending=False)
    desc_stats_df.to_csv(desc_stats_csv, encoding='utf-8')


if __name__ == '__main__':
    main()
