import argparse
import math
from typing import Optional, Any, List

import pandas as pd


def is_empty_value(x: Any) -> bool:
    """Check whether a value is empty (NaN / None / empty string / whitespace-only)."""
    if x is None:
        return True
    if isinstance(x, float) and math.isnan(x):
        return True
    if isinstance(x, str) and x.strip() == "":
        return True
    return False


def find_balanced_brace_blocks(text: str) -> List[str]:
    """
    Extract all balanced curly-brace {...} blocks from text, supporting nesting.
    Curly braces inside strings are ignored, and escaped quotes (\") are handled.
    """
    blocks = []
    if not isinstance(text, str) or not text:
        return blocks

    depth = 0
    start = None
    in_string = False
    escape = False

    for i, ch in enumerate(text):
        if escape:
            escape = False
            continue

        if ch == "\\":
            escape = True
            continue

        if ch == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    blocks.append(text[start:i + 1])
                    start = None

    return blocks


def extract_target_json(text: str) -> Optional[str]:
    """
    Extract the last JSON-like block that contains both "solution" and "final answer".
    The block does not need to be strictly valid JSON; only structural extraction
    with balanced braces is required.
    """
    if not isinstance(text, str):
        return None

    blocks = find_balanced_brace_blocks(text)
    if not blocks:
        return None

    for block in reversed(blocks):
        if '"solution"' in block and '"final answer"' in block:
            return block.strip()

    return None


def repair_cell(x: Any) -> Any:
    if is_empty_value(x):
        return pd.NA

    if not isinstance(x, str):
        x = str(x)

    json_block = extract_target_json(x)
    if json_block is None:
        return x  # Return original value if no valid block is found

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
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    if output_path is None:
        if input_path.lower().endswith(".csv"):
            output_path = input_path[:-4] + "_repaired.csv"
        else:
            output_path = input_path + "_repaired.csv"

    df = pd.read_csv(input_path)

    target_cols = [
        "Test Redudant Background Question_Model_Response",
        "Test Redudant Conditions Question_Model_Response",
        "Test Shuffle Question Sentence_Model_Response"
    ]

    missing = [c for c in target_cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing columns: {missing}. "
            f"Available columns are: {list(df.columns)}"
        )

    for col in target_cols:
        df[col + "_repaired"] = df[col].apply(repair_cell)

    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Output written to: {output_path}")


if __name__ == "__main__":
    main()
