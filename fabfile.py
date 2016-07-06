# -*- coding: utf-8 -*-
import os
import sys
from contextlib import contextmanager

from fabric.api import local, lcd, prefix, env


BASE_DIR = os.path.join(os.path.dirname(__file__))
ENV_DIR = os.path.join(BASE_DIR, 'env')
LIB_DIR = os.path.join(BASE_DIR, 'lib')


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
    # initialise submodule(s)
    local("git submodule init")
    local("git submodule update")

    # setup virtualenv
    local("virtualenv {}".format(ENV_DIR))

    # install environment packages
    requirements = os.path.join(BASE_DIR, 'requirements.txt')
    with virtualenv():
        local("pip install -r {}".format(requirements))

        # install Reddit markdown parser
        with lcd(os.path.join(LIB_DIR, 'snudown')):
            local("python setup.py install")

    # install R packages
    local("Rscript requirements.R")

    # setup data and output directories
    dirs = [
        os.path.join(BASE_DIR, 'data', 'freq_tables'),
        os.path.join(BASE_DIR, 'build', 'wordclouds')
    ]
    if sys.platform == 'win32':
        map(lambda x: local('mkdir {0}'.format(x)), dirs)
    else:
        map(lambda x: local('mkdir -p {0}'.format(x)), dirs)


def scrape():
    """Run Reddit scraper.
    """
    with virtualenv():
        local("python -m app.scraper")


def analyse():
    """Run Reddit analyser.
    """
    with virtualenv():
        local("python -m app.analyser")


def test():
    """Run project tests.
    """
    with virtualenv():
        local("py.test app")
