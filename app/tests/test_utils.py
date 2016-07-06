# -*- coding: utf-8 -*-
import pytest

from app import utils
from app.tests import MOCK_TEXT_3


def test_contraction_expander():
    contraction_expander = utils.ContractionExpander()
    text = "they'll she'll can't won't I'd you've"
    expected = "they will she will cannot will not I would you have"
    assert contraction_expander.replace(text) == expected


def test_strip_punct():
    expected = ("I cant believe that she was a sea shell seller "
                u"—— I really cant  ")
    assert utils.strip_punct(MOCK_TEXT_3) == expected
