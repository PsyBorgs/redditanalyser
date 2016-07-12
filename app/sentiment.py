import os.path

import numpy as np
import pandas as pd
from sqlalchemy.orm import joinedload
from textblob import TextBlob
from tqdm import tqdm

from app import cfg, logger, reddit, session
from app.models import (
    Submission, SubmissionSentiment, Comment, CommentSentiment)


def comment_sentiment(comment):
    """Generate sentiment scores for a given comment object.
    """
    comment_blob = TextBlob(comment.body)
    return {
        'comment_id': comment.id,
        'polarity': comment_blob.sentiment.polarity,
        'subjectivity': comment_blob.sentiment.subjectivity
    }


def comment_sentiment_avg(comment_sentiments):
    """Generate average sentiment scores for the comments within a submission.
    """
    polarities = np.array([c['polarity'] for c in comment_sentiments])
    subjectivities = np.array([c['subjectivity'] for c in comment_sentiments])

    avg_polarity = np.mean(polarities)
    avg_subjectivity = np.mean(subjectivities)

    return {'polarity': avg_polarity, 'subjectivity': avg_subjectivity}


def main():
    # session and engine info for exporting data
    session_bind = session.get_bind()
    engine = session_bind.engine

    # all cached submissions with eager-loaded comments
    submissions = session.query(Submission).\
        options(joinedload('comments')).\
        all()

    # data frames for generated sentiments
    submission_sentiments_df = pd.DataFrame()
    comment_sentiments_df = pd.DataFrame()

    for s in tqdm(submissions, desc="Submissions"):
        c_sentiments = []
        comments = s.comments
        if comments:
            # calculate comment sentiments
            for c in tqdm(comments, desc="Comments", nested=True):
                c_sentiment = comment_sentiment(c)
                c_sentiments.append(c_sentiment)

            # calculate average submission sentiments
            s_sentiment = comment_sentiment_avg(c_sentiments)
            s_sentiment.update({'submission_id': s.id})

            # append sentiments to data frames
            comment_sentiments_df = comment_sentiments_df.append(
                pd.DataFrame(c_sentiments), ignore_index=True)
            submission_sentiments_df = submission_sentiments_df.append(
                s_sentiment, ignore_index=True)

    # export generated data
    comment_sentiment_csv = os.path.join(
        cfg.PROJECT_ROOT, 'data', 'comment_sentiments.csv')
    comment_sentiments_df.to_csv(comment_sentiment_csv)

    submission_sentiment_csv = os.path.join(
        cfg.PROJECT_ROOT, 'data', 'submission_sentiments.csv')
    submission_sentiments_df.to_csv(submission_sentiment_csv)


if __name__ == '__main__':
    main()
