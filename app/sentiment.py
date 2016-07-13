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
    def _export_data(df, table_name):
        session_bind = session.get_bind()
        df.to_sql(
            table_name,
            session_bind.engine,
            chunksize=1000,
            if_exists='replace',
            index_label='id'
            )
    _export_data(comment_sentiments_df, CommentSentiment.__tablename__)
    _export_data(submission_sentiments_df, SubmissionSentiment.__tablename__)


if __name__ == '__main__':
    main()
