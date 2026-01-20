import pandas as pd
import os


def run(input_csv_path, outName):
    output_dir = r"your_path"
    output_csv_path = os.path.join(
        output_dir, f"Accuracy_{outName}.csv"
    )

    df = pd.read_csv(input_csv_path)

    required_columns = [
        "Difficulty",
        "Test Shuffle Question Word_Model_Response"
    ]
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    new_df = pd.DataFrame()
    new_df["Difficulty"] = df["Difficulty"]

    def compute_score(x):
        # Assign 10 points if the response contains "unsolvable" (case-insensitive), otherwise 0
        if pd.isna(x):
            return 0
        return 10 if "unsolvable" in str(x).lower() else 0

    # Compute score
    new_df["score"] = df["Test Shuffle Question Word_Model_Response"].apply(compute_score)

    # Compute accuracy (percentage)
    total_count = len(new_df)
    ten_count = (new_df["score"] == 10).sum()
    accuracy = (ten_count / total_count * 100) if total_count > 0 else 0

    # Add Accuracy column (value only in the first row)
    new_df["Accuracy"] = None
    new_df.loc[0, "Accuracy"] = f"{accuracy:.2f}%"

    # Reorder columns
    new_df = new_df[["score", "Difficulty", "Accuracy"]]

    new_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print("Processing completed. New file generated:", output_csv_path)


def extract_name(filename: str) -> str:
    return filename.replace("all_result_", "").replace(".csv", "")


if __name__ == "__main__":
    input_dir = r"your_path"
    data = [
        {
            "path": os.path.join(input_dir, "computational_reasoning.csv"),
            "index": extract_name("computational_reasoning.csv")
        }
    ]
    for d in data:
        run(d["path"], d["index"])
