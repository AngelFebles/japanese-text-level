# WaniKani Level Checker

A Python script to determine the **minimum WaniKani level required** to read a text in Japanese.
It supports **kanji** and **vocabulary** lookups using JSON datasets from extracted WaniKani.

Use:
```
python main.py "path/to/text.txt"
```

If no argument is given, script uses example text at files/example_text.txt

Example output:

```
Minimum Wanikani level to read kanji:  [{'80%': 3, '85%': 3, '90%': 3, '100%': 3}]
Minimum Wanikani level to read vocab:  [{'80%': 4, '85%': 4, '90%': 4, '100%': 4}]
```
