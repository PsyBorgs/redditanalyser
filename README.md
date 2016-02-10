# redditanalyser

A scraper for Reddit communities (or users) with scripts to perform post-scraping text analysis.

## Usage

### Requirements

- [python 2.7](https://www.python.org/)
- [virtualenv](https://pypi.python.org/pypi/virtualenv)
- [fabric](http://fabfile.org/)
- [R](https://www.r-project.org/)

### Installation

Clone the repository, then bootstrap the environment:

    $ fab bootstrap

### Configuration

Copy `settings-sample.py` in the root directory and rename it `settings.py`. Then configure the file, as appropriate.

Note: You *must* set the username before executing the scraper.

### Execution

Run the scraper:

    $ fab scrape

Run the data analyser:

    $ fab analyse

Generate wordclouds:

    $ Rscript scripts/wordclouds.R


## Testing

Setup bootstrap environment, configure settings, and then run:

    $ fab test
