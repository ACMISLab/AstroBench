
import json
import os

import pandas as pd
from openai import OpenAI
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback


def Process_Evaluation_GPT5_1(question, Reference_Answer, Candidate_Answer):
    # Note: Reference_Answer is the ground-truth solution,
    # Candidate_Answer is the model-generated solution
    System_Prompt = f'''# Task Definition
You are an expert evaluator. You are given: Question, Reference Solution and Candidate Solution.
Your task is to evaluate how well the Candidate Solution matches the Reference Solution.

# Evaluation Criteria
Evaluate the Candidate Answer based on the following dimensions:

1. Correctness
   Are the core facts, logic, and conclusions consistent with the Reference Solution?
   Are there any factual errors or incorrect reasoning?

2. Completeness
   Does the Candidate Answer cover all key points present in the Reference Solution?
   Are any important elements missing?

3. Relevance
   Is the solution focused on the question?
   Does it avoid unnecessary or irrelevant information?

4. Clarity & Coherence
   Is the solution well-structured and easy to understand?
   Are explanations clear and logically connected?

5. Precision & Detail
   Does the level of detail appropriately match the Reference Solution?
   Are concepts expressed accurately without being vague or misleading?

# Scoring Instructions
Assign a numerical score from 0 to 10, where:
9–10: Excellent match; nearly identical in meaning and quality
7–9: Minor omissions or slight inaccuracies, but overall correct
6–7: Partially correct; important details missing or unclear
4–6: Significant errors or gaps; only some correct aspects
0–4: Mostly incorrect, irrelevant, or misleading

Use fine-grained judgment. Do not round scores unnecessarily.

# Output Format
Provide your evaluation strictly in the following format:
```
Overall Score: <numeric score from 0 to 10>
Evaluation:
- Correctness: <numeric score from 0 to 10>
- Completeness: <numeric score from 0 to 10>
- Relevance: <numeric score from 0 to 10>
- Clarity & Coherence: <numeric score from 0 to 10>
- Precision & Detail: <numeric score from 0 to 10>

Overall Justification:
<Concise explanation of why this score was assigned>
```

# Important Notes
Base your evaluation only on the provided Question, Reference Solution, and Candidate Solution.
Do not reward stylistic differences unless they affect clarity or correctness.
If the Candidate Solution introduces new information not present in the Reference Solution:
- Penalize only if it is incorrect or misleading.
- Be objective and consistent across evaluations.
'''
    User_Prompt = f'''Now start your work.

Question: "{question}".

Reference Answer: """{Reference_Answer}""".

Candidate Answer: """{Candidate_Answer}""".
'''
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


def EVAL_ORI_Formula_Derivation(Model, input_csv_path, output_dir):
    # =========================
    # 1. Path configuration
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"eval_{Model}_Redundant_Background_formula_derivation.csv"
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
        question = None if pd.isna(row['Test Redundant Background Question']) else row['Test Redundant Background Question'].strip()
        ori_solution = row['Test Ori Solution'].strip()
        model_solution = None if pd.isna(row['Test Redundant Background Question_Model_Response']) else row['Test Redundant Background Question_Model_Response'].strip()
        difficulty = row['Difficulty']

        if model_solution is None or question is None or "unsolvable" in model_solution.lower():
            response = (
                "Overall Score: 0 \n"
                "Evaluation:\n"
                "- Correctness: 0 \n"
                "- Completeness: 0 \n"
                "- Relevance: 0 \n"
                "- Clarity & Coherence: 0 \n"
                "- Precision & Detail: 0"
            )
        else:
            response = Process_Evaluation_GPT5_1(
                question=question,
                Reference_Answer=ori_solution,
                Candidate_Answer=model_solution
            )

        print(response)

        # ---------- Save results ----------
        results.append({
            "Index": idx + 1,
            "Question": question,
            "Eval_Response": response,
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
    output_dir = r"your_path"

    EVAL_ORI_Formula_Derivation(
        Model=Model,
        input_csv_path=input_csv_path,
        output_dir=output_dir
    )
    return (Model, input_csv_path)


if __name__ == "__main__":
    max_concurrent = 2
    main_dir = r"your_path"

    data = [
        {
            "Model": "AstroSage3_8B",
            "path": os.path.join(main_dir, "formula_derivation.csv")
        }
    ]

    with ThreadPoolExecutor(max_workers=max_concurrent) as ex:
        futures = {ex.submit(run_one, d): d for d in data}

        for fut in as_completed(futures):
            d = futures[fut]
            try:
                res = fut.result()
                print(f"[DONE] {res[0]} | {res[1]}")
            except Exception as e:
                print(f"[FAIL] {d['Model']} | {d['path']}")
                print("".join(traceback.format_exception(type(e), e, e.__traceback__)))
