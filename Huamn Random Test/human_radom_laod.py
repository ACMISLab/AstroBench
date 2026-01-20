import pandas as pd
pd.set_option('display.max_rows', None)
# 1. 读取数据（示例）
df = pd.read_excel(r".\Human Scale.xlsx",sheet_name="FC")
# 或
# df = pd.read_csv("raw_scores.csv")

# 2. 指定维度列 & 指标列
id_cols = ["Model", "Question", "Score Type"]
metric_cols = ["Score","正确性", "完整性", "相关性", "清晰度", "精确度", "ACC"]

# 3. 将宽表转换为长表（metric 一列）
long_df = df.melt(
    id_vars=id_cols,
    value_vars=metric_cols,
    var_name="metric",
    value_name="score"
)

# 4. 拆分 LLM / Human
llm_df = (
    long_df[long_df["Score Type"] == "LLM"]
    .rename(columns={"score": "llm_score"})
    .drop(columns=["Score Type"])
)

human_df = (
    long_df[long_df["Score Type"] == "Human"]
    .rename(columns={"score": "human_score"})
    .drop(columns=["Score Type"])
)

# 5. 合并 LLM & Human 分数
final_df = llm_df.merge(
    human_df,
    on=["Model", "Question", "metric"],
    how="inner"
)

# 6. 列名规范化（按你的要求）
final_df = final_df.rename(columns={
    "Model": "model",
    "Question": "question"
})

# 7. 排序（可选）
final_df = final_df.sort_values(
    by=["model", "question", "metric"]
).reset_index(drop=True)

print(final_df)
final_df.to_excel('FC.xlsx', index=False)

