import numpy as np
from textblob import TextBlob


def comment_sentiment(comment):
    comment_blob = TextBlob(comment.body)
    return {
        'comment_id': comment.id,
        'polarity': comment_blob.sentiment.polarity,
        'subjectivity': comment_blob.sentiment.subjectivity
    }


def comment_sentiment_avg(comments):
    polarities = np.array([c.sentiment.polarity for c in comments])
    subjectivities = np.array([c.sentiment.subjectivity for c in comments])

    avg_polarity = np.mean(polarities)
    avg_subjectivity = np.mean(subjectivities)

    return {'polarity': avg_polarity, 'subjectivity': avg_subjectivity}
