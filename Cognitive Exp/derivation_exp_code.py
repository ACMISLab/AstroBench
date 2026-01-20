import os

import pandas as pd
from openai import OpenAI
from tqdm import tqdm
QwenMax_Key="xxx-xxx"
Closeai_key="xxx-xxx"
Closeai_url="https://api.openai-proxy.org/v1"

def call_deepseek_v3_2(question,system):
    client = OpenAI(
        api_key="xxx-xxx",
        base_url="https://api.deepseek.com/v1")

    response = client.chat.completions.create(
        model="deepseek-chat",
        temperature=0, #代码生成/数学解题
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
        stream=False
    )

    return response.choices[0].message.content

def call_AstroOne(question,system):
    client = OpenAI(
        api_key="xxx-xxx",
        base_url="https://oneastronomy.zero2x.org/api/platform/v1",
        max_retries=0
    )

    chat_completion = client.chat.completions.create(
        model="oneastronomy-chat",
        messages=[
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': question}
        ],
        stream=False,
    )
    return chat_completion.choices[0].message.content

def call_qwen3_max_syetem(question,system):
    client = OpenAI(
        # openai系列的sdk，包括langchain，都需要这个/v1的后缀
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=QwenMax_Key,
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question}
        ],
        # extra_body={"enable_thinking":True}, #启用深度思考
        model="qwen3-max-2025-09-23", # 如果是其他兼容模型，比如deepseek，直接这里改模型名即可，其他都不用动
    )
    return chat_completion.choices[0].message.content

def call_closeai_gemini2_5_flash_syetem(question,system):
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
        model="gemini-2.5-flash", # 如果是其他兼容模型，比如deepseek，直接这里改模型名即可，其他都不用动
        # extra_body={
        #     'extra_body':{
        #         "google":{
        #             "thinking_config": {
        #                 "thinking_budget": 24576}}}}
        )
    return chat_completion.choices[0].message.content
    # return chat_completion

def call_closeai_claude_haiku_4_5_syetem(question,system):
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
        model="claude-haiku-4-5", # 如果是其他兼容模型，比如deepseek，直接这里改模型名即可，其他都不用动
        # extra_body={"thinking":{ "type": "enabled","budget_tokens":0}}
    )
    return chat_completion.choices[0].message.content
    # return chat_completion


def TEST_Shuffle_Formula_Calculation(Task=r"shuffle_formula_calculation",
                                     Model=r"DeepSeekV3_2",
                                     input_csv_path=r".\derivation_data\Shuffle-Redundant-Reasoning-Formula Calculation.csv",
                                     output_dir=r".\derivation_test_results",
                                     api_function=r"call_deepseek_v3_2"):
    # =========================
    # 1. 路径配置（可按需修改）
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"all_result_{Model}_{Task.lower()}.csv"
    )
    os.makedirs(output_dir, exist_ok=True)

    sub_file_paths=[]

    # =========================
    # 2. 读取数据集
    # =========================
    df = pd.read_csv(input_csv_path)

    # =========================
    # 3. 逐阶段测试
    # =========================
    for sub_task in ["Test Redudant Background Question","Test Redudant Conditions Question","Test Shuffle Question Sentence", \
                     "Test Shuffle Question Word","Test Forward Step","Test Mid Step","Test Backward Step"]:
    # for sub_task in ["Test Shuffle Question Word"]:

        print(f"===========模型：{Model} 开始执行:{sub_task}测试==============")
        # =========================
        # 3.1 初始化结果存储
        # =========================
        results = []

        sub_output_csv_path = os.path.join(output_dir, f"result_{Model}_{Task.lower()}_{sub_task}.csv")

        # =========================
        # 3.2 逐条测试
        # =========================
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            #固定不变
            Difficulty = row["Difficulty"]
            Test_Ori_Solution = row["Test Ori Solution"].strip()
            Test_Ori_Answer = row["Test Ori Final Answer"].strip()
            Test_Question = ""
            if sub_task in ["Test Forward Step", "Test Mid Step", "Test Backward Step"]:
                # 根据任务变动
                Steps_Num = row["Steps Num"]
                if Steps_Num <=1:
                    Response = "None"
                    Test_Question = row["Test Ori Question"].strip() #思维断裂任务使用原始问题
                    results.append({
                        "Difficulty": Difficulty,
                        "Test Ori Question": Test_Question,
                        "Test Ori Solution": Test_Ori_Solution,
                        "Test Ori Final Answer": Test_Ori_Answer,
                        f"{sub_task.replace('Step', 'Mask')}": row[sub_task.replace("Step", "Mask")],
                        f"{sub_task}_Model_Response": Response,
                    })
                    continue
                elif Steps_Num <=2 and sub_task == "Test Mid Step":
                    Response = "None"
                    Test_Question = row["Test Ori Question"].strip() #思维断裂任务使用原始问题
                    results.append({
                        "Difficulty": Difficulty,
                        "Test Ori Question": Test_Question,
                        "Test Ori Solution": Test_Ori_Solution,
                        "Test Ori Final Answer": Test_Ori_Answer,
                        f"{sub_task.replace('Step', 'Mask')}": row[sub_task.replace("Step", "Mask")],
                        f"{sub_task}_Model_Response": Response,
                    })
                    continue
                else:
                    Test_Question = row["Test Ori Question"].strip() #思维断裂任务使用原始问题
                    Mask_Solution = row[sub_task]
                    question_prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given problem and its solution, in which some key steps are missing. The missing parts are marked with '<Replace>'. You need to fill in these placeholders based on the context to complete the solution.

# Output Format
{{
  "filled replace": "List the content filled into Replace placeholder.",
  "complete solution": "Fill the full solution with replace content integrated"
  "final answer": "Only fill in the final result to the question here, no additional steps are needed."
}}

Now, here is your question: "{Test_Question}".
The solution that needs you to improve is: """{Mask_Solution}"""'''
            elif sub_task in ["Test Redudant Background Question","Test Redudant Conditions Question","Test Shuffle Question Sentence","Test Shuffle Question Word"]:
                Test_Question = row[sub_task].strip() #使用衍生问题
                question_prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. 
In principle, you need to solve this problem and provide the problem-solving process and the final result. But, if you think the problem is not unsolvable, just return `Unsolvable`.

# Output Format
{{
  "solution": "Fill in the problem-solving process here",
  "final answer": "Only fill in the final result to the question here, no additional steps are needed."
}}

Now, here is your question: "{Test_Question}"'''
            else:
                print("===========字段错误==============")
            try:
                print(question_prompt)
                Response = globals()[api_function](question=question_prompt,system="You are an expert in astronomical formula calculation.")
                print(Response)
            except:
                Response = "Erro"

            if sub_task in ["Test Forward Step" , "Test Mid Step" , "Test Backward Step"]:
                # ---------- 记录结果 ----------
                results.append({
                    "Difficulty": Difficulty,
                    "Test Ori Question": Test_Question,
                    "Test Ori Solution": Test_Ori_Solution,
                    "Test Ori Final Answer": Test_Ori_Answer,
                    f"{sub_task.replace('Step', 'Mask')}": row[sub_task.replace("Step", "Mask")],
                    f"{sub_task}_Model_Response": Response,
                })
            elif sub_task in ["Test Redudant Background Question" , "Test Redudant Conditions Question" , "Test Shuffle Question Sentence"]:
                results.append({
                    "Difficulty": Difficulty,
                    f"{sub_task}": Test_Question,
                    "Test Ori Solution": Test_Ori_Solution,
                    "Test Ori Final Answer": Test_Ori_Answer,
                    f"{sub_task}_Model_Response": Response,
                })
            elif sub_task == "Test Shuffle Question Word":
                results.append({
                    "Difficulty": Difficulty,
                    f"{sub_task}": Test_Question,
                    "Test Ori Answer": "Unsolvable",
                    f"{sub_task}_Model_Response": Response,
                })
            else:
                print("===========预期结果保存错误==============")

        # =========================
        # 3.3. 子任务保存为CSV,防止中途错误
        # =========================
        result_df = pd.DataFrame(results)
        result_df.to_csv(sub_output_csv_path, index=True, encoding="utf-8-sig")

        sub_file_paths.append(sub_output_csv_path)
        print(f"✅ 测试完成，结果已保存至: {sub_output_csv_path}")
        print(f"===========✅模型：{Model} 执行:{sub_task}完成==============")


    # =========================
    # 4. 合并总的结果
    # =========================
    # 使用列表推导式读取所有CSV文件
    dfs = [pd.read_csv(file) for file in sub_file_paths]
    # 使用concat合并，axis=1表示按列合并，忽略索引
    merged_df = pd.concat(dfs, axis=1, ignore_index=False)
    # 删除重复的列（保留第一次出现的列）
    merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]
    # 保存到新文件
    merged_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

def TEST_Shuffle_Computational_Reasoning(Task=r"shuffle_computational_reasoning",
                                     Model=r"DeepSeekV3_2",
                                     input_csv_path=r".\derivation_data\Shuffle-Redundant-Reasoning-Computational-Reasoning.csv",
                                     output_dir=r".\derivation_test_results",
                                     api_function=r"call_deepseek_v3_2"):
    # =========================
    # 1. 路径配置（可按需修改）
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"all_result_{Model}_{Task.lower()}.csv"
    )
    os.makedirs(output_dir, exist_ok=True)

    sub_file_paths=[]

    # =========================
    # 2. 读取数据集
    # =========================
    df = pd.read_csv(input_csv_path)

    # =========================
    # 3. 逐阶段测试
    # =========================
    for sub_task in ["Test Redudant Background Question","Test Redudant Conditions Question","Test Shuffle Question Sentence", \
                     "Test Shuffle Question Word","Test Forward Step","Test Mid Step","Test Backward Step"]:

        print(f"===========模型：{Model} 开始执行:{sub_task}测试==============")
        # =========================
        # 3.1 初始化结果存储
        # =========================
        results = []

        sub_output_csv_path = os.path.join(output_dir, f"result_{Model}_{Task.lower()}_{sub_task}.csv")

        # =========================
        # 3.2 逐条测试
        # =========================
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            #固定不变
            Difficulty = row["Difficulty"]
            Test_Ori_Solution = row["Test Ori Solution"].strip()
            Test_Ori_Answer = row["Test Ori Final Answer"].strip()
            Test_Question = ""

            if sub_task in [ "Test Forward Step" , "Test Mid Step" , "Test Backward Step"]:
                # 根据任务变动
                Steps_Num = row["Steps Num"]
                if Steps_Num <=1:
                    Response = "None"
                    Test_Question = row["Test Ori Question"].strip() #思维断裂任务使用原始问题
                    results.append({
                        "Difficulty": Difficulty,
                        "Test Ori Question": Test_Question,
                        "Test Ori Solution": Test_Ori_Solution,
                        "Test Ori Final Answer": Test_Ori_Answer,
                        f"{sub_task.replace('Step', 'Mask')}": row[sub_task.replace("Step", "Mask")],
                        f"{sub_task}_Model_Response": Response,
                    })
                    continue
                elif Steps_Num <=2 and sub_task == "Test Mid Step":
                    Response = "None"
                    Test_Question = row["Test Ori Question"].strip() #思维断裂任务使用原始问题
                    results.append({
                        "Difficulty": Difficulty,
                        "Test Ori Question": Test_Question,
                        "Test Ori Solution": Test_Ori_Solution,
                        "Test Ori Final Answer": Test_Ori_Answer,
                        f"{sub_task.replace('Step', 'Mask')}": row[sub_task.replace("Step", "Mask")],
                        f"{sub_task}_Model_Response": Response,
                    })
                    continue
                else:
                    Test_Question = row["Test Ori Question"].strip() #思维断裂任务使用原始问题
                    Mask_Solution = row[sub_task]
                    question_prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given problem and its solution, in which some key steps are missing. The missing parts are marked with '<Replace>'. You need to fill in these placeholders based on the context to complete the solution.

# Output Format
{{
  "filled replace": "List the content filled into Replace placeholder.",
  "complete solution": "Fill the full solution with replace content integrated"
  "final answer": "Only fill in the final result to the question here, no additional steps are needed."
}}

Now, here is your question: "{Test_Question}".
The solution that needs you to improve is: """{Mask_Solution}"""'''
            elif sub_task in ["Test Redudant Background Question" , "Test Redudant Conditions Question" , "Test Shuffle Question Sentence" , "Test Shuffle Question Word"]:
                Test_Question = row[sub_task].strip() #使用衍生问题
                question_prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. 
In principle, you need to solve this problem and provide the problem-solving process and the final result. But, if you think the problem is not unsolvable, just return `Unsolvable`.

# Output Format
{{
  "solution": "Fill in the problem-solving process here",
  "final answer": "Only fill in the final result to the question here, no additional steps are needed."
}}

Now, here is your question: "{Test_Question}"'''
            else:
                print("===========字段错误==============")

            try:
                Response = globals()[api_function](question=question_prompt,system="You are an expert in astronomical computational reasoning.")
            except:
                Response = "Erro"

            if sub_task in ["Test Forward Step" , "Test Mid Step" , "Test Backward Step"]:
                # ---------- 记录结果 ----------
                results.append({
                    "Difficulty": Difficulty,
                    "Test Ori Question": Test_Question,
                    "Test Ori Solution": Test_Ori_Solution,
                    "Test Ori Final Answer": Test_Ori_Answer,
                    f"{sub_task.replace('Step', 'Mask')}": row[sub_task.replace("Step", "Mask")],
                    f"{sub_task}_Model_Response": Response,
                })
            elif sub_task in ["Test Redudant Background Question" , "Test Redudant Conditions Question" , "Test Shuffle Question Sentence"]:
                results.append({
                    "Difficulty": Difficulty,
                    f"{sub_task}": Test_Question,
                    "Test Ori Solution": Test_Ori_Solution,
                    "Test Ori Final Answer": Test_Ori_Answer,
                    f"{sub_task}_Model_Response": Response,
                })
            elif sub_task == "Test Shuffle Question Word":
                results.append({
                    "Difficulty": Difficulty,
                    f"{sub_task}": Test_Question,
                    "Test Ori Answer": "Unsolvable",
                    f"{sub_task}_Model_Response": Response,
                })
            else:
                print("===========预期结果保存错误==============")

        # =========================
        # 3.3. 子任务保存为CSV,防止中途错误
        # =========================
        result_df = pd.DataFrame(results)
        result_df.to_csv(sub_output_csv_path, index=True, encoding="utf-8-sig")

        sub_file_paths.append(sub_output_csv_path)
        print(f"✅ 测试完成，结果已保存至: {sub_output_csv_path}")
        print(f"===========✅模型：{Model} 执行:{sub_task}完成==============")


    # =========================
    # 4. 合并总的结果
    # =========================
    # 使用列表推导式读取所有CSV文件
    dfs = [pd.read_csv(file) for file in sub_file_paths]
    # 使用concat合并，axis=1表示按列合并，忽略索引
    merged_df = pd.concat(dfs, axis=1, ignore_index=False)
    # 删除重复的列（保留第一次出现的列）
    merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]
    # 保存到新文件
    merged_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

def TEST_Shuffle_Formula_Derivation(Task=r"shuffle_formula_derivation",
                                     Model=r"DeepSeekV3_2",
                                     input_csv_path=r".\derivation_data\Shuffle-Redundant-Reasoning-Formula Derivation.csv",
                                     output_dir=r".\derivation_test_results",
                                     api_function=r"call_deepseek_v3_2"):
    # =========================
    # 1. 路径配置（可按需修改）
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"all_result_{Model}_{Task.lower()}.csv"
    )
    os.makedirs(output_dir, exist_ok=True)

    sub_file_paths=[]

    # =========================
    # 2. 读取数据集
    # =========================
    df = pd.read_csv(input_csv_path)

    # =========================
    # 3. 逐阶段测试
    # =========================
    for sub_task in ["Test Redudant Background Question","Test Redudant Conditions Question","Test Shuffle Question Sentence", \
                     "Test Shuffle Question Word","Test Forward Step","Test Mid Step","Test Backward Step"]:

        print(f"===========模型：{Model} 开始执行:{sub_task}测试==============")
        # =========================
        # 3.1 初始化结果存储
        # =========================
        results = []

        sub_output_csv_path = os.path.join(output_dir, f"result_{Model}_{Task.lower()}_{sub_task}.csv")

        # =========================
        # 3.2 逐条测试
        # =========================
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            #固定不变
            Difficulty = row["Difficulty"]
            Test_Ori_Solution = row["Test Ori Solution"].strip()
            # Test_Ori_Answer = row["Test Ori Final Answer"].strip()
            Test_Question = ""

            if sub_task in ["Test Forward Step" , "Test Mid Step" , "Test Backward Step"]:
                # 根据任务变动
                Steps_Num = row["Steps Num"]
                if Steps_Num <=1:
                    Response = "None"
                    Test_Question = row["Test Ori Question"].strip() #思维断裂任务使用原始问题
                    results.append({
                        "Difficulty": Difficulty,
                        "Test Ori Question": Test_Question,
                        "Test Ori Solution": Test_Ori_Solution,
                        # "Test Ori Final Answer": Test_Ori_Answer,
                        f"{sub_task.replace('Step', 'Mask')}": row[sub_task.replace("Step", "Mask")],
                        f"{sub_task}_Model_Response": Response,
                    })
                    continue
                elif Steps_Num <=2 and sub_task == "Test Mid Step":
                    Response = "None"
                    Test_Question = row["Test Ori Question"].strip() #思维断裂任务使用原始问题
                    results.append({
                        "Difficulty": Difficulty,
                        "Test Ori Question": Test_Question,
                        "Test Ori Solution": Test_Ori_Solution,
                        # "Test Ori Final Answer": Test_Ori_Answer,
                        f"{sub_task.replace('Step', 'Mask')}": row[sub_task.replace("Step", "Mask")],
                        f"{sub_task}_Model_Response": Response,
                    })
                    continue
                else:
                    Test_Question = row["Test Ori Question"].strip() #思维断裂任务使用原始问题
                    Mask_Solution = row[sub_task]
                    question_prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given problem and its solution, in which some key steps are missing. The missing parts are marked with '<Replace>'. You need to fill in these placeholders based on the context to complete the solution.

# Output Format
{{
  "filled replace": "List the content filled into Replace placeholder.",
  "complete solution": "Fill the full solution with replace content integrated"
}}

Now, here is your question: "{Test_Question}".
The solution that needs you to improve is: """{Mask_Solution}"""'''
            elif sub_task in ["Test Redudant Background Question" , "Test Redudant Conditions Question" , "Test Shuffle Question Sentence" , "Test Shuffle Question Word"]:
                Test_Question = row[sub_task].strip() #使用衍生问题
                question_prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. In principle, you need to solve this problem and provide the problem-solving process. But, if you think the problem is not unsolvable, just return `Unsolvable`.


Now, here is your question: "{Test_Question}"'''
            else:
                print("===========字段错误==============")

            try:
                Response = globals()[api_function](question=question_prompt,system="You are an expert in deriving astronomical formulas.")
            except:
                Response = "Erro"

            if sub_task in ["Test Forward Step" , "Test Mid Step" , "Test Backward Step"]:
                # ---------- 记录结果 ----------
                results.append({
                    "Difficulty": Difficulty,
                    "Test Ori Question": Test_Question,
                    "Test Ori Solution": Test_Ori_Solution,
                    # "Test Ori Final Answer": Test_Ori_Answer,
                    f"{sub_task.replace('Step', 'Mask')}": row[sub_task.replace("Step", "Mask")],
                    f"{sub_task}_Model_Response": Response,
                })
            elif sub_task in ["Test Redudant Background Question" , "Test Redudant Conditions Question" , "Test Shuffle Question Sentence"]:
                results.append({
                    "Difficulty": Difficulty,
                    f"{sub_task}": Test_Question,
                    "Test Ori Solution": Test_Ori_Solution,
                    # "Test Ori Final Answer": Test_Ori_Answer,
                    f"{sub_task}_Model_Response": Response,
                })
            elif sub_task == "Test Shuffle Question Word":
                results.append({
                    "Difficulty": Difficulty,
                    f"{sub_task}": Test_Question,
                    "Test Ori Answer": "Unsolvable",
                    f"{sub_task}_Model_Response": Response,
                })
            else:
                print("===========预期结果保存错误==============")

        # =========================
        # 3.3. 子任务保存为CSV,防止中途错误
        # =========================
        result_df = pd.DataFrame(results)
        result_df.to_csv(sub_output_csv_path, index=True, encoding="utf-8-sig")

        sub_file_paths.append(sub_output_csv_path)
        print(f"✅ 测试完成，结果已保存至: {sub_output_csv_path}")
        print(f"===========✅模型：{Model} 执行:{sub_task}完成==============")


    # =========================
    # 4. 合并总的结果
    # =========================
    # 使用列表推导式读取所有CSV文件
    dfs = [pd.read_csv(file) for file in sub_file_paths]
    # 使用concat合并，axis=1表示按列合并，忽略索引
    merged_df = pd.concat(dfs, axis=1, ignore_index=False)
    # 删除重复的列（保留第一次出现的列）
    merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]
    # 保存到新文件
    merged_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

def TEST_Condition_Computational_Reasoning(Task=r"condition_computational_reasoning",
                                     Model=r"DeepSeekV3_2",
                                     input_csv_path=r".\derivation_data\Condition-Computational-Reasoning.csv",
                                     output_dir=r".\derivation_test_results",
                                     api_function=r"call_deepseek_v3_2"):
    # =========================
    # 1. 路径配置（可按需修改）
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"all_result_{Model}_{Task.lower()}.csv"
    )
    os.makedirs(output_dir, exist_ok=True)

    sub_file_paths=[]

    # =========================
    # 2. 读取数据集
    # =========================
    df = pd.read_csv(input_csv_path)

    # =========================
    # 3. 逐阶段测试
    # =========================
    for sub_task in ["Test Condition Miss Question","Test Condition Damage Question"]:

        print(f"===========模型：{Model} 开始执行:{sub_task}测试==============")
        # =========================
        # 3.1 初始化结果存储
        # =========================
        results = []

        sub_output_csv_path = os.path.join(output_dir, f"result_{Model}_{Task.lower()}_{sub_task}.csv")

        # =========================
        # 3.2 逐条测试
        # =========================
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            #固定不变
            Difficulty = row["Difficulty"]
            Test_Question = row[sub_task].strip().replace("<Replace>", "")

            question_prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. 
In principle, you need to solve this problem and provide the problem-solving process and the final result. But, if you think the problem is not unsolvable, just return `Unsolvable`.

# Output Format
{{
  "solution": "Fill in the problem-solving process here",
  "final answer": "Only fill in the final result to the question here, no additional steps are needed."
}}

Now, here is your question: "{Test_Question}"'''

            try:
                Response = globals()[api_function](question=question_prompt,system="You are an expert in astronomical computational reasoning.")
            except:
                Response = "Erro"

            results.append({
                    "Difficulty": Difficulty,
                    f"{sub_task}": Test_Question,
                    "Test Ori Answer": "Unsolvable",
                    f"{sub_task}_Model_Response": Response,
                })
        # =========================
        # 3.3. 子任务保存为CSV,防止中途错误
        # =========================
        result_df = pd.DataFrame(results)
        result_df.to_csv(sub_output_csv_path, index=True, encoding="utf-8-sig")
        sub_file_paths.append(sub_output_csv_path)
        print(f"✅ 测试完成，结果已保存至: {sub_output_csv_path}")
        print(f"===========✅模型：{Model} 执行:{sub_task}完成==============")

    # =========================
    # 4. 合并总的结果
    # =========================
    # 使用列表推导式读取所有CSV文件
    dfs = [pd.read_csv(file) for file in sub_file_paths]
    # 使用concat合并，axis=1表示按列合并，忽略索引
    merged_df = pd.concat(dfs, axis=1, ignore_index=False)
    # 删除重复的列（保留第一次出现的列）
    merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]
    # 保存到新文件
    merged_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")


def TEST_Condition_Formula_Calculation(Task=r"condition_formula_calculation",
                                     Model=r"DeepSeekV3_2",
                                     input_csv_path=r".\derivation_data\Condition-Formula Calculation.csv",
                                     output_dir=r".\derivation_test_results",
                                     api_function=r"call_deepseek_v3_2"):
    # =========================
    # 1. 路径配置（可按需修改）
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"all_result_{Model}_{Task.lower()}.csv"
    )
    os.makedirs(output_dir, exist_ok=True)

    sub_file_paths=[]

    # =========================
    # 2. 读取数据集
    # =========================
    df = pd.read_csv(input_csv_path)

    # =========================
    # 3. 逐阶段测试
    # =========================
    for sub_task in ["Test Condition Miss Question","Test Condition Damage Question"]:

        print(f"===========模型：{Model} 开始执行:{sub_task}测试==============")
        # =========================
        # 3.1 初始化结果存储
        # =========================
        results = []

        sub_output_csv_path = os.path.join(output_dir, f"result_{Model}_{Task.lower()}_{sub_task}.csv")

        # =========================
        # 3.2 逐条测试
        # =========================
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            #固定不变
            Difficulty = row["Difficulty"]
            Test_Question = row[sub_task].strip().replace("<Replace>", "")

            question_prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. 
In principle, you need to solve this problem and provide the problem-solving process and the final result. But, if you think the problem is not unsolvable, just return `Unsolvable`.

# Output Format
{{
  "solution": "Fill in the problem-solving process here",
  "final answer": "Only fill in the final result to the question here, no additional steps are needed."
}}

Now, here is your question: "{Test_Question}"'''

            try:
                Response = globals()[api_function](question=question_prompt,system="You are an expert in astronomical formula calculation.")
            except:
                Response = "Erro"

            results.append({
                    "Difficulty": Difficulty,
                    f"{sub_task}": Test_Question,
                    "Test Ori Answer": "Unsolvable",
                    f"{sub_task}_Model_Response": Response,
                })
        # =========================
        # 3.3. 子任务保存为CSV,防止中途错误
        # =========================
        result_df = pd.DataFrame(results)
        result_df.to_csv(sub_output_csv_path, index=True, encoding="utf-8-sig")
        sub_file_paths.append(sub_output_csv_path)
        print(f"✅ 测试完成，结果已保存至: {sub_output_csv_path}")
        print(f"===========✅模型：{Model} 执行:{sub_task}完成==============")

    # =========================
    # 4. 合并总的结果
    # =========================
    # 使用列表推导式读取所有CSV文件
    dfs = [pd.read_csv(file) for file in sub_file_paths]
    # 使用concat合并，axis=1表示按列合并，忽略索引
    merged_df = pd.concat(dfs, axis=1, ignore_index=False)
    # 删除重复的列（保留第一次出现的列）
    merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]
    # 保存到新文件
    merged_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

#No-Problem
def TEST_Knowledge_Redefinition_Formula_Calculation(Task=r"knowledge_redefinition_formula_calculation",
                                     Model=r"DeepSeekV3_2",
                                     input_csv_path=r".\derivation_data\Knowledge-Redefinition-Formula Calculation.csv",
                                     output_dir=r".\derivation_test_results",
                                     api_function=r"call_deepseek_v3_2"):
    # =========================
    # 1. 路径配置（可按需修改）
    # =========================
    output_csv_path = os.path.join(
        output_dir, f"all_result_{Model}_{Task.lower()}.csv"
    )
    os.makedirs(output_dir, exist_ok=True)

    # =========================
    # 2. 读取数据集
    # =========================
    df = pd.read_csv(input_csv_path)

    # =========================
    # 3. 逐阶段测试
    # =========================

    print(f"===========模型：{Model} 开始执行:{Task}测试==============")
    # =========================
    # 4 初始化结果存储
    # =========================
    results = []

    # =========================
    # 5 逐条测试
    # =========================
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        #固定不变
        Difficulty = row["Difficulty"]
        Test_Question = row["Knowledge Redefinition Generation Question"].strip()
        Test_Ori_Solution = row["Knowledge Redefinition Generation Solution"].strip()
        Test_Ori_Answer = row["Knowledge Redefinition Final Answer"].strip()

        question_prompt = f'''# Task Definition
Now you are a astronomy expert. Your task is to read the given question and then solve it. 
You need to solve this problem and provide the problem-solving process and the final result. 

# Output Format
{{
  "solution": "Fill in the problem-solving process here",
  "final answer": "Only fill in the final result to the question here, no additional steps are needed."
}}

Now, here is your question: "{Test_Question}"'''

        try:
            Response = globals()[api_function](question=question_prompt,system="You are an expert in astronomical formula calculation.")
        except:
            Response = "Erro"

        results.append({
                "Difficulty": Difficulty,
                "Knowledge Redefinition Generation Question": Test_Question,
                "Knowledge Redefinition Generation Solution": Test_Ori_Solution,
                "Knowledge Redefinition Final Answer": Test_Ori_Answer,
                f"{Task}_Model_Response": Response,
            })
    # =========================
    # 6 保存为CSV
    # =========================
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_csv_path, index=True, encoding="utf-8-sig")
    print(f"✅ 测试完成，结果已保存至: {output_csv_path}")
    print(f"===========✅模型：{Model} 执行:{Task}完成==============")

# TEST_Shuffle_Formula_Calculation()
# TEST_Shuffle_Formula_Derivation()
TEST_Shuffle_Computational_Reasoning(Model="Gemini2_5_Flash",api_function="call_closeai_gemini2_5_flash_syetem")