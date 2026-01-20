import re
import json
import pandas as pd


def extract_solution_and_final(text: str) -> dict:
    """
    Goal:
    - Search backward from the end of the text to find the start marker
      of the "final answer" section
    - final answer: from the marker start to the end of the text (including the marker)
    - solution: from the beginning of the text to just before the marker

    Adapted examples:
    - Prefer matching real answer phrases like "The final answer is"
    - "### Final Answer" is usually just a heading and should not be treated
      as the start of the actual final answer section
    """
    if text is None:
        text = ""
    if not isinstance(text, str):
        text = str(text)

    # If empty or whitespace-only, return empty fields
    if text.strip() == "":
        return {"solution": "", "final answer": ""}

    # Markers ranked by how likely they indicate a true final answer section
    patterns = [
        # Most reliable: explicit final answer sentence
        re.compile(r"\bthe\s+final\s+answer\s+is\b\s*:?", re.IGNORECASE),

        # Next: some models use "Final answer:" as a paragraph start
        re.compile(r"\bfinal\s+answer\b\s*:?", re.IGNORECASE),

        # Less reliable: Therefore / Thus may introduce a concluding sentence
        re.compile(r"\btherefore\b\s*:?", re.IGNORECASE),
        re.compile(r"\bthus\b\s*:?", re.IGNORECASE),
    ]

    start_idx = None

    # Find the last occurrence of any marker (equivalent to scanning from the end)
    for pat in patterns:
        matches = list(pat.finditer(text))
        if matches:
            m = matches[-1]
            start_idx = m.start()
            break

    # No marker found: treat entire text as solution
    if start_idx is None:
        return {"solution": text, "final answer": ""}

    solution_part = text[:start_idx].rstrip()
    final_part = text[start_idx:].lstrip()

    return {"solution": solution_part, "final answer": final_part}


def repair_csv(input_csv_path: str, output_csv_path: str) -> None:
    # Read CSV as strings; keep empty cells as empty strings (do not convert to NaN)
    df = pd.read_csv(
        input_csv_path,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8-sig"
    )

    if "Model_Response" not in df.columns:
        raise ValueError("Column not found in input CSV: Model_Response")

    def to_json_str(s):
        # NaN: write empty
        if pd.isna(s):
            return ""
        if s.strip() == "Erro":
            return s

        if not isinstance(s, str):
            s = str(s)

        # Empty or whitespace-only: return as is
        if s.strip() == "":
            return s

        # Modification:
        # If the string starts with "{" after stripping leading whitespace,
        # assume it is already JSON and return it directly
        if s.lstrip().startswith("{"):
            return s

        obj = extract_solution_and_final(s)
        return json.dumps(obj, ensure_ascii=False)

    df["Model_Response_repair"] = df["Model_Response"].apply(to_json_str)
    df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    input = r"your_path.csv"
    output = r"your_path.csv"
    repair_csv(input, output)
