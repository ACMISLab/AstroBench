<h1 align="center"> AstroBench </h1>

The official repository of **"AstroBench: A Benchmark for Computational Reasoning in Astronomy with Large Language Models"**.
![image](https://github.com/ACMISLab/AstroBench/blob/main/Images/Framework.png)

## 🆕 News
- \[**January 2026**\] We have released the second version 2.0 and are very excited to share our research and insights into astronomical calculation reasoning!
- \[**June 2024**\] We have released the first version 1.0 and are very excited to share our research and insights into astronomical macromodeling!

## Review Dataset Introduction
xxx xxx

The AstroBench Paper: **Comming Soon**<br>

## 💡 Directory Description
**Analysis Agent：** This directory contains the essential code required for the automatic analysis of reports.

**Cognitive Exp：** This directory includes test datasets and result files for cognitive derivative data, along with the necessary testing code.
Please note that the provided test data are variant datasets consistent with those used in the original paper and do not contain any private data.

**Data Pollution Test：** This directory contains the code required for data pollution testing, as well as the corresponding result files.

**Human Random Test：** This directory includes the necessary code for human evaluation experiments and their corresponding result files.

**Main Exp：** This directory contains test datasets and result files for five categories of fundamental task types, along with the required testing code.
Please note that the provided test data are variant datasets consistent with those used in the original paper and do not contain any private data.

**Private：** This directory contains tools used for evaluation and testing, as well as code for deriving results from private data.
Please note that private data are not publicly available.

## 💡 Prompt
xxx

### Settings
xxx

### Analysis
xxx

### Conclusion
In this work, we introduce the first evaluation benchmark specifically designed for computational and scientific reasoning in the astronomical domain. Unlike existing general-purpose or domain-agnostic benchmarks, our benchmark is explicitly constructed to support the long-term development and assessment of models capable of astronomical computation and scientific reasoning. A key distinguishing feature of our benchmark is its strong resistance to data contamination and its long-term validity, which substantially extends the lifecycle of benchmarks in data-scarce scientific domains such as astronomy. This property is critical for enabling reliable and fair evaluation of future models as they continue to scale and evolve.
The benchmark comprehensively covers a wide spectrum of foundational astronomical reasoning tasks, including formula derivation, computational reasoning, formula-based calculation, multimodal image–text computation, and code-based calculation. Beyond task-level performance, the benchmark is designed to probe deeper cognitive generalization boundaries of models, such as problem comprehension, robustness to condition perturbations, knowledge consistency, reverse reasoning ability, and resistance to irrelevant interference. As such, it provides a more holistic assessment of scientific reasoning capabilities than accuracy-focused benchmarks alone.

## 📌 Evaluation Methodology
After downloading the dataset, please ask the model questions using the prompts corresponding to the “Question Prompt” column, the relevant scripts are located in the scripts directory. The final results will be summarized in an xlsx file with an “Answer” column for each type of question to store the model's responses. Please note that the responses to the questions should correspond to the prompts and question numbers. Once all responses have been collected, please submit the xlsx file to the review site. 
**Link to be added**

## 🤗 Citation
If you find the code and testset are useful in your research, please consider citing
```
Comming soon
```

## 🤗 Contact us
Fuyong Zhao: gs.fyzhao24@gzu.edu.cn

## License
The AstroBench dataset is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

