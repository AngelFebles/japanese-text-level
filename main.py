import json
import regex as re


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
                wanikani["kanji"][kanji] = level

    with open(wanikani_vocab_path, "r") as file:
        temp = json.load(file)
        # wanikani["kanji"] = json.load(file)
        for level in temp:
            for vocab in temp[level]:
                wanikani["vocab"][vocab] = level

    # print("一" in wanikani["kanji"])
    # print(wanikani["kanji"].get("一"))

    return wanikani


def get_kanji_wanikani_level(raw_text: str, wanikani_kanji: dict) -> int:
    """
    Returns the highest WaniKani level among the kanji in raw_text.

    Args:
        raw_text (str): Raw input text from which kanji will be extracted.

        wanikani_kanji (dict[str, int]): Mapping of kanji → level.

    Returns:
        int: The highest WaniKani level found among the kanji in the set.
                Returns 1 if no kanji in the set is found in the dataset.
    """

    kanji_set = get_kanjis_from_file(raw_text)

    max_level = 1

    for kanji in kanji_set:
        if kanji in wanikani_kanji:
            level = int(wanikani_kanji.get(kanji))
            if max_level < level:
                max_level = level

    return max_level


# WIP
def get_vocab_wanikani_level(raw_text: str, wanikani_vocab: dict) -> int:
    """
    Returns the highest WaniKani level among the vocab in raw_text.

    Args:
        raw_text (str): Raw input text to search for vocabulary items.

        wanikani_vocab (dict[str, int]): Mapping of vocabulary → level.

    Returns:
        int: The highest WaniKani level found among the kanji in the set.
                Returns 1 if no kanji in the set is found in the dataset.
    """

    # find vocabs from raw_text
    found_vocab = []

    for word in wanikani_vocab.keys():
        for match in re.finditer(re.escape(word), raw_text):
            found_vocab.append(word)

    found_vocab_set = set(found_vocab)

    # final step, get vocab levels
    max_level = 1

    for vocab in found_vocab_set:
        if vocab in wanikani_vocab:
            level = int(wanikani_vocab.get(vocab))
            if max_level < level:
                max_level = level

    return max_level


def get_kanjis_from_file(raw_text: str) -> set:
    """
    Extracts all Han-script characters from raw_text and returns them as a set.

    This solution for filtering with regex doesn't cover 100% of kanjis,
    it excludes some obscure/historical/incredibly rare characters.
    ex: 〆 (Unicode: U+3006) or 𦫖 (Unicode: U+26AD6)
    It is still good, however, for ~99.9% of cases.

    Since none of the omitted characters are present
    in Wanikani/JLPT/Jōyō kanji lists (the scope of this project)
    I implemented this solution.
    For a 100% one, refer to: https://ayaka.shn.hk/hanregex/

    Args:
        raw_text (str): the raw text extracted from the input file.

    Returns:
        set: Set of all kanjis from the string.

    """

    set_of_kanjis = set(re.findall(r"\p{Script=Han}", raw_text))

    return set_of_kanjis


def get_vocab_from_file(raw_text: str) -> set:

    return []


def main():

    wanikani_kanji_path = "files/kanjis_wanikani_levels.json"
    wanikani_vocab_path = "files/vocabs_wanikani_levels.json"

    wanikani_data = get_wanikani_data(wanikani_kanji_path, wanikani_vocab_path)

    input_file_path = "files/text.txt"
    with open(input_file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    wanikani_level_vocab = get_vocab_wanikani_level(raw_text, wanikani_data["vocab"])
    print("Minimum Wanikani level to read vocab: ", wanikani_level_vocab)

    wanikani_level_kanji = get_kanji_wanikani_level(raw_text, wanikani_data["kanji"])
    print("Minimum Wanikani level to read kanji: ", wanikani_level_kanji)


if __name__ == "__main__":
    main()
