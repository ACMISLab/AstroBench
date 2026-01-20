import csv
import jieba
import pandas as pd
import random
import re
from AstroMath.config import call_deepseek_v3_2,call_closeai_gpt5_1_syetem,call_qwen3_max_syetem
from similarity import calculate_similarity
from FlagEmbedding import FlagAutoModel

def split_sentences(text):
    pattern = r'([，。！？\?!；;]|(?<!\d)\.(?!\d)|(?<!\d),(?!\d))'
    parts = re.split(pattern, text)
    sentences = []
    for i in range(0, len(parts) - 1, 2):
        sentences.append(parts[i] + parts[i + 1])
    return [s.strip() for s in sentences if s.strip()]

def get_first_word(sentence):
    words = list(jieba.cut(sentence))
    for w in words:
        w = w.strip()
        if w:
            return w
    return None

def process_text(text):
    if not isinstance(text, str):
        return None, None, None

    sentences = split_sentences(text)

    # 只有一句话，不处理
    if len(sentences) <= 1:
        return None, None, None

    # 随机起点（必须保证有下一句话）
    start = random.randint(0, len(sentences) - 2)

    # 随机连续长度（至少 1 句）
    max_len = len(sentences) - start - 1
    length = random.randint(1, max_len)

    random_context = ''.join(sentences[start:start + length])
    masked_next_sentence = sentences[start + length]
    masked_next_word = get_first_word(masked_next_sentence)

    return random_context, masked_next_sentence, masked_next_word

def test_question_generate():
    df = pd.read_csv(r"xxx.csv", encoding="utf-8")

    results = df.iloc[:, 0].apply(process_text)

    df["random_context"] = results.apply(lambda x: x[0])
    df["masked_next_sentence"] = results.apply(lambda x: x[1])
    df["masked_next_word"] = results.apply(lambda x: x[2])

    # 保存结果
    df.to_csv(r"xxx.csv", encoding="utf-8-sig",index=False)

def pollution_random_testing(question):
    system = f'''You are a helpful autocomplete bot for astronomical math questions. You will be prompted with a partial question. Your task is to complete only the immediate next sentence, continuing the text naturally and consistently with the dataset. Output only the missing sentence, without quotation marks or additional commentary.'''
    prompt = f'Now, start your work. The given sentence is {question}'
    # answer = call_deepseek_v3_2(question=prompt,model="deepseek-chat",system=system)
    # answer = call_closeai_gpt5_1_syetem(question=prompt, system=system)
    answer = call_qwen3_max_syetem(question=prompt, system=system)
    return answer

def pollution_nextword_testing(question):
    system = f'''You are a helpful autocomplete bot for astronomical math questions. You will be prompted with a partial question. Your task is to complete only the immediate next word, continuing the text naturally and consistently with the dataset. Output only the missing word, without quotation marks or additional commentary.'''
    prompt = f'Now, start your work. The given sentence is {question}'
    # answer = call_deepseek_v3_2(question=prompt, model="deepseek-chat", system=system)
    # answer = call_closeai_gpt5_1_syetem(question=prompt, system=system)
    answer = call_qwen3_max_syetem(question=prompt, system=system)
    return answer

def testing(input_file,output_file):
    with open(input_file, 'r', encoding='utf-8', newline='') as infile:
        rows = list(csv.reader(infile))

    # 表头处理
    if rows:
        header = rows[0]
        if "nextword_testing_result" not in header:
            header.append("nextword_testing_result")

    num_cols = len(rows[0])  # 表头列数（包含 Answer）

    # 从第5行开始处理（索引4）
    for i in range(1, len(rows)):
        row = rows[i]
        # 补齐到表头列数 - 1（留出 Answer）
        while len(row) < num_cols - 1:
            row.append("")

        ori_question = row[1].strip()
        print(ori_question)

        if ori_question=="":
            answer = None
        else:
            try:
                answer = pollution_nextword_testing(ori_question)
            except Exception as e:
                print(f"第{i + 1}行处理出错: {e}")
                answer = ""

        # ===== 关键：保存 answer 到行 =====
        if len(row) == num_cols - 1:
            row.append(answer)      # 新增 Answer
        else:
            row[num_cols - 1] = answer  # 覆盖已有 Answer

        print(f"Done:{i}")

    # ===== 写入新的 CSV 文件 =====
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)

def score(input_file,output_file):
    # load encoding model
    model = FlagAutoModel.from_finetuned(r'.\bge-large-en-v1.5',
                                         use_fp16=True)

    with open(input_file, 'r', encoding='utf-8', newline='') as infile:
        rows = list(csv.reader(infile))

    # ===== Header processing =====
    if rows:
        header = rows[0]

        if "nextsentence_similarity" not in header:
            header.append("nextsentence_similarity")
        if "nextword_matched" not in header:
            header.append("nextword_matched")

    # Record column index
    sim_col_idx = header.index("nextsentence_similarity")
    word_col_idx = header.index("nextword_matched")

    num_cols = len(header)

    # ===== Line processing =====
    for i in range(1, len(rows)):
        row = rows[i]

        # 补齐列数
        while len(row) < num_cols:
            row.append("")

        masked_next_sentence = row[2].strip()
        llm_next_sentence = row[4].strip()
        masked_next_word = row[3].strip()
        llm_next_word = row[5].strip()

        if masked_next_sentence == "" or masked_next_word == "":
            score1 = "---"
            score2 = "---"
        else:
            try:
                score1 = calculate_similarity(
                    model=model,
                    related=llm_next_sentence,
                    target=masked_next_sentence,
                    open_eu=False
                )
                score2 = int(llm_next_word == masked_next_word)
            except Exception as e:
                print(f"第{i + 1}行处理出错: {e}")
                score1 = 0
                score2 = 0

        # ===== Write to specified column =====
        row[sim_col_idx] = score1
        row[word_col_idx] = score2

    # ===== 写入新的 CSV 文件 =====
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)