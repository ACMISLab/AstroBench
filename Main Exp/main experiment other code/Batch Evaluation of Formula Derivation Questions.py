
import json
import os

import pandas as pd
from openai import OpenAI
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback


def Process_Evaluation_GPT5_1(question,Reference_Answer,Candidate_Answer):
    # Please note that Reference_Answer is our standard answer, and Candidate_Answer is the model's response.
    Syetem_Prompt = f'''# Task Definition
You are an expert evaluator. You are given: Question, Reference Solution and Candidate Solution. Your task is to evaluate how well the Candidate Solution matches the Reference Solution.

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
    -Penalize only if it is incorrect or misleading.
    -Be objective and consistent across evaluations.'''
    User_Prompt =f'''Now start your work.

Question: "{question}".

Reference Answer: """{Reference_Answer}""".

Candidate Answer: """{Candidate_Answer}""".'''
    answer = call_deepseek_v3_2(question=User_Prompt,system=Syetem_Prompt)
    return answer

def Result_Evaluation_GPT5_1(question,Reference_Answer,Candidate_Answer):
    #Please note that Reference_Answer is our standard answer, and Candidate_Answer is the model's response.
    Syetem_Prompt = f'''You are an expert evaluator. You are given: Question, Reference Answer and Candidate Answer. Your task is to determine whether the Candidate Answer is truly consistent with the Reference Answer.

Consistency means semantic equivalence, not superficial similarity. Please follow these rules carefully:

1. If the Candidate Answer and the Reference Answer express the same meaning, they should be considered consistent, even if:
    The wording, structure, or format is different
    One is more concise or more verbose than the other
    One uses synonyms, paraphrases, or different sentence structures

2. If the answers involve numerical values, they should be considered consistent if:
    The values are equal
    Or the difference is within a reasonable or explicitly acceptable error tolerance
    Or one is an approximation of the other with the same underlying meaning

3. The Candidate Answer should be marked inconsistent if:
    It contradicts the Reference Answer
    It misses key information that changes the meaning
    It introduces incorrect facts or conclusions

4. Do not judge based on style, grammar, or formatting alone. Focus only on whether the final expressed meaning and correctness match.

Output only one of the following labels: `Consistent` or `Inconsistent`
Do not provide explanations or additional text.'''
    User_Prompt =f'''Now start your work.

Question: "{question}".

Reference Answer: """{Reference_Answer}""".

Candidate Answer: """{Candidate_Answer}""".'''
    answer = call_deepseek_v3_2(question=User_Prompt,system=Syetem_Prompt)
    return answer

def call_deepseek_v3_2(question,system):
    model="deepseek-chat"
    client = OpenAI(
        api_key="api_key",
        base_url="https://api.deepseek.com/v1")

    response = client.chat.completions.create(
        model=model,
        temperature=1,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
        stream=False
    )

    return response.choices[0].message.content

def EVAL_ORI_Formula_Derivation(Model,Image_Flag,input_csv_path,output_dir,index_type):
    # =========================
    # 1. Path configuration (can be modified as needed)
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"eval_{Model}_{index_type}_formula_derivation.csv"
    )
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(input_csv_path)

    has_difficulty = "Difficulty" in df.columns

    results = []
    # =========================
    # 3. Test each item individually.
    # =========================
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        question = row['Question'].strip()
        ori_solution = row['Solution'].strip()
        # model_solution = row['Model_Response'].strip()
        value = row['Model_Response']
        if isinstance(value, str):
            model_solution = value.strip()
        else:
            model_solution = ''
        image_lable = row['Image Lable'].strip()
        difficulty = row["Difficulty"] if has_difficulty else ""
        # ---------- 图像判断 ----------
        if Image_Flag:
            pass
        else:
            if row['Image Lable'] == 'Yes':
                # response = Process_Evaluation_GPT5_1(question=question, Reference_Answer=ori_solution,
                #                                      Candidate_Answer=model_solution)
                continue
            else:
                response = Process_Evaluation_GPT5_1(question=question,Reference_Answer=ori_solution,Candidate_Answer=model_solution)
                print(response)
        # ---------- 记录结果 ----------
        results.append({
            "Index": idx+1,
            "Question": question,
            "Image Lable": image_lable,
            "Eval_Response": response,
            "Difficulty": difficulty,
        })

    result_df = pd.DataFrame(results)
    result_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"Testing complete, results saved to: {output_csv_path}")


def run_one(d):
    Model = d["Model"]
    input_csv_path = d["path"]
    output_dir = r"your_path"
    index_type = d["index"]

    EVAL_ORI_Formula_Derivation(
        Model=Model,
        Image_Flag=False,
        input_csv_path=input_csv_path,
        output_dir=output_dir,
        index_type=index_type
    )
    return (Model, index_type, input_csv_path)

if __name__ == "__main__":
    max_concurrent = 1
    data=[
        {
            "Model": "AstroOne",
            "path": r"your_path",
            "index": "Think"
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
                print(f"[FAIL] {d['Model']} | {d['index']} | {d['path']}")
                print("".join(traceback.format_exception(type(e), e, e.__traceback__)))