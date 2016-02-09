import pytest

from redditanalyser import cfg, analyser


def test_strip_markdown():
    text_md = ("[Link to the study]"
               "(http://www.cmaj.ca/content/early/2016/02/08/cmaj.150790)")
    text_expected = "Link to the study\n"
    assert analyser.strip_markdown(text_md) == text_expected


MOCK_TEXT_1 = (
    "The seething sea ceaseth and thus the seething sea sufficeth us.")
MOCK_TEXT_2 = (
    "She sells sea shells on the sea shore. "
    "The shells she sells are sea shells, I'm sure. "
    "For if she sells sea shells on the sea shore "
    "Then I'm sure she sells sea shore shells."
    )


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
