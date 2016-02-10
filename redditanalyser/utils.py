# -*- coding: utf-8 -*-
import re


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
        new_text = text
        for (regex, repl) in self.patterns:
            (new_text, count) = re.subn(regex, repl, new_text)
            return new_text
