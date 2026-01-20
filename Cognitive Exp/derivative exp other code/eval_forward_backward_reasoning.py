
import json
import os
import pandas as pd
from openai import OpenAI
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback
import re
import subprocess
import sys
import tempfile
from typing import List, Dict, Optional


def Result_Evaluation_GPT5_1(question, Reference_Answer, Candidate_Answer):
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
    It misses key information
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
    client = OpenAI(
        api_key="your_key",
        base_url="https://api.deepseek.com/v1"
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        temperature=1,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
        stream=False
    )
    return response.choices[0].message.content


def extract_python_code(text: str) -> Optional[str]:
    """
    1) Extract ```python ... ``` code block
    2) Truncate until the last "return ..." statement
       (termination condition: newline or two consecutive spaces)
    """
    block_pat = r"```python\s*(.*?)\s*```"
    m = re.search(block_pat, text, re.DOTALL | re.IGNORECASE)
    if not m:
        return None

    code = m.group(1)

    # Find the last return line and stop after newline or two spaces
    return_pat = re.compile(r"(?m)^[ \t]*return\b.*?(?=(?:\n| {2}))")

    last = None
    for it in return_pat.finditer(code):
        last = it

    if not last:
        return code.strip()

    end = last.end()
    return code[:end].rstrip()


def EVAL_ORI_Formula_Calculationg(Model, input_csv_path, output_dir, type_index):
    output_csv_path = os.path.join(
        output_dir, f"eval_{Model}_Code_{type_index}.csv"
    )
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(input_csv_path)

    error_rows: List[Dict[str, str]] = []

    base_dir = os.path.dirname(os.path.abspath(__file__))
    code_template_path = os.path.join(base_dir, 'Code_temp_file.py')

    # =========================
    # Read-only template (never write back)
    # =========================
    with open(code_template_path, 'r', encoding='utf-8') as f:
        template_origin = f.read()

    if '# <<<FUNCTION_CODE>>>' not in template_origin:
        raise RuntimeError(
            "Template Code_temp_file.py is corrupted: missing # <<<FUNCTION_CODE>>>"
        )

    results = []

    for idx, row in tqdm(df.iterrows(), total=len(df)):
        question = str(row.get('Question', '')).strip()
        ori_result = str(row.get('Ori Final Answer', '')).strip()
        model_solution_json = str(row.get('Model_Response', ''))
        difficulty = row.get('Difficulty', '')

        code_str = extract_python_code(model_solution_json)

        if code_str is None:
            error_rows.append({
                'csv_file': os.path.basename(input_csv_path),
                'row': str(idx + 1),
                'Model_Response': model_solution_json,
                'error_type': 'Function detection error',
                'stdout': '',
                'stderr': ''
            })
            Eval_result = 'Erro'
        else:
            try:
                # =========================
                # Fill template in memory only
                # =========================
                filled = template_origin.replace(
                    '# <<<FUNCTION_CODE>>>',
                    code_str
                )

                main_replace = """

# =========================
# Execution Area
# =========================
if __name__ == '__main__':
    res = execute_code()
    print(res)
"""

                sep = '# =========================\n# Execution Area'
                if sep in filled:
                    prefix = filled.split(sep)[0]
                    test_content = prefix + main_replace
                else:
                    test_content = filled + main_replace

                # =========================
                # Option A: create an independent temp script per row
                # =========================
                with tempfile.NamedTemporaryFile(
                    mode="w",
                    suffix=".py",
                    prefix="test_",
                    delete=False,
                    encoding="utf-8",
                    dir=base_dir
                ) as tf:
                    temp_test_py_path = tf.name
                    tf.write(test_content)

                try:
                    run = subprocess.run(
                        [sys.executable, temp_test_py_path],
                        capture_output=True,
                        text=True,
                        cwd=base_dir
                    )
                finally:
                    try:
                        os.remove(temp_test_py_path)
                    except OSError:
                        pass

                if run.returncode != 0:
                    error_rows.append({
                        'csv_file': os.path.basename(input_csv_path),
                        'row': str(idx + 1),
                        'Model_Response': model_solution_json,
                        'error_type': 'test.py runtime error',
                        'stdout': (run.stdout or '')[:2000],
                        'stderr': (run.stderr or '')[:2000],
                    })
                    Eval_result = 'Erro'
                else:
                    stdout = (run.stdout or '').strip()
                    model_result = stdout.splitlines()[-1] if stdout else ''

                    print(model_result)

                    Eval_result = Result_Evaluation_GPT5_1(
                        question=question,
                        Reference_Answer=ori_result,
                        Candidate_Answer=model_result
                    )

            except Exception as e:
                error_rows.append({
                    'csv_file': os.path.basename(input_csv_path),
                    'row': str(idx + 1),
                    'Model_Response': model_solution_json,
                    'error_type': 'test.py runtime exception',
                    'stdout': '',
                    'stderr': ''.join(traceback.format_exception(type(e), e, e.__traceback__))[:2000]
                })
                Eval_result = 'Erro'

            print(Eval_result)

        results.append({
            "Index": idx + 1,
            "Question": question,
            "Eval_result": Eval_result,
            "Difficulty": difficulty,
        })

    result_df = pd.DataFrame(results)
    result_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"Evaluation completed. Results saved to: {output_csv_path}")

    if error_rows:
        error_csv_path = os.path.join(output_dir, 'error.csv')
        error_df = pd.DataFrame(
            error_rows,
            columns=['csv_file', 'row', 'Model_Response', 'error_type', 'stdout', 'stderr']
        )
        if os.path.exists(error_csv_path):
            error_df.to_csv(
                error_csv_path, mode='a',
                header=False, index=False,
                encoding='utf-8-sig'
            )
        else:
            error_df.to_csv(
                error_csv_path,
                index=False,
                encoding='utf-8-sig'
            )


def run_one(d):
    EVAL_ORI_Formula_Calculationg(
        Model=d["Model"],
        input_csv_path=d["path"],
        output_dir=r"your_path",
        type_index=d["index"]
    )
    return (d["Model"], d["index"], d["path"])


if __name__ == "__main__":
    max_concurrent = 1
    main_dir = r"your_path"
    data = [
        {
            "Model": "llama_3_1_8b",
            "path": os.path.join(main_dir, "formula_calculation.csv"),
            "index": "formula_calculation"
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
