<h1 align="center"> AstroBench </h1>

The official repository of **"AstroBench: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"**.
![image](https://github.com/ACMISLab/AstroBench/blob/main/Images/Framework.png)

## 🆕 News
- \[**January 2026**\] We have released the second version 2.0 and are very excited to share our research and insights into astronomical calculation reasoning!
- \[**June 2024**\] We have released the first version 1.0 and are very excited to share our research and insights into astronomical macromodeling!

## Review Dataset Introduction
AstroBench is a benchmark by xxx ACMIS Labs for large language model generation capabilities in the field of astronomy. In this test, the Chinese large language models tested are required to provide accurate and relevant answers to 2709 different types of questions under five subject categories: astrophysics, celestial mechanics, astronomy, history of astronomy, and astronomical techniques and methods. We have designed a comprehensive scoring system, for non-calculated questions, each of the terminology and short answer questions has a standardized reference answer, which is scored using multiple criteria and then weighted and summed. For objective questions, we extract the final answer and then combine the scores using a difficulty factor.

The dataset includes the following fields:

ID,Question,Options

## Directory Description
AstroBench Paper **Link to be added**<br>

## 💡 Prompt
Below are the prompts we use in our papers. You can also try your own designed prompts! Just change the prompts in the python code for each task and then we can see the results.

Furthermore, we have conducted extensive sensitivity and stability analyses on the prompt used, with the aim of selecting the optimal ones based on your specific circumstances (we highly recommend using our official prompt). The detailed experimental results are as follows:
### Settings
We designed 8 prompts (4 in Chinese and 4 in English, with Prompt0 being our recommendation) for experimentation under multiple-choice questions.

### Analysis
(1) Without system prompts, the scores of the three models, InternLM-20B, Llama3-8B, and StarWhisper3, experienced minor fluctuations but no significant improvement. This indicates that these models have low sensitivity to prompts and relatively stable performance without system prompts.
However, InternLM-7B and Qwen1.5-MoE-A2.7B showed a significant improvement in scores with English prompts compared to Chinese prompts. This may be due to these models' stronger processing ability for English data during training or that English prompts better align with the models' expected semantic expressions.

(2) When system prompts were used, the scores of the five large models fluctuated less, with overall stable performance. In particular, the three models, Llama3-8B, Qwen1.5-MoE-A2.7B, and StarWhisper3, showed improved results after using system prompts. This suggests that system prompts can effectively guide the models to generate higher-quality responses. Unexpectedly, however, InternLM-7B and InternLM-20B experienced a significant decrease in scores after using system prompts. This may be due to the unstable processing of system prompts by these two models, leading to performance degradation. The specific reasons may involve factors such as the models' parsing methods for system prompts and the compatibility between prompts and the models' internal knowledge bases. The detailed experimental results are as follows:

### Conclusion
(1) Language choice for prompts: Without system prompts, some models performed better with English prompts than with Chinese prompts. This suggests that we should consider the impact of language on model performance when designing prompts.

(2) Effectiveness of system prompts: system prompts effectively improved performance in most models, especially Llama3-8B, Qwen1.5-MoE-A2.7B, and StarWhisper3. This indicates that system prompts can serve as an effective guiding tool to help models generate higher-quality responses in specific domains.

(3) Model stability: The poor performance of InternLM-7B and InternLM-20B after using system prompts suggests that we need to conduct more stability tests on models in practical applications to ensure that system prompts do not lead to performance degradation.
Therefore, for the selection of test prompts, we prioritize the use of Prompt0 for evaluation, as it can adapt to different types of models and demonstrates good performance.

## 📌 Evaluation Methodology
After downloading the dataset, please ask the model questions using the prompts corresponding to the “Question Prompt” column, the relevant scripts are located in the scripts directory. The final results will be summarized in an xlsx file with an “Answer” column for each type of question to store the model's responses. Please note that the responses to the questions should correspond to the prompts and question numbers. Once all responses have been collected, please submit the xlsx file to the review site. 
**Link to be added**

The xlsx file you need to submit should refer to the following document:
Submit test samples.xlsx

We strongly recommend five different assessments for each question!

The site calculates scores automatically and you can choose whether or not to synchronize your scores to the leaderboard.

## 🤗 Citation
If you find the code and testset are useful in your research, please consider citing
```
Comming soon
```

## 🤗 Contact us
Fuyong Zhao: gs.fyzhao24@gzu.edu.cn

## License
The AstroBench dataset is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

