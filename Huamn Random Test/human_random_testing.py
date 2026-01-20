import pandas as pd
pd.set_option('display.max_rows', None)

metrics = ['Score', '正确性', '完整性', '相关性', '清晰度','精确度',"ACC"]

df = pd.read_excel(r".\FC.xlsx")

print(df)

#=================================Bias Analysis=================================
# 1️⃣ 单样本分差
df["score_diff"] = df["llm_score"] - df["human_score"]

# 2️⃣ 全局平均分差
mean_bias = df["score_diff"].mean()
print("Overall Mean Bias (LLM - Human):", mean_bias)

# 3️⃣ 按指标 / 模型 / 题目分析偏差（强烈建议）
# 按指标
bias_by_metric = df.groupby("metric")["score_diff"].mean()

# # 按模型
# bias_by_model = df.groupby("model")["score_diff"].mean()

print("Bias by Metric:\n", bias_by_metric)
# print("Bias by Model:\n", bias_by_model)


#=================================Correlation Analysis=================================
from scipy.stats import pearsonr, spearmanr

pearson_r, pearson_p = pearsonr(df["llm_score"], df["human_score"])
spearman_r, spearman_p = spearmanr(df["llm_score"], df["human_score"])

print(f"Pearson r = {pearson_r:.3f}, p = {pearson_p:.4f}")
print(f"Spearman ρ = {spearman_r:.3f}, p = {spearman_p:.4f}")


# 2️⃣ 按指标分别计算相关性（非常有说服力）
corr_by_metric = []

for met in metrics:
    sub = df[df["metric"] == met]
    r, _ = spearmanr(sub["llm_score"], sub["human_score"])
    corr_by_metric.append((met, r))

corr_df = pd.DataFrame(corr_by_metric, columns=["metric", "spearman_r"])
print(corr_df)

#=================================Correlation Analysis=================================
# ICC（Intraclass Correlation Coefficient）
import pingouin as pg

icc_df = df[["question", "metric", "llm_score", "human_score"]].copy()
icc_long = icc_df.melt(
    id_vars=["question", "metric"],
    value_vars=["llm_score", "human_score"],
    var_name="rater",
    value_name="score"
)

icc = pg.intraclass_corr(
    data=icc_long,
    targets="question",
    raters="rater",
    ratings="score"
)

icc_results = []

for metric in df["metric"].unique():
    sub = df[df["metric"] == metric]

    # 转为 long format（每个题目是一个 target）
    long_df = sub.melt(
        id_vars=["question"],
        value_vars=["llm_score", "human_score"],
        var_name="rater",
        value_name="score"
    )

    # 计算 ICC
    icc_all = pg.intraclass_corr(
        data=long_df,
        targets="question",
        raters="rater",
        ratings="score"
    )

    # 只取 ICC(2,1)
    icc_21 = icc_all[icc_all["Type"] == "ICC2"].iloc[0]

    icc_results.append({
        "metric": metric,
        "ICC(2,1)": icc_21["ICC"],
        "CI95%": icc_21["CI95%"],
        "F": icc_21["F"],
        "pval": icc_21["pval"]
    })

print(icc_results)
