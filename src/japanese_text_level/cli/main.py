"""
japanese_text_level

A CLI tool for analyzing Japanese text and determining the WaniKani
level required to comprehend specific percentages of the kanji and
vocabulary present in the text.

The tool supports analyzing a user-provided .txt file or a bundled
example text for demonstration purposes.

USAGE:
        jp-level <system> <input-type> [target]

    SYSTEMS:
        wk          Use WaniKani level standards (Current)
        jlpt        Use JLPT level standards (Coming Soon)

    INPUT-TYPES:
        text        Analyze raw .txt files

    TARGETS:
        file        Path to a valid UTF-8 encoded text file
        --example   Use the internal example_text.txt
"""

import argparse
from importlib.resources import files
from pathlib import Path

from japanese_text_level.systems.wk import analyze_text


def main():
    """
    CLI entrypoint for japanese_text_level.

    This module defines the command-line interface and dispatches
    to the appropriate analysis system (e.g., WaniKani, JLPT).

    The CLI follows the structure:

        jp-level <system> <input-type> <input>

    Example:
        jp-level wk text file.txt
        jp-level wk text --example
    """

    parser = argparse.ArgumentParser(
        prog="jp-level",
        description="Japanese text difficulty analysis tool.",
    )

    subparsers = parser.add_subparsers(dest="system", required=True)

    # ---- WK system ----
    wk_parser = subparsers.add_parser("wk", help="WaniKani-based analysis")
    wk_subparsers = wk_parser.add_subparsers(dest="input_type", required=True)

    wk_text_parser = wk_subparsers.add_parser("text", help="Analyze text file")

    # Mutually exclusive group: either provide a file OR --example
    group = wk_text_parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "file",
        nargs="?",
        help="Path to input .txt file",
    )
    group.add_argument(
        "--example",
        action="store_true",
        help="Run analysis on bundled example text",
    )

    args = parser.parse_args()

    if args.system == "wk" and args.input_type == "text":
        # Determine source of text
        if args.example:
            data_dir = files("japanese_text_level").joinpath("files")
            example_path = data_dir / "example_text.txt"
            raw_text = example_path.read_text(encoding="utf-8")
            print("Example text:")
            print(raw_text)
        else:
            raw_text = Path(args.file).read_text(encoding="utf-8")

        # Analyze text
        kanji_levels, vocab_levels = analyze_text(raw_text)

        # Print results as a table
        print("\n------- WaniKani Analysis ------")
        print(f"{'Percentage':<10} | {'LV Kanji':<7} | {'LV Vocab':<7}")
        print("-" * 32)

        # Iterate through the percentages, sorted numerically
        for pct in sorted(kanji_levels.keys(), key=lambda x: int(x.rstrip("%"))):
            print(f"{pct:<10} | {kanji_levels[pct]:<5} | {vocab_levels[pct]:<5}")

        print("--------------------------------\n")
