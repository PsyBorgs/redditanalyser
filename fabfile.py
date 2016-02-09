# -*- coding: utf-8 -*-
import os
import sys
from contextlib import contextmanager

from fabric.api import local, lcd, prefix, env


BASE_DIR = os.path.join(os.path.dirname(__file__))
ENV_DIR = os.path.join(BASE_DIR, 'env')


@contextmanager
def virtualenv():
    if sys.platform == 'win32':
        activate = os.path.join(ENV_DIR, 'Scripts', 'activate')
    else:
        activate = '. {}'.format(os.path.join(ENV_DIR, 'bin', 'activate'))

    with prefix(activate):
        yield


def bootstrap():
    """Setup virtual env and python packages.
    """
    local("virtualenv {}".format(ENV_DIR))

    # install environment packages
    requirements = os.path.join(BASE_DIR, 'requirements.txt')
    with virtualenv():
        local("pip install -r {}".format(requirements))


def scrape():
    """Run Reddit scraper.
    """
    with virtualenv():
        local("python -m redditanalyser.scraper")


def test():
    """Run project tests.
    """
    with virtualenv():
        local("py.test redditanalyser")
