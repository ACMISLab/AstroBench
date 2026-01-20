import os
import glob
import pandas as pd


def run(input, output):
    # =========================
    # Configuration section: customize paths / patterns here
    # =========================
    INPUT_GLOB = input
    OUTPUT_DIR = r"your_path"      # Output directory
    OUTPUT_SUFFIX = output         # Output file name
    ENCODING = None                # Set encoding if needed: "utf-8", "utf-8-sig", "gbk"

    # Column names to read/use
    COL_DIFFICULTY = "Difficulty"
    COL_ORI_ANSWER = "Test Ori Answer"
    COL_MISS_RESP = "Test Condition Miss Question_Model_Response"
    COL_DMG_RESP = "Test Condition Damage Question_Model_Response"

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    def _normalize_series_str(s: pd.Series) -> pd.Series:
        # Convert to string and strip whitespace; keep NaN as NaN
        return s.where(~s.isna(), other=pd.NA).astype("string").str.strip()

    def _contains_unsolvable(s: pd.Series) -> pd.Series:
        # Case-insensitive check for the substring "Unsolvable"
        s2 = _normalize_series_str(s)
        return s2.str.contains("Unsolvable", case=False, na=False)

    def _pick_column(df: pd.DataFrame, base_name: str) -> str:
        """
        Handle duplicated column names:
        pandas may rename duplicates as base_name, base_name.1, base_name.2, ...
        Prefer exact match; otherwise return the first column starting with base_name.
        """
        if base_name in df.columns:
            return base_name
        candidates = [c for c in df.columns if c == base_name or c.startswith(base_name + ".")]
        if candidates:
            return candidates[0]
        raise KeyError(f"Column not found: {base_name}. Existing columns: {list(df.columns)}")

    unprocessable_files = []
    processed_files = []

    for path in sorted(glob.glob(INPUT_GLOB)):
        try:
            # Read CSV
            df = pd.read_csv(path, encoding=ENCODING) if ENCODING else pd.read_csv(path)

            # Resolve possible duplicated column names
            col_diff = _pick_column(df, COL_DIFFICULTY)
            col_ori = _pick_column(df, COL_ORI_ANSWER)
            col_miss = _pick_column(df, COL_MISS_RESP)
            col_dmg = _pick_column(df, COL_DMG_RESP)

            # Check if file is processable:
            # Test Ori Answer must be entirely "Unsolvable" (case-insensitive)
            ori = _normalize_series_str(df[col_ori])
            is_all_unsolvable = ori.str.fullmatch(r"(?i)Unsolvable", na=False).all()

            if not is_all_unsolvable:
                unprocessable_files.append(os.path.basename(path))
                continue

            # Processable: generate output table
            miss_score = _contains_unsolvable(df[col_miss]).map(lambda x: "10" if x else "0")
            dmg_score = _contains_unsolvable(df[col_dmg]).map(lambda x: "10" if x else "0")

            out_df = pd.DataFrame({
                "Miss Question_score": miss_score,
                "Condition Damage Question_score": dmg_score,
                "Difficulty": df[col_diff],  # Direct copy
            })

            # Output path
            out_path = os.path.join(OUTPUT_DIR, OUTPUT_SUFFIX)

            # Write CSV (utf-8-sig is Excel-friendly)
            out_df.to_csv(out_path, index=False, encoding="utf-8-sig")
            processed_files.append(os.path.basename(path))

        except Exception as e:
            # Any read/write/column error marks the file as unprocessable
            unprocessable_files.append(os.path.basename(path))
            print(f"[ERROR] Processing failed: {path}\n  -> {e}")

    # Print summary of unprocessable files
    print("\n==== Unprocessable files ====")
    if unprocessable_files:
        for name in unprocessable_files:
            print(name)
    else:
        print("(None)")

    # Print summary of processed files
    print("\n==== Processed files ====")
    if processed_files:
        for name in processed_files:
            print(name)
    else:
        print("(None)")


if __name__ == "__main__":
    input = r"your_path"
    word = "shuffle_word_"
    data = [
        {
            "input_csv_path": os.path.join(input, "condition_computational_reasoning.csv"),
            "output_csv_path": f"{word}condition_computational_reasoning.csv"
        }
    ]
    for d in data:
        run(d["input_csv_path"], d["output_csv_path"])
