import numpy as np


def comment_sentiment_avg(comments):
    polarities = np.array([c.sentiment.polarity for c in comments])
    subjectivities = np.array([c.sentiment.subjectivity for c in comments])

    avg_polarity = np.mean(polarities)
    avg_subjectivity = np.mean(subjectivities)

    return {'polarity': avg_polarity, 'subjectivity': avg_subjectivity}
