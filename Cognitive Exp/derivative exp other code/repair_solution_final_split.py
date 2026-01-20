import re
import json
import pandas as pd


def extract_solution_and_final(text: str) -> dict | None:
    if text is None:
        text = ""
    if not isinstance(text, str):
        text = str(text)

    if text.strip() == "":
        return None

    patterns = [
        re.compile(r"\bthe\s+final\s+answer\s+is\b\s*:?", re.IGNORECASE),
        re.compile(r"\bfinal\s+answer\b\s*:?", re.IGNORECASE),
        re.compile(r"\btherefore\b\s*:?", re.IGNORECASE),
        re.compile(r"\bthus\b\s*:?", re.IGNORECASE),
        re.compile(r"\bso\b\s*:?", re.IGNORECASE),
    ]

    start_idx = None
    for pat in patterns:
        matches = list(pat.finditer(text))
        if matches:
            start_idx = matches[-1].start()
            break

    # Core logic:
    # If no marker is matched, explicitly indicate "do not repair"
    if start_idx is None:
        return None

    solution_part = text[:start_idx].rstrip()
    final_part = text[start_idx:].lstrip()

    return {
        "solution": solution_part,
        "final answer": final_part,
    }


def repair_csv(
    input_csv_path: str,
    output_csv_path: str,
    cols_to_repair: list[str],
) -> None:
    # Read CSV, force all columns to string
    df = pd.read_csv(
        input_csv_path,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8-sig",
    )

    # Check whether required columns exist
    missing = [c for c in cols_to_repair if c not in df.columns]
    if missing:
        raise ValueError(f"Columns not found in input CSV: {missing}")

    def to_json_str(s):
        if pd.isna(s):
            return ""

        if not isinstance(s, str):
            s = str(s)

        if s.strip() == "":
            return s

        # Already JSON, keep as is
        if s.lstrip().startswith("{"):
            return s

        obj = extract_solution_and_final(s)

        # If no pattern matched, return the original text
        if obj is None:
            return s

        return json.dumps(obj, ensure_ascii=False)

    # Core logic: process multiple columns
    for col in cols_to_repair:
        new_col = f"{col}_repair"
        df[new_col] = df[col].apply(to_json_str)

    df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    input_csv = r"your_path.csv"
    output_csv = r"your_path.csv"

    cols = [
        "knowledge_redefinition_formula_calculation_Model_Response"
    ]

    repair_csv(input_csv, output_csv, cols)
