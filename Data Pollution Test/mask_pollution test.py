import csv
import os
import time
import pandas as pd
import json
from openai import OpenAI

# 初始化 NVIDIA DeepSeek 客户端
client = OpenAI(api_key="xxx-xxx", base_url="https://api.deepseek.com/v1")

def call_deepseek_v3_2(prompt):
    for i in range(15):  # 最多重试10次
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": {prompt}},
                ]
            )

            # 获取模型回复内容
            response_content = response.choices[0].message.content

            return response_content

        except Exception as e:
            print(f"调用失败: {e}")
            wait_time = 15 * (2 ** i)  # 指数退避
            print(f"等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)

    return None

def get_model_prediction(masked_question: str) -> list:
    """根据 masked_question 获取模型预测的变量列表"""
    prompt = f"""
You are a variable completion assistant. The input will include a question text containing numbered `<Replace i>` placeholders (e.g., `<Replace 1>`, `<Replace 2>`, …).

For each `<Replace i>` placeholder, determine the corresponding original content, including:
* Variable name (`name`)
* Variable value (`value`)

Do not include any explanatory text; only return the completion results.

**Input:** {masked_question}

**Output:**
[
{{
"order": "the corresponding placeholder",
"name": "variable name",
"value": "the corresponding value of the variable"
}},
...
]
    """
    answer = call_deepseek_v3_2(prompt)  # 调用你的模型
    try:
        return json.loads(answer)
    except json.JSONDecodeError:
        print("模型返回 JSON 解析失败")
        return []

def batch_evaluate_write_detail(csv_files: list, json_col: str, detail_file: str, summary_file: str):
    """批量处理 CSV 文件，每处理完一道题就写入 detail 文件"""
    summary_results = []

    # 初始化 detail 文件，如果文件不存在则创建并写入表头
    if not os.path.exists(detail_file):
        with open(detail_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                "filename", "masked_question", "variables", "predicted_values",
                "exact_match", "partial_match"
            ])
        print(f"创建新的 detail 文件: {detail_file}")

    # 打开 detail 文件用于追加（保持打开状态以减少频繁开关文件）
    detail_f = open(detail_file, 'a', newline='', encoding='utf-8-sig')
    detail_writer = csv.writer(detail_f)

    for csv_file in csv_files:
        print(f"正在处理文件: {csv_file}")
        df = pd.read_csv(csv_file, encoding='utf-8')
        exact_match_count = 0
        partial_match_count = 0
        total_questions = len(df)
        processed_count = 0

        for idx, row in df.iterrows():
            processed_count += 1
            print(f"处理进度: {csv_file} - 第 {processed_count}/{total_questions} 题")

            try:
                data = json.loads(row[json_col])
            except json.JSONDecodeError:
                print(f"{csv_file} Row {idx} JSON decode error")
                total_questions -= 1
                # 写入错误记录
                detail_writer.writerow([
                    os.path.basename(csv_file),
                    "JSON解析错误",
                    "",
                    "",
                    0,
                    0
                ])
                detail_f.flush()
                continue

            masked_question = data.get("masked_question", "")
            variables = data.get("variables", [])

            # 调用模型获取预测
            print(f"调用模型预测: {masked_question[:50]}...")
            predicted_values = get_model_prediction(masked_question)

            all_exact = True
            has_partial = False

            for std_var in variables:
                order = std_var.get("order", "")
                std_name = std_var.get("name", "").strip()
                std_value = std_var.get("value", "").strip()

                pred_var = next((v for v in predicted_values if v.get("order") == order), {})
                pred_name = pred_var.get("name", "").strip()
                pred_value = pred_var.get("value", "").strip()

                # 精确匹配要求 name 和 value 都一致
                if pred_name != std_name or pred_value != std_value:
                    all_exact = False

                # 部分匹配：name 或 value 任意一个一致
                if pred_name == std_name or pred_value == std_value:
                    has_partial = True

            if all_exact:
                exact_match_count += 1
            if has_partial:
                partial_match_count += 1

            # **立即写入 detail 文件**
            detail_writer.writerow([
                os.path.basename(csv_file),
                masked_question,
                json.dumps(variables, ensure_ascii=False),
                json.dumps(predicted_values, ensure_ascii=False),
                1 if all_exact else 0,
                1 if has_partial else 0
            ])
            detail_f.flush()
            print(f"已记录第 {processed_count} 题结果")

        # 汇总每个文件的匹配率
        overall_exact_match_rate = exact_match_count / total_questions if total_questions else 0
        overall_partial_match_rate = partial_match_count / total_questions if total_questions else 0

        summary_results.append({
            "filename": os.path.basename(csv_file),
            "overall_exact_match_rate": overall_exact_match_rate,
            "overall_partial_match_rate": overall_partial_match_rate
        })

        print(f"文件 {csv_file} 处理完成: ")
        print(f"  精确匹配率: {overall_exact_match_rate:.2%}")
        print(f"  部分匹配率: {overall_partial_match_rate:.2%}")

    # 关闭 detail 文件
    detail_f.close()

    # 保存 summary 文件
    summary_df = pd.DataFrame(summary_results)
    summary_df.to_csv(summary_file, index=False, encoding='utf-8-sig')
    print(f"Detail 记录已保存到: {detail_file}")
    print(f"Summary 已保存到: {summary_file}")


if __name__ == "__main__":
    csv_files = [
        "./APBench Calculation-masked-derive-done.csv",
        "./Computational-Reasoning-coded-masked-derive-done.csv",
        "./Computational-Reasoning-uncoded-masked-done.csv",
        "./Formula Calculation-derive-done.csv",
        "./Formula Derivation-masked-done.csv",
        "./TPBench Calculation-masked-done.csv",
    ]
    json_col = "Pollution Test Json"
    detail_file = r"deepseek_v3.2-Eval-Resul-records.csv"
    summary_file = r"deepseek_v3.2-Eval-Score-test.csv"

    batch_evaluate_write_detail(csv_files, json_col, detail_file, summary_file)