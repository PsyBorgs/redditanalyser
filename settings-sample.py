class Settings(object):
    """Settings for your project.

    Note: Every object must have a value.
    """
    # Sets your Reddit username for the bot. Don't forget to set this!
    username = None

    # A list of subreddits that you are targeting for scraping.
    # Note: enter `/r/TARGET` for subreddits or `/u/TARGET` for users
    targets = [
        "/r/science",
        "/r/technology"
    ]

    # Period to count words over:; e.g., day/week/month/year/all
    period = "all"

    # Maximum number of submissions/comments to count word frequencies for
    # Note: For no limit, set value to `0`
    limit = 0

    # Maximum relative frequency in the text a word can appear to be considered
    # in word counts (prevents word spamming in a single submission)
    max_threshold = 0.34

    # Words repeated in text blocks (titles, selftexts, comment bodies)
    # increment the word count, rather than being counted a word once per block
    count_word_freqs = True

    # Enable PRAW multiprocess support
    multiprocess = True

    options, args = parser.parse_args()

    if len(args) != 2:
        parser.error("Invalid number of arguments provided.")
    user, target = args

    if target.startswith("/r/"):
        options.is_subreddit = True
    elif target.startswith("/u/"):
        options.is_subreddit = False
    else:
        parser.error("Invalid target.")

    if options.period not in ["day", "week", "month", "year", "all"]:
        parser.error("Invalid period.")

    if options.include_dictionary:
        with open(os.path.join(PACKAGE_DIR, "words", "dict-words.txt"), "r") as in_file:
            for line in in_file:
                COMMON_WORDS.add(line.strip().lower())

    return user, target, options
