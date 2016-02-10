# -*- coding: utf-8 -*-
import pytest

from redditanalyser import cfg, analyser
from redditanalyser.tests import MOCK_TEXT_1, MOCK_TEXT_2, MOCK_TEXT_3


def test_strip_markdown():
    # NOTE: cf. utf-8 emdash
    text_md = ("[Link to the study]"
               "(http://www.cmaj.ca/content/early/2016/02/08/cmaj.150790) "
               u"— now")
    text_expected = u"Link to the study — now\n"
    assert analyser.strip_markdown(text_md) == text_expected


def test_extract_word_frequencies():
    expected = {
        u'ceaseth': 1,
        u'sea': 2,
        u'seething': 2,
        u'sufficeth': 1,
        u'thus': 1,
    }
    assert analyser.extract_word_frequencies(MOCK_TEXT_1) == expected


def test_extract_word_frequencies_2():
    expected = {
        u'sea': 6,
        u'sell': 4,
        u'shell': 5,
        u'shore': 3,
        u'sure': 2
    }
    assert analyser.extract_word_frequencies(MOCK_TEXT_2) == expected


def test_extract_word_frequencies_3():
    expected = {
        u'believe': 1,
        u'cannot': 2,
        u'really': 1,
        u'sea': 1,
        u'seller': 1,
        u'shell': 1
    }
    assert analyser.extract_word_frequencies(MOCK_TEXT_3) == expected
