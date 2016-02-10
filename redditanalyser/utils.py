# -*- coding: utf-8 -*-
import re
from string import punctuation


CONTRACTION_PATTERNS = [
    (r'won\'t', 'will not'),
    (r'can\'t', 'cannot'),
    (r'i\'m', 'i am'),
    (r'ain\'t', 'is not'),
    (r'(\w+)\'ll', '\g<1> will'),
    (r'(\w+)n\'t', '\g<1> not'),
    (r'(\w+)\'ve', '\g<1> have'),
    (r'(\w+)\'s', '\g<1> is'),
    (r'(\w+)\'re', '\g<1> are'),
    (r'(\w+)\'d', '\g<1> would')
]


class ContractionExpander(object):
    """docstring for ContractionExpander"""
    def __init__(self, patterns=CONTRACTION_PATTERNS):
        self.patterns = [
            (re.compile(regex), repl) for (regex, repl) in patterns]

    def replace(self, text):
        for (regex, repl) in self.patterns:
            text = regex.sub(repl, text)
        return text


def strip_punct(text):
    return u''.join([c for c in text if c not in punctuation])
