# reddit-MTBI-scraper

A scraper for Reddit communities with scripts to perform post-scraping text analysis

## Usage

### Requirements

- [python 2.7](https://www.python.org/)
- [virtualenv](https://pypi.python.org/pypi/virtualenv)

### Installation

Clone the repository, then setup a virtual environment in the repo directory:

    $ virtualenv env

Activate the virtual environment:

    $ source env/bin/activate (on Linux or Mac)
    $ env/Scripts/activate.exe (on Windows)

Install requisite Python packages:

    $ pip install -r requirements.txt

### Configuration

Copy `config-sample.py` in the root directory and rename it `config.py`. Then configure the file, as appropriate.

Note: You *must* set the username before executing the scraper.

### Execution

Run the scraper:

    $ python -m scripts.comment_scraper
