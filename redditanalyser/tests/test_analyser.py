import pytest

from redditanalyser import cfg, analyser


def test_strip_markdown():
    text_md = ("[Link to the study]"
               "(http://www.cmaj.ca/content/early/2016/02/08/cmaj.150790)")
    text_expected = "Link to the study\n"
    assert analyser.strip_markdown(text_md) == text_expected


def test_extract_word_frequencies():
    text = ("How much wood would a woodchuck chuck if a woodchuck could "
            "chuck wood?")
    expected = {
        u'chuck': 2,
        u'could': 1,
        u'much': 1,
        u'wood': 2,
        u'woodchuck': 2,
        u'would': 1
    }
    assert analyser.extract_word_frequencies(text) == expected


def test_extract_word_frequencies_2():
    text = (
        "Betty Botter bought a bit of butter. "
        "The butter Betty Botter bought was a bit bitter "
        "And made her batter bitter. "
        "But a bit of better butter makes better batter. "
        "So Betty Botter bought a bit of better butter "
        "Making Betty Botter's bitter batter better")
    expected = {
        u'batter': 3,
        u'better': 4,
        u'betty': 4,
        u'bit': 4,
        u'bitter': 3,
        u'botter': 4,
        u'bought': 3,
        u'butter': 4,
        u'made': 1,
        u'make': 1,
        u'making': 1,
    }
    assert analyser.extract_word_frequencies(text) == expected
