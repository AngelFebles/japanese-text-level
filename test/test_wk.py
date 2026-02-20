from japanese_text_level.systems.wk import (
    analyze_text,
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


def test_analyze_text():

    assert analyze_text(test1) == (
        {"80%": 3, "90%": 3, "95%": 3, "100%": 4},
        {"80%": 3, "90%": 4, "95%": 4, "100%": 4},
    )


def test_empty_input():
    empty_text = ""
    fake_dict = {"今": 3}

    assert get_kanji_wanikani_levels(empty_text, fake_dict) == {}
    assert get_vocab_wanikani_levels(empty_text, fake_dict) == {}


def test_no_japanese_content():
    english_text = "Hello, how are you? 12345!"
    fake_dict = {"今": 3}

    assert get_kanji_wanikani_levels(english_text, fake_dict) == {}
    assert get_vocab_wanikani_levels(english_text, fake_dict) == {}


def test_unknown_kanji_handling():
    # Not in wanikani
    text = "齉"
    fake_dict = {"今": 3}

    # 100% of 1 item (level 61) should be 61
    result = get_kanji_wanikani_levels(text, fake_dict)
    assert result["100%"] == 61


def test_greedy_vocab_matching():
    text = "今日"
    fake_vocab = {
        "今": 3,
        "日": 2,
        "今日": 5,  # We give the compound a higher level to distinguish it
    }

    # If greedy matching works, it finds 1 word (level 5)
    # If it fails, it finds 2 words (level 3 and 2)
    result = get_vocab_wanikani_levels(text, fake_vocab)
    assert result["100%"] == 5
