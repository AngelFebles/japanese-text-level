"""
WaniKani analysis system.

Provides functions to determine the WaniKani level required
to comprehend specified percentages of kanji and vocabulary
within a given Japanese text.
"""

import json
from importlib.abc import Traversable
from importlib.resources import files

import numpy as np
import regex as re


def get_wanikani_data(
    wanikani_kanji_path: Traversable, wanikani_vocab_path: Traversable
) -> dict:
    """
    Reads the WaniKani kanji and vocabulary JSON files and inverts them
    for fast lookups.

    This function loads both JSON files into memory and converts them from:
        level → [item1, item2, ...]
    to:
        item → level
    This avoids repeated scans for individual lookups.

    Args:

        wanikani_kanji_path (Traversable): Path to the kanji JSON file by level.

        wanikani_vocab_path (Traversable): Path to the vocabulary JSON file by level.

    Returns:

        dict: A dictionary with two keys: "kanji" and "vocab", each mapping
            items to their levels:
                {
                    "kanji": dict[str, int],  # kanji character → level
                    "vocab": dict[str, int]   # vocabulary word → level
                }
    """

    wanikani = {"kanji": {}, "vocab": {}}

    with wanikani_kanji_path.open("r", encoding="utf-8") as file:
        temp = json.load(file)

        for level in temp:
            for kanji in temp[level]:
                wanikani["kanji"][kanji] = int(level)

    with wanikani_vocab_path.open("r", encoding="utf-8") as file:
        temp = json.load(file)

        for level in temp:
            for vocab in temp[level]:
                wanikani["vocab"][vocab] = int(level)

    return wanikani


def load_wanikani_data() -> dict:
    data_dir = files("japanese_text_level").joinpath("files")

    kanji_path = data_dir / "kanjis_wanikani_levels.json"
    vocab_path = data_dir / "vocabs_wanikani_levels.json"

    return get_wanikani_data(kanji_path, vocab_path)


def get_kanji_wanikani_levels(raw_text: str, wanikani_kanji: dict) -> dict:
    """
    Returns mapping of WaniKani level needed to read difference percentages of the kanji in raw_text.

    Note:

    This solution for filtering with regex (Script=Han) doesn't cover 100% of kanjis,
    it excludes some obscure/historical/incredibly rare characters.
    ex: 〆 (Unicode: U+3006) or 𦫖 (Unicode: U+26AD6)
    It is still good, however, for ~99.9% of cases.

    Since none of the omitted characters are present
    in Wanikani/JLPT/Jōyō kanji lists (the scope of this project)
    I implemented this solution.
    For a 100% one, refer to: https://ayaka.shn.hk/hanregex/

    Args:

        raw_text (str): Raw input text from which kanji will be extracted.

        wanikani_kanji (dict[str, int]): Mapping of kanji → level.

    Returns:

        dict: mapping of the levels needed to read different percentaged of the raw text
              { percentage → level }

    """

    # This solution for filtering with regex (Script=Han) doesn't cover 100% of kanjis,
    # it excludes some obscure/historical/incredibly rare characters.
    # ex: 〆 (Unicode: U+3006) or 𦫖 (Unicode: U+26AD6)
    # It is still good, however, for ~99.9% of cases.

    # Since none of the omitted characters are present
    # in Wanikani/JLPT/Jōyō kanji lists (the scope of this project)
    # I implemented this solution.
    # For a 100% one, refer to: https://ayaka.shn.hk/hanregex/

    kanjis_text = re.findall(r"\p{Script=Han}", raw_text)

    kanji_levels = [wanikani_kanji.get(item, 61) for item in kanjis_text]

    # print(kanji_levels)

    # print(kanji_levels)

    if kanji_levels == []:
        return {}
    else:
        return {
            "80%": int(np.percentile(kanji_levels, 80)),
            "90%": int(np.percentile(kanji_levels, 90)),
            "95%": int(np.percentile(kanji_levels, 95)),
            "100%": max(kanji_levels),
        }


def get_vocab_wanikani_levels(raw_text: str, wanikani_vocab: dict) -> dict:
    """
     Returns mapping of WaniKani level needed to read difference percentages of the vocab in raw_text.

    Args:

        raw_text (str): Raw input text from which kanji will be extracted.

        wanikani_vocab (dict[str, int]): Mapping of vocab → level.

    Returns:

        dict: mapping of the levels needed to read different percentaged of the raw text
              { percentage → level }
    """

    # found_vocab = []

    # Code runs well if we unify the pattern creation into a single expression
    # but type checkers complain for [no-matching-overload] if you don't
    # separate re.compile and the 'join' call

    vocab_keys = list(wanikani_vocab.keys())
    vocab_keys.sort(key=len, reverse=True)

    escaped_vocab = [re.escape(word) for word in vocab_keys]
    joined_pattern = "|".join(escaped_vocab)

    pattern = re.compile(f"(?=({joined_pattern}))")
    found_vocab = [m.group(1) for m in pattern.finditer(raw_text)]

    vocab_levels = []

    for item in found_vocab:
        if item in wanikani_vocab:
            vocab_levels.append(wanikani_vocab[item])
        else:
            vocab_levels.append(61)
    if vocab_levels == []:
        return {}
    else:
        return {
            "80%": int(np.percentile(vocab_levels, 80)),
            "90%": int(np.percentile(vocab_levels, 90)),
            "95%": int(np.percentile(vocab_levels, 95)),
            "100%": max(vocab_levels),
        }


def analyze_text(raw_text: str) -> tuple[dict, dict]:
    data = load_wanikani_data()

    kanji_levels = get_kanji_wanikani_levels(raw_text, data["kanji"])
    vocab_levels = get_vocab_wanikani_levels(raw_text, data["vocab"])

    return kanji_levels, vocab_levels
