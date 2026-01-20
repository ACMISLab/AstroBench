import csv
import os
import random
import re
from redundant_infor import redundant_infor_list,redundant_conditions_list
import argparse
from pathlib import Path
import pandas as pd

def generate_code_question(input_csv = r"xxx",output_csv = "output.csv"):
    import csv

    # ===== 公共依赖 =====
    import random
    import math
    from datetime import datetime, timedelta
    from typing import Dict, List, Any, Tuple
    import numpy as np
    from scipy.integrate import quad

    # 放到一个 dict 中，供 exec 使用
    base_env = {
        "Dict": Dict,
        "List": List,
        "Any": Any,
        "random": random,
        "math": math,
        "datetime": datetime,
        "Tuple": Tuple,
        "np": np,
        "quad": quad,
        "timedelta": timedelta,
    }

    with open(input_csv, newline='', encoding="utf-8") as infile, \
            open(output_csv, "w", newline='', encoding="utf-8-sig") as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        writer.writerow(["test_generate_question","test_generate_solution","test_generate_finalanswer"])
        next(reader)  # 跳过表头

        for row_idx, row in enumerate(reader, start=1):
            gen_func_code = row[3]
            main_func_code = row[4] + "\n    return sample"

            # 每一行创建独立执行环境
            exec_env = base_env.copy()

            try:
                # 1执行生成函数
                exec(gen_func_code, exec_env)

                # 2执行 main 函数（内部调用生成函数）
                exec(main_func_code, exec_env)

                # 3调用 main()
                result = exec_env["main"]()

                question = result['question']
                solution = result['question']
                final_answer = result['question']
                # print(result)

            except Exception as e:
                question = f"ERROR row {row_idx}: {e}"

            writer.writerow([question,solution,final_answer])

def shuffle_question_sentence(question, answer, confusion_level, save_file_path):
    """
    question: str 原始问题
    answer: str 原始答案
    confusion_level: float (0~1) 打乱强度
    save_file_path: str csv文件路径
    """

    # 1. 句子切分（保留分隔符）,不切分小数
    pattern = r'([，。！？\?!；;]|(?<!\d)\.(?!\d)|(?<!\d),(?!\d))'
    parts = re.split(pattern, question)
    # parts = re.split(r'([，,。！？\?!；;])', question)
    # parts = re.split(r'([，,。！？\?!；;-])', question)
    # parts = re.split(r'([，,。\.！？\?!；;])', question)
    sentences = [''.join(parts[i:i+2]) for i in range(0, len(parts), 2)]

    # 2. 根据 confusion_level 进行打乱
    shuffled_sentences = sentences.copy()

    if confusion_level > 0 and len(sentences) > 1:
        swap_times = int(len(sentences) * confusion_level)

        for _ in range(swap_times):
            i, j = random.sample(range(len(sentences)), 2)
            shuffled_sentences[i], shuffled_sentences[j] = (
                shuffled_sentences[j],
                shuffled_sentences[i],
            )

    shuffled_question = ''.join(shuffled_sentences)

    # 4. 写入 CSV（追加写入）
    file_exists = os.path.exists(save_file_path)

    with open(save_file_path, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        # 如果文件不存在，先写表头
        if not file_exists:
            writer.writerow(["original_question", "Test Shuffle Question Sentence", "answer"])

        writer.writerow([question, shuffled_question, answer])

    return save_file_path

def shuffle_question_word(question, confusion_level, save_file_path):
    """
    question: str 原始问题（单词以空格分隔）
    confusion_level: float (0~1) 打乱强度
    save_file_path: str csv文件路径
    """

    # 1. 按空格拆分单词
    words = question.split()

    shuffled_words = words.copy()

    # 2. 根据 confusion_level 进行单词打乱
    if confusion_level > 0 and len(words) > 1:
        swap_times = int(len(words) * confusion_level)

        for _ in range(swap_times):
            i, j = random.sample(range(len(words)), 2)
            shuffled_words[i], shuffled_words[j] = (
                shuffled_words[j],
                shuffled_words[i],
            )

    shuffled_question = " ".join(shuffled_words)

    # 3. 固定 answer
    answer = "reject"

    # 4. 写入 CSV（追加写入）
    file_exists = os.path.exists(save_file_path)

    with open(save_file_path, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["original_question", "Test Shuffle Question Word", "answer"])

        writer.writerow([question, shuffled_question, answer])

def add_redundant_background(question,answer,redundant_level,redundant_infor_list,save_file_path):
    # 1. 按句号等分割句子（保留原意，不保留分隔符）
    sentences = re.split(r'[。!！？?]', question)
    sentences = [s.strip() for s in sentences if s.strip()]

    # 如果句子太少，直接在末尾插
    insert_positions = list(range(len(sentences) + 1))

    # 实际插入数量（不超过可插位置）
    insert_num = min(redundant_level, len(insert_positions))

    # 随机选择插入位置
    chosen_positions = sorted(
        random.sample(insert_positions, insert_num),
        reverse=True
    )

    # 随机选择冗余信息
    redundant_infos = random.choices(redundant_infor_list, k=insert_num)

    # 插入冗余背景信息
    for pos, info in zip(chosen_positions, redundant_infos):
        sentences.insert(pos, info)

    # 重新拼接成新的 question
    new_question = "。".join(sentences) + "。"

    # 3. 写入 CSV（追加写入）
    file_exists = os.path.exists(save_file_path)

    with open(save_file_path, mode="a", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)

        # 如果文件不存在，先写表头
        if not file_exists:
            writer.writerow([
                "original_question",
                "Test Redudant Background Question",
                "original_answer"
            ])

        writer.writerow([question,new_question,answer])
    pass

def add_redundant_conditions(question,answer,redundant_level,redundant_conditions_list,save_file_path):
    # 1. 按句号等分割句子（保留原意，不保留分隔符）
    sentences = re.split(r'[。!！？?]', question)
    sentences = [s.strip() for s in sentences if s.strip()]

    # 如果句子太少，直接在末尾插
    insert_positions = list(range(len(sentences) + 1))

    # 实际插入数量（不超过可插位置）
    insert_num = min(redundant_level, len(insert_positions))

    # 随机选择插入位置
    chosen_positions = sorted(
        random.sample(insert_positions, insert_num),
        reverse=True
    )

    # 随机选择冗余信息
    redundant_infos = random.choices(redundant_conditions_list, k=insert_num)

    # 插入条件景信息
    for pos, info in zip(chosen_positions, redundant_infos):
        sentences.insert(pos, info)

    # 重新拼接成新的 question
    new_question = "。".join(sentences) + "。"

    # 3. 写入 CSV（追加写入）
    file_exists = os.path.exists(save_file_path)

    with open(save_file_path, mode="a", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)

        # 如果文件不存在，先写表头
        if not file_exists:
            writer.writerow([
                "original_question",
                "Test Redudant Conditions Question",
                "original_answer"
            ])

        writer.writerow([question, new_question, answer])
    pass



with open(r".\private data\TPBench Calculation-masked-done.csv", newline='', encoding="utf-8") as infile:

    reader = csv.reader(infile)

    for row_idx, row in enumerate(reader, start=1):
        question = row[0]
        # print(question)
        # add_redundant_background(question=question,
        #                          answer="None",
        #                          redundant_level=2,
        #                          redundant_infor_list=redundant_infor_list,
        #                          save_file_path=r'.\Private Seed Data\AstroMathBench\uncoded\Derive\Output.csv')

        # add_redundant_conditions(question=question,
        #                          answer="None",
        #                          redundant_level=2,
        #                          redundant_conditions_list=redundant_conditions_list,
        #                          save_file_path=r'.\Private Seed Data\AstroMathBench\uncoded\Derive\Output.csv')

        shuffle_question_sentence(question=question,
                                  answer="None",
                                  confusion_level=0.4,
                                  save_file_path=r'.\Private Seed Data\AstroMathBench\uncoded\Derive\Output.csv')

        # shuffle_question_word(question=question,
        #                       confusion_level=0.4,
        #                       save_file_path=r'.\Private Seed Data\AstroMathBench\uncoded\Derive\Output.csv')


def Process_disruption(args):
    # This script parses step-structured solutions in a CSV file,
    # deletes half of the steps in forward, middle, or backward order,
    # inserts a <Replace> token at the first deletion point, and saves the resulting variants.
    df = pd.read_csv(Path(args.input))
    col = args.col

    # Candidate regex patterns for step headers
    # (tested in priority order; the first pattern that matches at least once is used)
    STEP_HEADER_PATTERNS: list[re.Pattern] = [
        # #### Step1: / #### Step 1 / ####step1:
        re.compile(
            r"^\s*####\s*step\s*0*(\d+)\s*(?:[:：])?\s*",
            flags=re.IGNORECASE | re.MULTILINE,
        ),
        # ### Step1: / ### Step 1 / ###step1:
        re.compile(
            r"^\s*###\s*step\s*0*(\d+)\s*(?:[:：])?\s*",
            flags=re.IGNORECASE | re.MULTILINE,
        ),
        # ** Step1: / **Step 1:
        re.compile(
            r"^\s*\*\*\s*step\s*0*(\d+)\s*(?:[:：])?\s*",
            flags=re.IGNORECASE | re.MULTILINE,
        ),
        # Step1: / Step 1:
        re.compile(
            r"^\s*step\s*0*(\d+)\s*(?:[:：])?\s*",
            flags=re.IGNORECASE | re.MULTILINE,
        ),
        # **1 / ** 1 / **01:
        re.compile(
            r"^\s*\*\*\s*0*(\d+)\s*(?:[:：])?\s*",
            flags=re.IGNORECASE | re.MULTILINE,
        ),
        # 1. **.....**  /  1) **.....**  /  01. **.....**
        # Treat "number + delimiter (. or )) + optional space + **...**" as a step header
        re.compile(
            r"^\s*0*(\d+)\s*[\.\)]\s*\*\*.*?\*\*\s*(?:[:：])?\s*",
            flags=re.IGNORECASE | re.MULTILINE,
        ),
    ]

    def _pick_step_header_re(text: str) -> re.Pattern | None:
        """Select the first step-header regex (by priority) that matches the text."""
        for pat in STEP_HEADER_PATTERNS:
            if pat.search(text or ""):
                return pat
        return None

    def split_steps(text: str):
        """
        Split text into step blocks (each block is header + body).
        Returns: (steps, prefix)

        - prefix: content before the first step header (may be empty)
        - steps: blocks from each step header up to the next step header
        """
        if text is None:
            return [], ""
        text = str(text)
        if not text.strip():
            return [], ""

        step_re = _pick_step_header_re(text)
        if not step_re:
            return [], text.strip()

        matches = list(step_re.finditer(text))
        if not matches:
            return [], text.strip()

        prefix = text[: matches[0].start()].strip()
        steps = []

        for i, m in enumerate(matches):
            start = m.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            steps.append(text[start:end].rstrip())

        return steps, prefix

    def join_chunks(prefix: str, steps: list[str]) -> str:
        parts = []
        if prefix and prefix.strip():
            parts.append(prefix.strip())
        parts.extend([s.strip() for s in steps if s and s.strip()])
        return "\n\n".join(parts).strip()

    def compute_mid_delete_indices(n: int, k: int):
        if k <= 0 or n <= 0:
            return []
        center = (n - 1) / 2.0
        order = sorted(range(n), key=lambda i: (abs(i - center), i))
        return order[:k]

    def delete_steps(
        steps: list[str],
        prefix: str,
        mode: str,
        delete_num: int,
        replace_token: str = "<Replace>",
    ):
        """
        Delete steps and insert <Replace> only once at the first deleted position.

        Returns: (remaining_text, deleted_text)
        """
        n = len(steps)
        k = max(0, min(delete_num, n))
        if n == 0 or k == 0:
            remaining = join_chunks(prefix, steps)
            return remaining, ""

        if mode == "forward":
            del_idx = list(range(k))
        elif mode == "back":
            del_idx = list(range(n - k, n))
        elif mode == "mid":
            del_idx = compute_mid_delete_indices(n, k)
        else:
            raise ValueError(f"Unknown mode: {mode}")

        del_set = set(del_idx)
        first_pos = min(del_idx)

        remaining_steps = []
        for i, s in enumerate(steps):
            if i == first_pos:
                remaining_steps.append(replace_token)
            if i in del_set:
                continue
            remaining_steps.append(s)

        deleted_steps = [steps[i] for i in sorted(del_idx)]

        remaining_text = join_chunks(prefix, remaining_steps)
        deleted_text = "\n\n".join(s.strip() for s in deleted_steps if s.strip()).strip()

        return remaining_text, deleted_text

    if col not in df.columns:
        raise KeyError(f"Column '{col}' not found.")

    out = df[[col]].copy()

    steps_num_list = []
    forward_step_list, forward_delete_list = [], []
    mid_step_list, mid_delete_list = [], []
    back_step_list, back_delete_list = [], []

    for val in out[col].tolist():
        raw_text = "" if val is None else str(val)

        steps, prefix = split_steps(raw_text)

        steps_num = len(steps)
        delete_num = steps_num // 2
        steps_num_list.append(steps_num)

        # === Special case: no steps ===
        if steps_num == 0:
            forward_step_list.append("No Step")
            forward_delete_list.append("No Step")

            mid_step_list.append("No Step")
            mid_delete_list.append("No Step")

            back_step_list.append("No Step")
            back_delete_list.append("No Step")
            continue

        # === Special case: only one step ===
        if steps_num == 1:
            only_step = steps[0].strip()
            replaced_prefix = prefix.strip() if prefix else ""
            replaced_text = join_chunks(replaced_prefix, ["<Replace>"])

            forward_step_list.append(replaced_text)
            forward_delete_list.append(only_step)

            mid_step_list.append(replaced_text)
            mid_delete_list.append(only_step)

            back_step_list.append(replaced_text)
            back_delete_list.append(only_step)
            continue

        # === forward / back ===
        f_rem, f_del = delete_steps(steps, prefix, "forward", delete_num)
        b_rem, b_del = delete_steps(steps, prefix, "back", delete_num)

        forward_step_list.append(f_rem)
        forward_delete_list.append(f_del)

        back_step_list.append(b_rem)
        back_delete_list.append(b_del)

        # === mid ===
        if steps_num < 3:
            mid_step_list.append("")
            mid_delete_list.append("")
        else:
            m_rem, m_del = delete_steps(steps, prefix, "mid", delete_num)
            mid_step_list.append(m_rem)
            mid_delete_list.append(m_del)

    out["steps_num"] = steps_num_list
    out["forward_step"] = forward_step_list
    out["forward_delete"] = forward_delete_list
    out["mid_step"] = mid_step_list
    out["mid_delete"] = mid_delete_list
    out["back_step"] = back_step_list
    out["back_delete"] = back_delete_list

    result = out[
        [
            col,
            "steps_num",
            "forward_step",
            "forward_delete",
            "mid_step",
            "mid_delete",
            "back_step",
            "back_delete",
        ]
    ]
    result.to_csv(Path(args.output), index=False, encoding="utf-8-sig")

parser = argparse.ArgumentParser(
        description=(
            "Process ORI solution steps: count steps, delete steps "
            "(forward/mid/back), and insert <Replace> at the first deleted position."
        )
    )
    parser.add_argument(
        "--input",
        type=str,
        default=r"your_path.csv",
        help="Input CSV path."
    )
    parser.add_argument(
        "--output",
        type=str,
        default=r"your_path.csv",
        help="Output CSV path."
    )
    parser.add_argument(
        "--col",
        type=str,
        default="Test Ori Solution",
        help="Column name containing original solution steps."
    )
    args = parser.parse_args()
    # Process_disruption(args)