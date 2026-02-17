# tests/test_main.py
from japanese_text_level.main import (
    get_kanji_wanikani_levels,
    get_vocab_wanikani_levels,
)

test1 = """
今日、いい天気ですね〜

I like bananas.

ñandu 今今今.
????????/!!!!!!!!!!!!!!!!!!@@@@
"""


def test_get_kanji_wanikani_levels():
    fake_kanji_dict = {
        "今": 3,
        "日": 2,
        "天": 2,
        "気": 4,
    }

    kanji_key_test1 = {"80%": 3, "90%": 3, "95%": 3, "100%": 4}

    assert get_kanji_wanikani_levels(test1, fake_kanji_dict) == kanji_key_test1


def test_get_vocab_wanikani_levels():
    fake_vocab_dict = {
        "今": 3,
        "日": 2,
        "今日": 3,
        "天": 2,
        "気": 4,
        "天気": 4,
    }

    vocab_key_test1 = {"80%": 3, "90%": 4, "95%": 4, "100%": 4}
    assert get_vocab_wanikani_levels(test1, fake_vocab_dict) == vocab_key_test1
