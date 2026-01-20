import json
import os

import pandas as pd
from openai import OpenAI
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback


def Result_Reasoning_Break_GPT5_1(Mask_Answer, Candidate_Answer):
    # Note: Mask_Answer is the ground-truth standard answer,
    # Candidate_Answer is the model-generated answer
    System_Prompt = f'''# Task Definition
You are a rigorous expert in astronomy, astrophysics, and mathematical reasoning.

There is an astronomy-related computational reasoning problem in which some intermediate solution steps were masked.
We now provide:
1. The ground-truth answer for the masked steps.
2. A model-generated completion for the masked steps.

Your task is to evaluate how well the model-generated completion matches the ground-truth answer.

# Evaluation guidelines:
- Focus on whether the reasoning logic, mathematical relationships, and physical meaning are consistent.
- Differences in wording, notation, or order of steps are acceptable as long as the reasoning and conclusions are logically equivalent.
- Deduct points if the completion contains incorrect reasoning, incorrect physical concepts, or non-equivalent conclusions.
- Deduct points if key steps present in the ground-truth answer are missing.
- Do NOT penalize valid equivalent derivations or reasonable additional explanations.

# Scoring rules:
- Score range: 0 to 10
- 10: Fully equivalent to the ground-truth answer in logic and conclusions
- 7–9: Mostly correct, with only minor non-critical differences
- 4–6: Partially correct, but with notable omissions or flaws
- 1–3: Mostly incorrect reasoning or inconsistent conclusions
- 0: Completely incorrect or unrelated

# Output format:
- Match Score: <numeric score from 0 to 10>
- Rationale: Brief explanation of the score.'''
    User_Prompt = f'''Now start your work.

Ground-truth Answer: """{Mask_Answer}"""

Model Completion: """{Candidate_Answer}"""'''
    answer = call_deepseek_v3_2(question=User_Prompt, system=System_Prompt)
    return answer


def call_deepseek_v3_2(question, system):
    model = "deepseek-chat"
    client = OpenAI(
        api_key="your_key",
        base_url="https://api.deepseek.com/v1"
    )

    response = client.chat.completions.create(
        model=model,
        temperature=1,  # Code generation / mathematical reasoning
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
        stream=False
    )

    return response.choices[0].message.content


def EVAL_ORI_Formula_Derivation(Model, input_csv_path, output_dir, type_index):
    # =========================
    # 1. Path configuration
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"eval_{Model}_Mid_mask_{type_index}.csv"
    )
    os.makedirs(output_dir, exist_ok=True)

    # =========================
    # 2. Load dataset
    # =========================
    df = pd.read_csv(input_csv_path)

    results = []

    # =========================
    # 3. Evaluate each sample
    # =========================
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        Mask_Answer = None if pd.isna(row['Test Mid Mask']) else row['Test Mid Mask'].strip()
        model_solution = None if pd.isna(row['Test Mid Step_Model_Response']) else row['Test Mid Step_Model_Response'].strip()
        difficulty = row['Difficulty']

        if Mask_Answer is None or Mask_Answer == "No Step":
            continue

        try:
            if model_solution is None or "unsolvable" in model_solution.lower():
                print(f"model_solution: {model_solution}")
                response = "**Match Score: 0**"
            else:
                response = Result_Reasoning_Break_GPT5_1(
                    Mask_Answer=Mask_Answer,
                    Candidate_Answer=model_solution
                )
        except json.JSONDecodeError as e:
            print(e)
            response = "**Match Score: 0**"

        print(response)

        # ---------- Save results ----------
        results.append({
            "Index": idx + 1,
            "Mid_Eval_Response": response,
            "Difficulty": difficulty,
        })

    # =========================
    # 4. Save results to CSV
    # =========================
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"Evaluation completed. Results saved to: {output_csv_path}")


def run_one(d):
    Model = d["Model"]
    input_csv_path = d["path"]
    type_index = d["type"]
    output_dir = r"your_path"

    EVAL_ORI_Formula_Derivation(
        Model=Model,
        input_csv_path=input_csv_path,
        output_dir=output_dir,
        type_index=type_index
    )
    return (Model, type_index, input_csv_path)


if __name__ == "__main__":
    max_concurrent = 3
    main_dir = r"your_path"

    data = [
        {
            "Model": "Qwen3VL_32B",
            "path": os.path.join(
                main_dir,
                "formula_derivation.csv"
            ),
            "type": "formula_derivation"
        }
    ]

    with ThreadPoolExecutor(max_workers=max_concurrent) as ex:
        futures = {ex.submit(run_one, d): d for d in data}

        for fut in as_completed(futures):
            d = futures[fut]
            try:
                res = fut.result()
                print(f"[DONE] {res[0]} | {res[1]} | {res[2]}")
            except Exception as e:
                print(f"[FAIL] {d['Model']} | {d['type']} | {d['path']}")
                print("".join(traceback.format_exception(type(e), e, e.__traceback__)))
