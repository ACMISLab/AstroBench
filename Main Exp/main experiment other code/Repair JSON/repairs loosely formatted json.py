import re
import json
import pandas as pd


def _strip_outer_quotes(s: str) -> str:
    if s is None:
        return ""
    s = s.strip()
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        return s[1:-1].strip()
    return s


def _find_key_span(text: str, key_regex: str):
    """
    Find the start of `key:` and the start position of its value
    (value_start = first position after the colon).
    Return (key_start, value_start), or None if not found.
    """
    m = re.search(rf'{key_regex}\s*:\s*', text, flags=re.IGNORECASE)
    if not m:
        return None
    return (m.start(), m.end())


def _clean_trailing_braces_commas(s: str) -> str:
    # Only clean trailing braces and commas at the end,
    # without touching braces inside the content.
    s = s.strip()
    s = re.sub(r'[\s,]*\}+\s*$', '', s)   # remove trailing one or more }
    s = re.sub(r'[\s,]+$', '', s)        # remove trailing commas/whitespace
    return s.strip()


def parse_bad_json_like(text: str):
    """
    More robust parsing rules:
    - The end boundary of `solution` can only be the `final answer` key
      (cannot rely on `}`).
    - The end boundary of `final answer` is the end of the text
      (then clean trailing `}`).
    - Values may be quoted or unquoted, multi-line, and may contain LaTeX braces.
    """
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return None

    raw = str(text)
    if not raw.strip():
        return None

    # Key regex (allow quoted or unquoted keys)
    solution_key = r'(?:\"solution\"|\'solution\'|solution)'
    final_key = r'(?:\"final\s+answer\"|\'final\s+answer\'|final\s+answer)'

    sol_pos = _find_key_span(raw, solution_key)
    fin_pos = _find_key_span(raw, final_key)

    # If neither key exists, return None (can be changed to {} if desired)
    if sol_pos is None and fin_pos is None:
        return None

    def extract_between(value_start: int, next_key_start: int | None):
        chunk = raw[value_start: next_key_start if next_key_start is not None else len(raw)]
        chunk = chunk.lstrip()

        if not chunk:
            return ""

        # If the value starts with a quote, try to find the matching quote (allow escapes)
        if chunk[0] in ('"', "'"):
            q = chunk[0]
            i, escaped = 1, False
            while i < len(chunk):
                ch = chunk[i]
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == q:
                    return chunk[1:i].strip()
                i += 1
            # If the quote is not closed, treat it as unquoted
            chunk = chunk[1:]

        # Unquoted value: return the whole chunk (post-processing will clean it)
        return chunk.strip()

    solution_val = ""
    final_val = ""

    # Extract solution: stop only at the `final answer` key (if it exists)
    if sol_pos is not None:
        _, sol_value_start = sol_pos
        fin_key_start = fin_pos[0] if fin_pos is not None else None
        solution_val = extract_between(sol_value_start, fin_key_start)

    # Extract final answer: go to the end of the text
    if fin_pos is not None:
        _, fin_value_start = fin_pos
        final_val = extract_between(fin_value_start, None)

    # Remove outer quotes
    solution_val = _strip_outer_quotes(solution_val)
    final_val = _strip_outer_quotes(final_val)

    # For solution: do not remove braces inside the content
    # Only clean trailing commas (optional)
    solution_val = re.sub(r'[\s,]+$', '', solution_val).strip()

    # For final answer: allow removing trailing braces/commas
    final_val = _clean_trailing_braces_commas(final_val)

    return {"solution": solution_val, "final answer": final_val}


def repair_model_response(text):
    """
    NaN -> keep as is
    Non-empty -> output a standard JSON string
    """
    if isinstance(text, float) and pd.isna(text):
        return text
    if text is None:
        return None
    if isinstance(text, str) and not text.strip():
        return text

    obj = parse_bad_json_like(text)
    if obj is None:
        # If keys cannot be parsed, return the original text (conservative behavior)
        return text

    return json.dumps(obj, ensure_ascii=False)


def process_csv(input_csv: str, output_csv: str):
    df = pd.read_csv(input_csv)

    if "Model_Response" not in df.columns:
        raise ValueError("Column does not exist in CSV: Model_Response")

    df["Model_Response_repire"] = df["Model_Response"].apply(repair_model_response)

    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    return df


if __name__ == "__main__":
    process_csv(
        input_csv=r"your_path.csv",
        output_csv=r"your_path.csv"
    )
