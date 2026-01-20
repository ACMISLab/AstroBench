import argparse
import json
import math
from typing import Optional, Any
import re

import pandas as pd


def is_empty_value(x: Any) -> bool:
    """Check whether a value is empty (NaN / None / empty string / whitespace-only)."""
    if x is None:
        return True
    # pandas NaN
    if isinstance(x, float) and math.isnan(x):
        return True
    if isinstance(x, str) and x.strip() == "":
        return True
    return False


def extract_target_json(text: str) -> Optional[str]:
    """
    Extract the last JSON-like block containing both
    "solution" and "final answer" from the text.
    The JSON does not need to be strictly valid; only structural extraction is performed.
    """
    if not isinstance(text, str):
        return None

    # Greedily match all {...} blocks
    matches = re.findall(r"\{[\s\S]*?\}", text)
    if not matches:
        return None

    # Search from the end to ensure the last occurrence
    for block in reversed(matches):
        if '"solution"' in block and '"final answer"' in block:
            return block.strip()

    return None


def repair_cell(x):
    if is_empty_value(x):
        return pd.NA

    if not isinstance(x, str):
        x = str(x)

    json_block = extract_target_json(x)
    if json_block is None:
        return x   # Return original value if nothing is found

    #Directly return the JSON block without attempting json.loads
    return json_block


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default=r"your_path.csv"
    )

    parser.add_argument(
        "--output",
        default=r"your_path.csv"
    )

    parser.add_argument(
        "--column",
        default="Model_Response"
    )
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    if output_path is None:
        if input_path.lower().endswith(".csv"):
            output_path = input_path[:-4] + "_repaired.csv"
        else:
            output_path = input_path + "_repaired.csv"

    df = pd.read_csv(input_path)

    if args.column not in df.columns:
        raise ValueError(
            f"Column not found: {args.column}. Existing columns: {list(df.columns)}"
        )

    df["Model_Response_repaie"] = df[args.column].apply(repair_cell)

    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Output written to: {output_path}")


if __name__ == "__main__":
    main()
