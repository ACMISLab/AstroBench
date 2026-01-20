import re
import json
import pandas as pd

COLS = [
    "Test Forward Step_Model_Response",
    "Test Mid Step_Model_Response",
    "Test Backward Step_Model_Response",
]

# =========================
# Rule 1: Extract JSON-style "filled replace": ...
# Supports multiple occurrences; the last one is used.
# Supported forms:
#   1) "filled replace": [ ... ]
#   2) "filled replace": " ... "
#   3) "filled replace": “ ... ”
# =========================
FILLED_REPLACE_ALL_RE = re.compile(
    r'"filled replace"\s*:\s*([\["“])',
    re.IGNORECASE
)

# =========================
# Rule 2: Extract Filled Replace blocks under section headers (more robust)
# Supported headers:
#   ## Filled Replace:
#   ## Filled Replaces
#   # Filled Replaces
#   **Filled Replace**
#   ### Filled in Replace
#   ### Filled in Replace:
#   ### Filled in Replace (case-insensitive)
#
# Notes:
# - Header lines may start with Markdown # or be bolded with **...**
# - Trailing ':' or '：' is allowed
# - Replace/Replaces (singular/plural) are allowed
# - Variants like "Filled in Replace", "Filled Replace Content",
#   "Fill the replace content" are supported
# =========================

# 1) Header detection: Markdown headers (#) or bold headers (**...**)
HEADER_ANY_RE = re.compile(
    r'(?im)^[ \t]*('
    r'#{1,6}[ \t]*'                              # markdown header
    r'|(?:\*\*)'                                 # or bold **
    r')'
    r'[ \t]*'
    r'('
    r'Filled(?:[ \t]+in)?[ \t]+Replace(?:s)?'    # Filled Replace / Filled in Replace / optional plural
    r'|Filled[ \t]+Replace[ \t]+Content'
    r'|Fill[ \t]+the[ \t]+replace[ \t]+content'
    r')'
    r'[ \t]*'
    r'(?:\*\*)?'                                 # optional ending ** for bold header
    r'[ \t]*'
    r'[:：]?[ \t]*$'
)

# 2) Plain-text headers (non-# / non-**)
PLAIN_HEADER_RE = re.compile(
    r'(?im)^[ \t]*'
    r'('
    r'Filled(?:[ \t]+in)?[ \t]+Replace(?:s)?'
    r'|Filled(?:[ \t]+in)?[ \t]+Replace[ \t]+Content'
    r'|Fill[ \t]+the[ \t]+replace[ \t]+content'
    r')'
    r'[ \t]*[:：][ \t]*$'
)

# 3) Section terminator: the next header line (# or **)
NEXT_SECTION_RE = re.compile(
    r'(?im)^[ \t]*(#{1,6}\s+|\*\*.+?\*\*\s*$)'
)


def sanitize_value(value: str) -> str:
    """Remove all double quotes (") from content to avoid interference in JSON usage."""
    return value.replace('"', '')


def extract_bracket_block(s: str, start_pos: int):
    """
    Starting from start_pos in string s (which should point to '['),
    extract the full matching [...] block, supporting nested brackets.
    Returns (content_inside, closing_bracket_index).
    Returns (None, None) if extraction fails.
    """
    if start_pos is None or start_pos < 0 or start_pos >= len(s) or s[start_pos] != "[":
        return None, None

    depth = 0
    i = start_pos
    content_start = start_pos + 1  # exclude the outer '['

    while i < len(s):
        ch = s[i]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return s[content_start:i], i
        i += 1

    return None, None


def parse_by_rule1_last(text: str):
    """
    Find all occurrences of "filled replace" and use the last one.
    Supported formats:
    - [ ... ]
    - " ... "
    - “ ... ”
    If extracted content is empty -> return "" (indicates empty new column).
    If not found -> return None.
    """
    matches = list(FILLED_REPLACE_ALL_RE.finditer(text))
    if not matches:
        return None

    m = matches[-1]  # use the last match
    opener_pos = m.end() - 1
    opener = text[opener_pos]

    # Case 1: list [...]
    if opener == "[":
        inside, _ = extract_bracket_block(text, opener_pos)
        if inside is None:
            return None
        value = inside.strip()

    # Case 2: English quotes "..."
    elif opener == '"':
        end = text.find('"', opener_pos + 1)
        if end == -1:
            return None
        value = text[opener_pos + 1:end].strip()

    # Case 3: Chinese quotes “...”
    elif opener == "“":
        end = text.find("”", opener_pos + 1)
        if end == -1:
            return None
        value = text[opener_pos + 1:end].strip()

    else:
        return None

    if value == "":
        return ""

    value = sanitize_value(value).strip()
    if value == "":
        return ""

    return json.dumps({"filled replace": value}, ensure_ascii=False)


def parse_by_rule2(text: str):
    """
    Detect Filled Replace section headers (# or **),
    and extract content until the next header.
    If extracted content is empty -> return "".
    If no header found -> return None.
    """
    m = HEADER_ANY_RE.search(text)
    if not m:
        m = PLAIN_HEADER_RE.search(text)
        if not m:
            return None

    start = m.end()
    rest = text[start:]

    end_m = NEXT_SECTION_RE.search(rest)
    block = rest[: end_m.start()] if end_m else rest

    value = block.strip()
    if value == "":
        return ""

    value = sanitize_value(value).strip()
    if value == "":
        return ""

    return json.dumps({"filled replace": value}, ensure_ascii=False)


def extract_filled_replace(text):
    """
    Main entry:
    - None / empty string: return as-is
    - Apply Rule 1 first (last JSON-style filled replace)
    - Then apply Rule 2 (section-based extraction)
    - If neither matches: return original text
    - If matched but empty: return "" (new column set to empty)
    """
    if text is None:
        return None
    if not isinstance(text, str):
        return text
    if text == "":
        return ""

    r1 = parse_by_rule1_last(text)
    if r1 is not None:
        return r1

    r2 = parse_by_rule2(text)
    if r2 is not None:
        return r2

    return text


def main(input_csv: str, output_csv: str):
    df = pd.read_csv(input_csv, encoding="utf-8-sig")

    for col in COLS:
        new_col = f"{col}_repaire"
        if col not in df.columns:
            df[new_col] = None
            continue
        df[new_col] = df[col].apply(extract_filled_replace)

    df.to_csv(output_csv, index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    input = r"your_path.csv"
    out = r"your_path.csv"
    main(input, out)
