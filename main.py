import json
import regex as re
import sys
import numpy as np


def get_wanikani_data(wanikani_kanji_path: str, wanikani_vocab_path: str) -> dict:
    """
    Reads the WaniKani kanji and vocabulary JSON files and inverts them
    for fast lookups.

    This function loads both JSON files into memory and converts them from:
        level → [item1, item2, ...]
    to:
        item → level
    This avoids repeated scans for individual lookups.

    Args:
        wanikani_kanji_path (str): Path to the kanji JSON file by level.

        wanikani_vocab_path (str): Path to the vocabulary JSON file by level.

    Returns:
        dict: A dictionary with two keys: "kanji" and "vocab", each mapping
        items to their levels:
            {
                "kanji": dict[str, int],  # kanji character → level
                "vocab": dict[str, int]   # vocabulary word → level
            }
    """

    wanikani = {"kanji": {}, "vocab": {}}

    with open(wanikani_kanji_path, "r") as file:
        temp = json.load(file)
        # wanikani["kanji"] = json.load(file)
        for level in temp:
            for kanji in temp[level]:
                wanikani["kanji"][kanji] = int(level)

    with open(wanikani_vocab_path, "r") as file:
        temp = json.load(file)
        # wanikani["kanji"] = json.load(file)
        for level in temp:
            for vocab in temp[level]:
                wanikani["vocab"][vocab] = int(level)

    # print("一" in wanikani["kanji"])
    # print(wanikani["kanji"].get("一"))

    return wanikani


def get_kanji_wanikani_level(raw_text: str, wanikani_kanji: dict) -> dict:
    """
    Returns mapping of WaniKani level needed to read difference percentages of the kanji in raw_text.

    Args:
        raw_text (str): Raw input text from which kanji will be extracted.

        wanikani_kanji (dict[str, int]): Mapping of kanji → level.

    Returns:
        dict: mapping of the levels needed to read different percentaged of the raw text
              {
                percentage → level
              }

    """

    # This solution for filtering with regex (Script=Han) doesn't cover 100% of kanjis,
    # it excludes some obscure/historical/incredibly rare characters.
    # ex: 〆 (Unicode: U+3006) or 𦫖 (Unicode: U+26AD6)
    # It is still good, however, for ~99.9% of cases.

    # Since none of the omitted characters are present
    # in Wanikani/JLPT/Jōyō kanji lists (the scope of this project)
    # I implemented this solution.
    # For a 100% one, refer to: https://ayaka.shn.hk/hanregex/

    kanjis_text = set(re.findall(r"\p{Script=Han}", raw_text))

    kanji_levels = []

    for item in kanjis_text:
        if item in wanikani_kanji.keys():
            kanji_levels.append(wanikani_kanji[item])
        else:
            kanji_levels.append(61)
    if kanji_levels == []:
        return []
    else:
        return [
            {
                "80%": int(np.percentile(kanji_levels, 80)),
                "85%": int(np.percentile(kanji_levels, 85)),
                "90%": int(np.percentile(kanji_levels, 90)),
                "100%": int(np.percentile(kanji_levels, 95)),
            }
        ]


# WIP
def get_vocab_wanikani_level(raw_text: str, wanikani_vocab: dict) -> int:
    """
     Returns mapping of WaniKani level needed to read difference percentages of the vocab in raw_text.

    Args:
        raw_text (str): Raw input text from which kanji will be extracted.

        wanikani_vocab (dict[str, int]): Mapping of vocab → level.

    Returns:
        dict: mapping of the levels needed to read different percentaged of the raw text
              {
                percentage → level
              }
    """

    # find vocabs from raw_text
    found_vocab = []

    for word in wanikani_vocab.keys():
        for match in re.finditer(re.escape(word), raw_text):
            found_vocab.append(word)

    found_vocab_set = set(found_vocab)

    # final step, get vocab levels

    vocab_levels = []

    for item in found_vocab_set:
        if item in wanikani_vocab.keys():
            vocab_levels.append(wanikani_vocab[item])
        else:
            vocab_levels.append(61)
    if vocab_levels == []:
        return []
    else:
        return [
            {
                "80%": int(np.percentile(vocab_levels, 80)),
                "85%": int(np.percentile(vocab_levels, 85)),
                "90%": int(np.percentile(vocab_levels, 90)),
                "100%": int(np.percentile(vocab_levels, 95)),
            }
        ]


# def get_kanjis_from_file(raw_text: str) -> set:
#     """
#     Extracts all Han-script characters from raw_text and returns them as a set.

#     This solution for filtering with regex doesn't cover 100% of kanjis,
#     it excludes some obscure/historical/incredibly rare characters.
#     ex: 〆 (Unicode: U+3006) or 𦫖 (Unicode: U+26AD6)
#     It is still good, however, for ~99.9% of cases.

#     Since none of the omitted characters are present
#     in Wanikani/JLPT/Jōyō kanji lists (the scope of this project)
#     I implemented this solution.
#     For a 100% one, refer to: https://ayaka.shn.hk/hanregex/

#     Args:
#         raw_text (str): the raw text extracted from the input file.

#     Returns:
#         set: Set of all kanjis from the string.

#     """

#     set_of_kanjis = set(re.findall(r"\p{Script=Han}", raw_text))

#     return set_of_kanjis


# def get_vocab_from_file(raw_text: str) -> set:

#     return []


def main(input_file_path):

    wanikani_kanji_path = "files/kanjis_wanikani_levels.json"
    wanikani_vocab_path = "files/vocabs_wanikani_levels.json"

    wanikani_data = get_wanikani_data(wanikani_kanji_path, wanikani_vocab_path)
    # print(wanikani_data["kanji"])

    with open(input_file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    wanikani_level_kanji = get_kanji_wanikani_level(raw_text, wanikani_data["kanji"])
    print("Minimum Wanikani level to read kanji: ", wanikani_level_kanji)

    wanikani_level_vocab = get_vocab_wanikani_level(raw_text, wanikani_data["vocab"])
    print("Minimum Wanikani level to read vocab: ", wanikani_level_vocab)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])

    else:
        input_file_path = "files/text.txt"
        main(input_file_path)
