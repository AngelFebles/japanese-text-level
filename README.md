# japanese_text_level

A CLI tool for analyzing Japanese text and determining reading difficulty levels based on WaniKani (and future systems like JLPT). It calculates the level required to read specific percentages (80%, 90%, 95%, 100%) of kanji and vocabulary in your text.


Full documentation available [here](https://angelfebles.github.io/japanese-text-level/).

See [ROADMAP.md](./ROADMAP.md) for the full development plan.

---

## Installation

This project is designed to be used as a global CLI tool.

Install using **pipx**:

```bash
pipx install "git+https://github.com/AngelFebles/japanese-text-level"
```

## Usage

### CLI Synopsis
```
jp-level <system> <input-type> [target | --example]
```

| Component | Options | Description |
| :--- | :--- | :--- |
| **SYSTEM** | wk | WaniKani (Kanji/Vocab levels 1-60) |
|  | jlpt | Coming Soon (N5 to N1) |
| **INPUT_TYPE** | text | Standard .txt file processing |
|  | url | Planned (Direct website scraping) |
| **TARGET** | path/to/file | Local path to your Japanese text |
|  | --example | Runs the bundled sample text |


### Examples
Analyze a local file:
```bash
jp-level wk text path/to/file.txt
```
Or the bundled example:
```bash
jp-level wk text --example
```
Which outputs:
```
Example text:
今日、いい天気ですね〜


------- WaniKani Analysis ------
Percentage | LV Kanji | LV Vocab
--------------------------------
80%        | 3     | 4
90%        | 3     | 4
95%        | 3     | 4
100%       | 4     | 4
--------------------------------
```


## Development

### Instalation
To work on the project locally, first clone project:
```bash
git clone https://github.com/AngelFebles/japanese-text-level
cd japanese-text-level
```
and then either install with **pip**:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```
or, if using **uv**, simply run:
```bash
uv sync

```
### Quality Checks
```bash
pytest        # Unit tests
ruff check .  # Linting
ruff format . # Formatting
ty check .    # Type checking
```

### Documentation
Documentation website is handled with mkdocs. To preview localy:
```bash
mkdocs serve
```

### Project Structure
* src/japanese_text_level/
    * main.py - CLI Entrypoint and Argument Parsing.
    * systems/ - Analysis logic for different grading systems (e.g., wk.py).
    * files/ - Reference JSON datasets and example files.
* test/ - Automated test suite.
