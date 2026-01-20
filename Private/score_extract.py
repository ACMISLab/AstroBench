import pandas as pd
import re
from pathlib import Path

def extract_scores(text):
    scores = {
        'Overall Score': 0,
        'Correctness': 0,
        'Completeness': 0,
        'Relevance': 0,
        'Clarity & Coherence': 0,
        'Precision & Detail': 0
    }

    if pd.isna(text) or str(text).strip().lower() in ['0', 'Erro', '']:
        return scores

    text = str(text)

    overall_match = re.search(r'Overall Score:\s*(\d+(?:\.\d+)?)', text)
    if overall_match:
        scores['Overall Score'] = float(overall_match.group(1))
    categories = ['Correctness', 'Completeness', 'Relevance', 'Clarity & Coherence', 'Precision & Detail']
    for category in categories:
        pattern = category.replace('&', r'&')
        match = re.search(fr'{pattern}:\s*(\d+(?:\.\d+)?)', text)
        if match:
            scores[category] = float(match.group(1))

    return scores


def process_csv_to_excel(input_csv, output_excel, text_column):

    df = pd.read_csv(input_csv)

    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' does not exist in the CSV file.")

    result_columns = ['Overall Score', 'Correctness', 'Completeness', 'Relevance',
                      'Clarity & Coherence', 'Precision & Detail']

    for col in result_columns:
        df[col] = 0.0

    for idx, row in df.iterrows():
        text_content = row[text_column]
        scores = extract_scores(text_content)

        for col in result_columns:
            df.at[idx, col] = scores[col]

    df.to_excel(output_excel, index=False)

    print(f"Processing complete! The results have been saved to:{output_excel}")
    print(f"A total of {len(df)} rows of data were processed.")

if __name__ == "__main__":
    input_dir = Path(r"your_Folder_path")
    output_dir = Path(r"your_Folder_path")
    output_dir.mkdir(parents=True, exist_ok=True)

    text_column_name = "Eval_Redudant_condition_Process"

    try:
        csv_files = sorted(input_dir.glob("*.csv"))
        if not csv_files:
            print(f"No CSV files found in: {input_dir}")
        else:
            print(f"{len(csv_files)} CSV files found, starting processing...")

        for csv_path in csv_files:
            output_excel_path = output_dir / (csv_path.stem + ".xlsx")

            try:
                process_csv_to_excel(
                    input_csv=str(csv_path),
                    output_excel=str(output_excel_path),
                    text_column=text_column_name
                )
                print(f"[OK] {csv_path.name} -> {output_excel_path.name}")

            except FileNotFoundError:
                print(f"[Skip] File not found:{csv_path}")
            except Exception as e:
                print(f"[Failure] Error processing {csv_path.name}:{e}")

        print("All processing is complete.")

    except Exception as e:
        print(f"An error occurred during the traversal or processing: {e}")

