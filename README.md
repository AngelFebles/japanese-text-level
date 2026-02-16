# japanese_text_level
A CLI tool for analyzing Japanese text and determining the **WaniKani** level required to read specific percentages (80%, 90%, 95%, and 100%) of the **kanji** and **vocabulary** present.



---

## Installation

This project is designed to be used as a global CLI tool.

Install using **pipx**:

```bash
pipx install "git+https://github.com/AngelFebles/japanese-text-level"
```

## Usage
Analyze a .txt file containing Japanese text:
```
wk_level path/to/text.txt
```
Or use the bundled example text:

```
wk_level --example
```
Example output:
```
--- Example Text ---
今日、いい天気ですね〜
--------------------

Wanikani levels to read kanji: {'80%': 3, '90%': 3, '95%': 3, '100%': 3}
Wanikani levels to read vocab: {'80%': 4, '90%': 4, '95%': 4, '100%': 4}

```

## Development
### Instalation
To work on the project locally, first clone project:
```
git clone https://github.com/AngelFebles/japanese-text-level
cd japanese-text-level
```
and then either install with **pip**:
```
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```
or, if using **uv**, simply run:
```
uv sync
```
### Running Quality Checks
Unit tests:
```
pytest
```

Linting:
```
ruff check
```

Formatting:
```
ruff format
```

Type checking:
```
ty check
```

Run all checks in one line:
```
pytest && ruff check && ruff format && ty check
```
