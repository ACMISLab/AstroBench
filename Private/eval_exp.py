import json
import os

import pandas as pd
from openai import OpenAI
from tqdm import tqdm

Closeai_key="xxx-xxx"
Closeai_url="https://api.openai-proxy.org/v1"

def call_closeai_gpt5_1_syetem(question,system):
    client = OpenAI(
        # openai系列的sdk，包括langchain，都需要这个/v1的后缀
        base_url=Closeai_url,
        api_key=Closeai_key,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question}
        ],
        model="gpt-5.1-2025-11-13", # 如果是其他兼容模型，比如deepseek，直接这里改模型名即可，其他都不用动
    )
    return chat_completion.choices[0].message.content

def Process_Evaluation_GPT5_1(question,Reference_Answer,Candidate_Answer):
    #注意Reference_Answer是我们自己的标准答案,Candidate_Answer是模型回复答案
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
    answer = call_closeai_gpt5_1_syetem(question=User_Prompt,system=Syetem_Prompt)
    return answer

def Result_Evaluation_GPT5_1(question,Reference_Answer,Candidate_Answer):
    #注意Reference_Answer是我们自己的标准答案,Candidate_Answer是模型回复答案
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
    answer = call_closeai_gpt5_1_syetem(question=User_Prompt,system=Syetem_Prompt)
    return answer

def Result_Reasoning_Break_GPT5_1(Mask_Answer,Candidate_Answer):
    #注意Mask_Answer是我们自己的标准答案,Candidate_Answer是模型回复答案
    Syetem_Prompt = f'''# Task Definition
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
    User_Prompt =f'''Now start your work.

Ground-truth Answer: """{Mask_Answer}"""

Model Completion: """{Candidate_Answer}"""'''
    answer = call_closeai_gpt5_1_syetem(question=User_Prompt,system=Syetem_Prompt)
    return answer

def EVAL_ORI_Computational_Reasoning(Model,Image_Flag,input_csv_path,output_dir):
    # =========================
    # 1. 路径配置（可按需修改）
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"eval_{Model}_ori_computational_reasoning.csv"
    )
    os.makedirs(output_dir, exist_ok=True)
    # =========================
    # 2. 读取数据集
    # =========================
    df = pd.read_csv(input_csv_path)

    results = []
    # =========================
    # 3. 逐条测试
    # =========================
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        question = row['Question'].strip()
        ori_solution = row['Solution'].strip()
        ori_result = row['Ori Final Answer'].strip()
        try:
            model_solution_json = row['Model_Response'].strip()
        except:
            model_solution_json = row['Model_Response']
        image_lable = row['Image Lable'].strip()
        difficulty = row['Difficulty']
        # ---------- 图像判断 ----------
        if Image_Flag:
            pass
        else:
            if row['Image Lable'] == 'Yes':
                Eval_Process=""
                Eval_result=""
            else:
                if model_solution_json == "No Json":
                    Eval_Process = 0
                    Eval_result = 0
                else:
                    try:
                        data = json.loads(model_solution_json)
                        model_solution=data['solution']
                        model_result=data['final answer']
                        Eval_Process = Process_Evaluation_GPT5_1(question=question,Reference_Answer=ori_solution,Candidate_Answer=model_solution)
                        Eval_result = Result_Evaluation_GPT5_1(question=question, Reference_Answer=ori_result, Candidate_Answer=model_result)

                        print(f"---------------Eval_Process---------------\n{Eval_Process}")
                        print(f"---------------Eval_result---------------\n{Eval_result}")
                    except:
                        Eval_Process = "Erro"
                        Eval_result = "Erro"
        # ---------- 记录结果 ----------
        results.append({
            "Index": idx+1,
            "Question": question,
            "Image Lable": image_lable,
            "Eval_Process": Eval_Process,
            "Eval_result": Eval_result,
            "Difficulty": difficulty,
        })
    # =========================
    # 4. 保存为 CSV
    # =========================
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"✅ 测试完成，结果已保存至: {output_csv_path}")

def EVAL_ORI_Formula_Calculationg(Model,input_csv_path,output_dir):
    # =========================
    # 1. 路径配置（可按需修改）
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"eval_{Model}_ori_formula_calculationg.csv"
    )
    os.makedirs(output_dir, exist_ok=True)
    # =========================
    # 2. 读取数据集
    # =========================
    df = pd.read_csv(input_csv_path)

    results = []
    # =========================
    # 3. 逐条测试
    # =========================
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        question = row['Question'].strip()
        ori_solution = row['Solution'].strip()
        ori_result = row['Ori Final Answer'].strip()
        try:
            model_solution_json = row['Model_Response'].strip()
        except:
            model_solution_json = row['Model_Response']
        difficulty = row['Difficulty']
        # ---------- 图像判断 ----------

        if model_solution_json == "No Json":
            Eval_Process = 0
            Eval_result = 0
        else:
            try:
                data = json.loads(model_solution_json)
                model_solution=data['solution']
                model_result=data['final answer']
                Eval_Process = Process_Evaluation_GPT5_1(question=question,Reference_Answer=ori_solution,Candidate_Answer=model_solution)
                Eval_result = Result_Evaluation_GPT5_1(question=question, Reference_Answer=ori_result, Candidate_Answer=model_result)

                print(f"---------------Eval_Process---------------\n{Eval_Process}")
                print(f"---------------Eval_result---------------\n{Eval_result}")
            except:
                Eval_Process = "Erro"
                Eval_result = "Erro"
        # ---------- 记录结果 ----------
        results.append({
            "Index": idx+1,
            "Question": question,
            "Eval_Process": Eval_Process,
            "Eval_result": Eval_result,
            "Difficulty": difficulty,
        })
    # =========================
    # 4. 保存为 CSV
    # =========================
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"✅ 测试完成，结果已保存至: {output_csv_path}")

