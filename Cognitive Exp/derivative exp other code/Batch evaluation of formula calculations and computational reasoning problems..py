import json
import os
import pandas as pd
from openai import OpenAI
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback


def Process_Evaluation_GPT5_1(question, Reference_Answer, Candidate_Answer):
    # Note: Reference_Answer is the ground-truth answer, Candidate_Answer is the model-generated answer
    System_Prompt = f'''# Task Definition
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


def Result_Evaluation_GPT5_1(question, Reference_Answer, Candidate_Answer):
    # Note: Reference_Answer is the ground-truth answer, Candidate_Answer is the model-generated answer
    System_Prompt = f'''You are an expert evaluator. You are given: Question, Reference Answer and Candidate Answer. Your task is to determine whether the Candidate Answer is truly consistent with the Reference Answer.

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
Do not provide explanations or additional text.
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
        temperature=1,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
        stream=False
    )

    return response.choices[0].message.content


def EVAL_ORI_Computational_Reasoning(Model, input_csv_path, output_dir, type_index):
    # =========================
    # 1. Path configuration
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"eval_{Model}_shuffle_{type_index}.csv"
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
        ori_result = row['Test Ori Final Answer'].strip()
        difficulty = row['Difficulty']

        Redundant_Background_Question = None if pd.isna(row['Test Redundant Background Question']) else row['Test Redundant Background Question'].strip()
        Redundant_Background_Model_Response = None if pd.isna(row['Test Redundant Background Question_Model_Response']) else row['Test Redundant Background Question_Model_Response'].strip()

        Redundant_Condition_Question = None if pd.isna(row['Test Redundant Conditions Question']) else row['Test Redundant Conditions Question'].strip()
        Redundant_Condition_Model_Response = None if pd.isna(row['Test Redundant Conditions Question_Model_Response']) else row['Test Redundant Conditions Question_Model_Response'].strip()

        Shuffle_Question_Sentence = None if pd.isna(row['Test Shuffle Question Sentence']) else row['Test Shuffle Question Sentence'].strip()
        Shuffle_Question_Sentence_Model_Response = None if pd.isna(row['Test Shuffle Question Sentence_Model_Response']) else row['Test Shuffle Question Sentence_Model_Response'].strip()

        try:
            if Redundant_Background_Question is None or Redundant_Background_Model_Response in [None, "Error"]:
                Eval_Redundant_Background_Process = "Error"
                Eval_Redundant_Background_Result = "Error"
            else:
                data = json.loads(Redundant_Background_Model_Response)
                model_solution = data['solution']
                model_result = data['final answer']
                Eval_Redundant_Background_Process = Process_Evaluation_GPT5_1(
                    question=Redundant_Background_Question,
                    Reference_Answer=ori_result,
                    Candidate_Answer=model_solution
                )
                Eval_Redundant_Background_Result = Result_Evaluation_GPT5_1(
                    question=Redundant_Background_Question,
                    Reference_Answer=ori_result,
                    Candidate_Answer=model_result
                )
        except json.JSONDecodeError:
            Eval_Redundant_Background_Process = "Error"
            Eval_Redundant_Background_Result = "Error"

        try:
            if Redundant_Condition_Question is None or Redundant_Condition_Model_Response in [None, "Error"]:
                Eval_Redundant_Condition_Process = "Error"
                Eval_Redundant_Condition_Result = "Error"
            else:
                data = json.loads(Redundant_Condition_Model_Response)
                model_solution = data['solution']
                model_result = data['final answer']
                Eval_Redundant_Condition_Process = Process_Evaluation_GPT5_1(
                    question=Redundant_Condition_Question,
                    Reference_Answer=ori_result,
                    Candidate_Answer=model_solution
                )
                Eval_Redundant_Condition_Result = Result_Evaluation_GPT5_1(
                    question=Redundant_Condition_Question,
                    Reference_Answer=ori_result,
                    Candidate_Answer=model_result
                )
        except json.JSONDecodeError:
            Eval_Redundant_Condition_Process = "Error"
            Eval_Redundant_Condition_Result = "Error"

        try:
            if Shuffle_Question_Sentence is None or Shuffle_Question_Sentence_Model_Response in [None, "Error"]:
                Eval_Shuffle_Process = "Error"
                Eval_Shuffle_Result = "Error"
            else:
                data = json.loads(Shuffle_Question_Sentence_Model_Response)
                model_solution = data['solution']
                model_result = data['final answer']
                Eval_Shuffle_Process = Process_Evaluation_GPT5_1(
                    question=Shuffle_Question_Sentence,
                    Reference_Answer=ori_result,
                    Candidate_Answer=model_solution
                )
                Eval_Shuffle_Result = Result_Evaluation_GPT5_1(
                    question=Shuffle_Question_Sentence,
                    Reference_Answer=ori_result,
                    Candidate_Answer=model_result
                )
        except json.JSONDecodeError:
            Eval_Shuffle_Process = "Error"
            Eval_Shuffle_Result = "Error"

        results.append({
            "Index": idx + 1,
            "Eval_Redundant_Background_Process": Eval_Redundant_Background_Process,
            "Eval_Redundant_Background_Result": Eval_Redundant_Background_Result,
            "Eval_Redundant_Condition_Process": Eval_Redundant_Condition_Process,
            "Eval_Redundant_Condition_Result": Eval_Redundant_Condition_Result,
            "Eval_Shuffle_Question_Sentence_Process": Eval_Shuffle_Process,
            "Eval_Shuffle_Question_Sentence_Result": Eval_Shuffle_Result,
            "Difficulty": difficulty,
        })

    # =========================
    # 4. Save results
    # =========================
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"Evaluation finished. Results saved to: {output_csv_path}")


def run_one(config):
    Model = config["Model"]
    input_csv_path = config["path"]
    output_dir = r"D:\ComputationalReasoning\Evaluation\Supplement\DerivedResults"
    index_type = config["index"]

    EVAL_ORI_Computational_Reasoning(
        Model=Model,
        input_csv_path=input_csv_path,
        output_dir=output_dir,
        type_index=index_type
    )
    return (Model, index_type, input_csv_path)


if __name__ == "__main__":
    max_concurrent = 10
    base_dir = r"your_path"
    data = [
        {
            "Model": "llama_3_1_8b",
            "path": os.path.join(base_dir, "computational_reasoning.csv"),
            "index": "computational_reasoning"
        }
    ]

    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        futures = {executor.submit(run_one, d): d for d in data}

        for future in as_completed(futures):
            config = futures[future]
            try:
                result = future.result()
                print(f"[DONE] {result[0]} | {result[1]} | {result[2]}")
            except Exception as e:
                print(f"[FAIL] {config['Model']} | {config['index']} | {config['path']}")
                print("".join(traceback.format_exception(type(e), e, e.__traceback__)))
