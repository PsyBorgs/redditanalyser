class Config(object):
    """Settings for your Reddit scraper project.

    Note: Every object must have a value.
    """
    # Your Reddit username for the bot.
    # IMPORTANT: This must be set before running the code.
    username = None

    # A list of subreddits that you are targeting for scraping.
    # Note: enter `/r/TARGET` for subreddits or `/u/TARGET` for users
    targets = [
        "/r/science",
        "/r/technology"
    ]

    # Period to count words over; e.g., day/week/month/year/all
    period = "all"

    # Maximum number of submissions/comments to count word frequencies for
    # Note: For no limit, set value to `0`
    limit = 0

    # Maximum relative frequency in the text a word can appear to be considered
    # in word counts (prevents word spamming in a single submission)
    max_threshold = 0.34

    # Count repeated words in text blocks (titles, selftexts, comment bodies)
    # and increment the word count, rather than counting each word occurrence
    # only once per block
    count_word_freqs = True

    # Enable PRAW multiprocess support
    multiprocess = True
