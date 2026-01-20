import json
import os
import pandas as pd
from tqdm import tqdm
from AstroMath.config import call_deepseek_v3_2,call_closeai_gpt5_1_syetem,call_qwen3_max_syetem,call_closeai_gpt5_1_syetem,call_AstroOne,call_qwen2_5_math_72b_syetem

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

def DeepSeek_V3_2_Formula_Derivation(question,system,model):
    prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. You need to solve this problem and provide the problem-solving process.

Now, here is your question: "{question}"'''
    answer = call_deepseek_v3_2(question=prompt,model=model,system=system)
    return answer

def ChatGPT_V5_1_Formula_Derivation(question,system):
    prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. You need to solve this problem and provide the problem-solving process.

Now, here is your question: "{question}"'''
    answer = call_closeai_gpt5_1_syetem(question=prompt,system=system)
    return answer

def AstroOne_Formula_Derivation(question,system,model):
    prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. You need to solve this problem and provide the problem-solving process. Let's think step by step.

Now, here is your question: "{question}"'''
    answer = call_AstroOne(question=prompt,model=model,system=system)
    return answer

def AstroOne_Formula_Calculationg(question,system,model):
    prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. 
You need to solve this problem and provide the problem-solving process and the final result. Let's think step by step.

# Output Format
{{
  "solution": "Fill in the problem-solving process here",
  "final answer": "Only fill in the final result to the question here, no additional steps are needed."
}}

Now, here is your question: "{question}"'''
    answer = call_AstroOne(question=prompt,model=model,system=system)
    return answer

def DeepSeek_V3_2_Computational_Reasoning(question,system,model):
    prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. 
You need to solve this problem and provide the problem-solving process and the final result. 

# Output Format
{{
  "solution": "Fill in the problem-solving process here",
  "final answer": "Only fill in the final result to the question here, no additional steps are needed."
}}

Now, here is your question: "{question}"'''
    answer = call_deepseek_v3_2(question=prompt,model=model,system=system)
    return answer

def AstroOne_Computational_Reasoning(question,system,model):
    prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. 
You need to solve this problem and provide the problem-solving process and the final result. Let's think step by step.

# Output Format
{{
  "solution": "Fill in the problem-solving process here",
  "final answer": "Only fill in the final result to the question here, no additional steps are needed."
}}

Now, here is your question: "{question}"'''
    answer = call_AstroOne(question=prompt,model=model,system=system)
    return answer

def DeepSeek_V3_2_Formula_Calculationg(question,system,model):
    prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. 
You need to solve this problem and provide the problem-solving process and the final result. 

# Output Format
{{
  "solution": "Fill in the problem-solving process here",
  "final answer": "Only fill in the final result to the question here, no additional steps are needed."
}}

Now, here is your question: "{question}"'''
    answer = call_deepseek_v3_2(question=prompt,model=model,system=system)
    return answer

def AstroOne_Code(question,system,model):
    prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. 
You need to solve this problem by writing python code and return the final result. Python code must be executable.

# Output Format
```python
def execute_code():
    # Code to solve the problem
         <codes>
    # final result return
    return result
```

Now, here is your question: "{question}"'''
    answer = call_AstroOne(question=prompt,model=model,system=system)
    return answer

def Qwen2_5_Math_72b_Computational_Reasoning(question,system):
    prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. 
You need to solve this problem and provide the problem-solving process and the final result.

# Output Format
{{
  "solution": "Fill in the problem-solving process here",
  "final answer": "Only fill in the final result to the question here, no additional steps are needed."
}}

Now, here is your question: "{question}"'''
    answer = call_qwen2_5_math_72b_syetem(question=prompt,system=system)
    return answer

def Qwen2_5_Math_72b_Formula_Derivation(question,system):
    prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. You need to solve this problem and provide the problem-solving process.

Now, here is your question: "{question}"'''
    answer = call_qwen2_5_math_72b_syetem(question=prompt,system=system)
    return answer

def Qwen2_5_Math_72b_Formula_Calculationg(question,system):
    prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. 
You need to solve this problem and provide the problem-solving process and the final result.

# Output Format
{{
  "solution": "Fill in the problem-solving process here",
  "final answer": "Only fill in the final result to the question here, no additional steps are needed."
}}

Now, here is your question: "{question}"'''
    answer = call_qwen2_5_math_72b_syetem(question=prompt,system=system)
    return answer

def Qwen2_5_Math_72b_Code(question,system):
    prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. 
You need to solve this problem by writing python code and return the final result. Python code must be executable.

# Output Format
```python
def execute_code():
    # Code to solve the problem
         <codes>
    # final result return
    return result
```

Now, here is your question: "{question}"'''
    answer = call_qwen2_5_math_72b_syetem(question=prompt,system=system)
    return answer


#-------------------------------------------------------------------------------------------------------------
def TEST_ORI_Formula_Derivation(Model,Q_Column_Name,S_Column_Name, Image_Flag,input_csv_path,output_dir):
    """
    使用指定模型对评估数据集进行测试，并保存测试结果为 CSV
    Parameters
    ----------
    Model : callable
        已加载的模型对象（支持文本或图文输入）
    Column_Name : str
        CSV 中用于测试的题目列名
    Image : bool
        是否启用图像判断逻辑
    """
    # =========================
    # 1. 路径配置（可按需修改）
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"result_{Model}_nosystem_formula_derivation.csv"
    )
    os.makedirs(output_dir, exist_ok=True)
    # =========================
    # 2. 读取数据集
    # =========================
    df = pd.read_csv(input_csv_path)

    if Q_Column_Name not in df.columns:
        raise ValueError(f"Column '{Q_Column_Name}' 不存在于 CSV 文件中")
    # =========================
    # 3. 初始化结果存储
    # =========================
    results = []
    # =========================
    # 4. 逐条测试
    # =========================
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        question = row[Q_Column_Name].strip()
        ori_solution = row[S_Column_Name].strip()
        image_lable = row['Image Lable'].strip()
        difficulty = row['Difficulty']
        # ---------- 图像判断 ----------
        if Image_Flag:
            pass
        else:
            if row['Image Lable'] == 'Yes':
                response=""
            else:
                print(question)
                try:
                    response = Qwen2_5_Math_72b_Formula_Derivation(question=question,system="You are an expert in deriving astronomical formulas.")
                except:
                    response = "Erro"
        # ---------- 记录结果 ----------
        results.append({
            "Index": idx+1,
            "Question": question,
            "Solution": ori_solution,
            "Image Lable": image_lable,
            "Model_Response": response,
            "Difficulty": difficulty,
        })
    # =========================
    # 5. 保存为 CSV
    # =========================
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"✅ 测试完成，结果已保存至: {output_csv_path}")

def EVAL_ORI_Formula_Derivation(Model,Image_Flag,input_csv_path,output_dir):
    # =========================
    # 1. 路径配置（可按需修改）
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"eval_{Model}_ori_formula_derivation.csv"
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
        model_solution = row['Model_Response'].strip()
        image_lable = row['Image Lable'].strip()
        difficulty = row['Difficulty']
        # ---------- 图像判断 ----------
        if Image_Flag:
            pass
        else:
            if row['Image Lable'] == 'Yes':
                response=""
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
    # =========================
    # 4. 保存为 CSV
    # =========================
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"✅ 测试完成，结果已保存至: {output_csv_path}")

def TEST_ORI_Computational_Reasoning(Model,Q_Column_Name,S_Column_Name,F_Column_Name, Image_Flag,input_csv_path,output_dir):
    """
    使用指定模型对评估数据集进行测试，并保存测试结果为 CSV
    Parameters
    ----------
    Model : callable
        已加载的模型对象（支持文本或图文输入）
    Column_Name : str
        CSV 中用于测试的题目列名
    Image : bool
        是否启用图像判断逻辑
    """
    # =========================
    # 1. 路径配置（可按需修改）
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"result_{Model}_think_computational_reasoning.csv"
    )
    os.makedirs(output_dir, exist_ok=True)
    # =========================
    # 2. 读取数据集
    # =========================
    df = pd.read_csv(input_csv_path)

    if Q_Column_Name not in df.columns:
        raise ValueError(f"Column '{Q_Column_Name}' 不存在于 CSV 文件中")
    # =========================
    # 3. 初始化结果存储
    # =========================
    results = []
    # =========================
    # 4. 逐条测试
    # =========================
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        question = row[Q_Column_Name].strip()
        ori_solution = row[S_Column_Name].strip()
        ori_final_answer = row[F_Column_Name].strip()
        difficulty = row['Difficulty']
        image_lable = row['Image Lable'].strip()
        # ---------- 图像判断 ----------
        if Image_Flag:
            pass
        else:
            if row['Image Lable'] == 'Yes':
                response=""
            else:
                print(question)
                try:
                    response = AstroOne_Computational_Reasoning(question=question,system="You are an expert in astronomical computational reasoning.",model="oneastronomy-r1")
                except:
                    response = "Erro"
        # ---------- 记录结果 ----------
        results.append({
            "Index": idx+1,
            "Question": question,
            "Solution": ori_solution,
            "Ori Final Answer":ori_final_answer,
            "Image Lable": image_lable,
            "Model_Response": response,
            "Difficulty":difficulty,
        })
    # =========================
    # 5. 保存为 CSV
    # =========================
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"✅ 测试完成，结果已保存至: {output_csv_path}")

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

def TEST_ORI_Formula_Calculationg(Model,Q_Column_Name,S_Column_Name,F_Column_Name, input_csv_path,output_dir):
    """
    使用指定模型对评估数据集进行测试，并保存测试结果为 CSV
    Parameters
    ----------
    Model : callable
        已加载的模型对象（支持文本或图文输入）
    Column_Name : str
        CSV 中用于测试的题目列名
    Image : bool
        是否启用图像判断逻辑
    """
    # =========================
    # 1. 路径配置（可按需修改）
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"result_{Model}_nosystem_formula_calculationg.csv"
    )
    os.makedirs(output_dir, exist_ok=True)
    # =========================
    # 2. 读取数据集
    # =========================
    df = pd.read_csv(input_csv_path)

    if Q_Column_Name not in df.columns:
        raise ValueError(f"Column '{Q_Column_Name}' 不存在于 CSV 文件中")
    # =========================
    # 3. 初始化结果存储
    # =========================
    results = []
    # =========================
    # 4. 逐条测试
    # =========================
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        question = row[Q_Column_Name].strip()
        ori_solution = row[S_Column_Name].strip()
        ori_final_answer = row[F_Column_Name].strip()
        difficulty = row['Difficulty']
        # ---------- 图像判断 ----------

        print(question)
        try:
            # response = DeepSeek_V3_2_Formula_Calculationg(question=question,system="You are an expert in astronomical formula calculation.",model="deepseek-chat")
            response = Qwen2_5_Math_72b_Formula_Calculationg(question=question,system="You are an expert in astronomical formula calculation.")
        except:
            response = "Erro"
        # ---------- 记录结果 ----------
        results.append({
            "Index": idx+1,
            "Question": question,
            "Solution": ori_solution,
            "Ori Final Answer":ori_final_answer,
            "Model_Response": response,
            "Difficulty":difficulty,
        })
    # =========================
    # 5. 保存为 CSV
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

def TEST_CODE_Computational_Reasoning(Model,Q_Column_Name,F_Column_Name, input_csv_path,output_dir):
    """
    使用指定模型对评估数据集进行测试，并保存测试结果为 CSV
    Parameters
    ----------
    Model : callable
        已加载的模型对象（支持文本或图文输入）
    Column_Name : str
        CSV 中用于测试的题目列名
    Image : bool
        是否启用图像判断逻辑
    """
    # =========================
    # 1. 路径配置（可按需修改）
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"result_{Model}_code_computational_reasoning.csv"
    )
    os.makedirs(output_dir, exist_ok=True)
    # =========================
    # 2. 读取数据集
    # =========================
    df = pd.read_csv(input_csv_path)

    if Q_Column_Name not in df.columns:
        raise ValueError(f"Column '{Q_Column_Name}' 不存在于 CSV 文件中")
    # =========================
    # 3. 初始化结果存储
    # =========================
    results = []
    # =========================
    # 4. 逐条测试
    # =========================
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        question = row[Q_Column_Name].strip()
        ori_final_answer = row[F_Column_Name].strip()
        difficulty = row['Difficulty']
        # ---------- 图像判断 ----------

        print(question)
        try:
            response = Qwen2_5_Math_72b_Code(question=question,system="You are an expert in astronomical computational reasoning.")
            # response = Qwen2_5_Math_72b_Code(question=question,system="You are an expert in astronomical formula calculation.")
        except:
            response = "Erro"
        # ---------- 记录结果 ----------
        results.append({
            "Index": idx+1,
            "Question": question,
            "Ori Final Answer":ori_final_answer,
            "Model_Response": response,
            "Difficulty":difficulty,
        })
    # =========================
    # 5. 保存为 CSV
    # =========================
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"✅ 测试完成，结果已保存至: {output_csv_path}")


if __name__ == '__main__':

    TEST_ORI_Computational_Reasoning(Model="AstroOne_Think", Q_Column_Name="Test Ori Question",S_Column_Name="Test Ori Solution", F_Column_Name="Test Ori Final Answer",Image_Flag=False,
                                    input_csv_path=r".\main data\ORI-Computational Reasoning.csv",
                                    output_dir=r".\main test results")