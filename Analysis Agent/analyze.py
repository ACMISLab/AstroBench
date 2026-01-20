# ===================================== main_exp Formula Derivation (FD) ===================================================
main_FD_analyze_prompt = """
You are an expert analyst proficient in astronomy, physics, and mathematical reasoning. Your task is to analyze the model performance in the Formula Derivation (FD) task based on the model evaluation results.

Task definition description:
Formula Derivation (FD): This type of question asks an LLM to derive a mathematical or physical formula related to astronomy from fundamental principles, known laws, or given conditions. It requires the LLM to understand the underlying astronomical concepts, physical assumptions, and logical steps involved in the derivation process.

Evaluation metrics description: use five process-oriented metrics to evaluate model responses
1. Correctness (0-10)
Are the core facts, logic, and conclusions consistent with the Reference Solution? Are there any factual errors or incorrect reasoning?
2. Completeness (0-10)
Does the Candidate Answer cover all key points present in the Reference Solution? Are any important elements missing?
3. Relevance (0-10)
Is the solution focused on the question? Does it avoid unnecessary or irrelevant information?
4. Clarity & Coherence (0-10)
Is the solution well-structured and easy to understand? Are explanations clear and logically connected?
5. Precision & Detail (0-10)
Does the level of detail appropriately match the Reference Solution? Are concepts expressed accurately without being vague or misleading?

Below are the evaluation results for the Formula Derivation (FD) task under different experimental settings:
Ori: Original input
+Think: Engage in slow thinking
+CoT: Use chain-of-thought prompts for step-by-step derivation
−System: Remove system prompts, keep only user input
+Image: Include relevant image information

Evaluation results:
{result}

Please generate a concise analysis report based on these evaluation results, focusing on:
1. The model's overall performance and trends in formula derivation ability across different experimental settings.
2. Based on the above observations, a summary judgment of the model's capability boundaries for this task.

Requirements:
- Focus on overall trends and common patterns, avoiding a detailed enumeration of scores or experimental settings.
- The report should be concise, objective, and analysis-oriented, avoiding subjective speculation.
- - Output a single, concise paragraph of coherent natural language analysis focused on trends and key insights.
"""

# ===================================== main_exp Computational Reasoning (CR) ===================================================
main_CR_analyze_prompt = """
You are an expert analyst proficient in astronomy, physics, and mathematical reasoning. Your task is to analyze the model performance in the Computational Reasoning (CR) task based on the model evaluation results.

Task definition description:
Computational Reasoning (CR): This type of question evaluates an LLM’s ability to perform multi-step reasoning that involves quantitative analysis in astronomical contexts. Rather than focusing solely on final numerical results, it emphasizes the reasoning process that connects physical concepts, assumptions, and intermediate calculations. 

Evaluation metrics description: use five process-oriented metrics and Accuracy to evaluate model responses
1. Correctness (0-10)
Are the core facts, logic, and conclusions consistent with the Reference Solution? Are there any factual errors or incorrect reasoning?
2. Completeness (0-10)
Does the Candidate Answer cover all key points present in the Reference Solution? Are any important elements missing?
3. Relevance (0-10)
Is the solution focused on the question? Does it avoid unnecessary or irrelevant information?
4. Clarity & Coherence (0-10)
Is the solution well-structured and easy to understand? Are explanations clear and logically connected?
5. Precision & Detail (0-10)
Does the level of detail appropriately match the Reference Solution? Are concepts expressed accurately without being vague or misleading?
6. Accuracy ('Consistent' or 'Inconsistent')
Whether the Candidate Answer is truly consistent with the Reference Answer.

Below are the evaluation results for the Computational Reasoning (CR) task under different experimental settings:
Ori: Original input
+Think: Engage in slow thinking
+CoT: Use chain-of-thought prompts for step-by-step derivation
−System: Remove system prompts, keep only user input
+Image: Include relevant image information

Evaluation results:
{result}

Please generate a concise analysis report based on these evaluation results, focusing on:
1. The model's overall performance and trends in computational reasoning ability across different experimental settings.
2. The relationship between Accuracy and process-oriented evaluation metrics.
3. Based on the above observations, a summary judgment of the model's capability boundaries for this task.

Requirements:
- Focus on overall trends and common patterns, avoiding a detailed enumeration of scores or experimental settings.
- The report should be concise, objective, and analysis-oriented, avoiding subjective speculation.
- Output a single, concise paragraph of coherent natural language analysis focused on trends and key insights.
"""

# ===================================== main_exp Formula Calculation (FC) ===================================================
main_FC_analyze_prompt = """
You are an expert analyst proficient in astronomy, physics, and mathematical reasoning. Your task is to analyze the model performance in the Formula Calculation (FC) task based on the model evaluation results.

Task definition description:
Formula Calculation (FC): This type of question requires an LLM to apply established astronomical or physical formulae to compute specific numerical results. It tests the LLM’s ability to correctly identify relevant equations, substitute appropriate parameters, handle units, and carry out accurate mathematical calculations.

Evaluation metrics description: use five process-oriented metrics and Accuracy to evaluate model responses
1. Correctness (0-10)
Are the core facts, logic, and conclusions consistent with the Reference Solution? Are there any factual errors or incorrect reasoning?
2. Completeness (0-10)
Does the Candidate Answer cover all key points present in the Reference Solution? Are any important elements missing?
3. Relevance (0-10)
Is the solution focused on the question? Does it avoid unnecessary or irrelevant information?
4. Clarity & Coherence (0-10)
Is the solution well-structured and easy to understand? Are explanations clear and logically connected?
5. Precision & Detail (0-10)
Does the level of detail appropriately match the Reference Solution? Are concepts expressed accurately without being vague or misleading?
6. Accuracy ('Consistent' or 'Inconsistent')
Whether the Candidate Answer is truly consistent with the Reference Answer.

Below are the evaluation results for the Formula Calculation (FC) task under different experimental settings:
Ori: Original input
+Think: Engage in slow thinking
+CoT: Use chain-of-thought prompts for step-by-step derivation
−System: Remove system prompts, keep only user input
+Image: Include relevant image information

Evaluation results:
{result}

Please generate a concise analysis report based on these evaluation results, focusing on:
1. The model's overall performance and trends in formula calculation ability across different experimental settings.
2. The relationship between Accuracy and process-oriented evaluation metrics.
3. Based on the above observations, a summary judgment of the model's capability boundaries for this task.

Requirements:
- Focus on overall trends and common patterns, avoiding a detailed enumeration of scores or experimental settings.
- The report should be concise, objective, and analysis-oriented, avoiding subjective speculation.
- Output a single, concise paragraph of coherent natural language analysis focused on trends and key insights.
"""

# ===================================== main_exp ===================================================
main_analyze_prompt = """
You are an expert analyst in large language model evaluation and scientific reasoning. Your task is to synthesize analysis reports from multiple tasks.

Task definition description:
Formula Derivation (FD): This type of question asks an LLM to derive a mathematical or physical formula related to astronomy from fundamental principles, known laws, or given conditions. It requires the LLM to understand the underlying astronomical concepts, physical assumptions, and logical steps involved in the derivation process.
Computational Reasoning (CR): This type of question evaluates an LLM’s ability to perform multi-step reasoning that involves quantitative analysis in astronomical contexts. Rather than focusing solely on final numerical results, it emphasizes the reasoning process that connects physical concepts, assumptions, and intermediate calculations. 
Formula Calculation (FC): This type of question requires an LLM to apply established astronomical or physical formulae to compute specific numerical results. It tests the LLM’s ability to correctly identify relevant equations, substitute appropriate parameters, handle units, and carry out accurate mathematical calculations.

Evaluation metrics description: use five process-oriented metrics and Accuracy to evaluate model responses
1. Correctness (0-10)
Are the core facts, logic, and conclusions consistent with the Reference Solution? Are there any factual errors or incorrect reasoning?
2. Completeness (0-10)
Does the Candidate Answer cover all key points present in the Reference Solution? Are any important elements missing?
3. Relevance (0-10)
Is the solution focused on the question? Does it avoid unnecessary or irrelevant information?
4. Clarity & Coherence (0-10)
Is the solution well-structured and easy to understand? Are explanations clear and logically connected?
5. Precision & Detail (0-10)
Does the level of detail appropriately match the Reference Solution? Are concepts expressed accurately without being vague or misleading?
6. Accuracy ('Consistent' or 'Inconsistent')
Whether the Candidate Answer is truly consistent with the Reference Answer.

Below are the evaluation results under different experimental settings:
Ori: Original input
+Think: Engage in slow thinking
+CoT: Use chain-of-thought prompts for step-by-step derivation
−System: Remove system prompts, keep only user input
+Image: Include relevant image information

Analyze results:
Formula Derivation (FD) Analyze Result:
{FD_analyze_result}
Computational Reasoning (CR) Analyze Result:
{CR_analyze_result}
Formula Calculation (FC) Analyze Result:
{FC_analyze_result}

Please generate a concise overall analysis based on these reports, focusing on:
1. The model’s overall performance and trends in computational reasoning ability across different experimental settings.
2. The relationship between process-oriented evaluation metrics and Accuracy across different tasks.
3. Any evaluation dimensions that consistently appear as strengths or weaknesses across multiple tasks.
4. A synthesized judgment of the model’s overall capability boundaries and limitations in astronomy-related computational reasoning tasks.

Requirements:
1. Focus on cross-task commonalities and differences; do not repeat details from single-task analyses.
2. The report should be concise, objective, and analysis-oriented, avoiding subjective speculation.
3. Output a single, concise paragraph of coherent natural language analysis focused on trends and key insights.
"""

# ===================================== derivation_exp Formula Derivation (FD) ===================================================
derivation_FD_analyze_prompt = """
You are an expert analyst proficient in astronomy, physics, and mathematical reasoning. Your task is to analyze the model performance in the Formula Derivation (FD) task based on the model evaluation results.

Task definition description:
Formula Derivation (FD): This type of question asks an LLM to derive a mathematical or physical formula related to astronomy from fundamental principles, known laws, or given conditions. It requires the LLM to understand the underlying astronomical concepts, physical assumptions, and logical steps involved in the derivation process.

Evaluation metrics description: use five process-oriented metrics to evaluate model responses
1. Correctness (0-10)
Are the core facts, logic, and conclusions consistent with the Reference Solution? Are there any factual errors or incorrect reasoning?
2. Completeness (0-10)
Does the Candidate Answer cover all key points present in the Reference Solution? Are any important elements missing?
3. Relevance (0-10)
Is the solution focused on the question? Does it avoid unnecessary or irrelevant information?
4. Clarity & Coherence (0-10)
Is the solution well-structured and easy to understand? Are explanations clear and logically connected?
5. Precision & Detail (0-10)
Does the level of detail appropriately match the Reference Solution? Are concepts expressed accurately without being vague or misleading?

Below are the evaluation results for the Formula Derivation (FD) task under different experimental settings:
Shuffle Sentence: Shuffle the order of sentences in the input.
Shuffle Word Order: Shuffle the order of words within sentences.
Redundant Background: Add extra irrelevant background information.
Redundant Conditions: Include additional unnecessary conditions in the question.
Condition Damage: Alter or corrupt some of the conditions in the question.
Condition Missing: Remove some essential conditions from the question.
Knowledge Redefinition: Change or redefine domain knowledge in the input.
Reasoning Forward: Encourage step-by-step reasoning in forward order.
Intermediate Reasoning: Mask some intermediate reasoning steps to test completion.
Reasoning Backward: Encourage reasoning in backward order from conclusion to premises.

Evaluation results:
{result}

Please generate a concise analysis report based on these evaluation results, focusing on:
1. The model's overall performance and trends in formula derivation ability across different experimental settings.
2. Based on the above observations, a summary judgment of the model's capability boundaries for this task.

Requirements:
- Focus on overall trends and common patterns, avoiding a detailed enumeration of scores or experimental settings.
- The report should be concise, objective, and analysis-oriented, avoiding subjective speculation.
- - Output a single, concise paragraph of coherent natural language analysis focused on trends and key insights.
"""

# ===================================== derivation_exp Computational Reasoning (CR) ===================================================
derivation_CR_analyze_prompt = """
You are an expert analyst proficient in astronomy, physics, and mathematical reasoning. Your task is to analyze the model performance in the Computational Reasoning (CR) task based on the model evaluation results.

Task definition description:
Computational Reasoning (CR): This type of question evaluates an LLM’s ability to perform multi-step reasoning that involves quantitative analysis in astronomical contexts. Rather than focusing solely on final numerical results, it emphasizes the reasoning process that connects physical concepts, assumptions, and intermediate calculations. 

Evaluation metrics description: use five process-oriented metrics and Accuracy to evaluate model responses
1. Correctness (0-10)
Are the core facts, logic, and conclusions consistent with the Reference Solution? Are there any factual errors or incorrect reasoning?
2. Completeness (0-10)
Does the Candidate Answer cover all key points present in the Reference Solution? Are any important elements missing?
3. Relevance (0-10)
Is the solution focused on the question? Does it avoid unnecessary or irrelevant information?
4. Clarity & Coherence (0-10)
Is the solution well-structured and easy to understand? Are explanations clear and logically connected?
5. Precision & Detail (0-10)
Does the level of detail appropriately match the Reference Solution? Are concepts expressed accurately without being vague or misleading?
6. Accuracy ('Consistent' or 'Inconsistent')
Whether the Candidate Answer is truly consistent with the Reference Answer.

Below are the evaluation results for the Computational Reasoning (CR) task under different experimental settings:
Shuffle Sentence: Shuffle the order of sentences in the input.
Shuffle Word Order: Shuffle the order of words within sentences.
Redundant Background: Add extra irrelevant background information.
Redundant Conditions: Include additional unnecessary conditions in the question.
Condition Damage: Alter or corrupt some of the conditions in the question.
Condition Missing: Remove some essential conditions from the question.
Knowledge Redefinition: Change or redefine domain knowledge in the input.
Reasoning Forward: Encourage step-by-step reasoning in forward order.
Intermediate Reasoning: Mask some intermediate reasoning steps to test completion.
Reasoning Backward: Encourage reasoning in backward order from conclusion to premises.

Evaluation results:
{result}

Please generate a concise analysis report based on these evaluation results, focusing on:
1. The model's overall performance and trends in computational reasoning ability across different experimental settings.
2. The relationship between Accuracy and process-oriented evaluation metrics.
3. Based on the above observations, a summary judgment of the model's capability boundaries for this task.

Requirements:
- Focus on overall trends and common patterns, avoiding a detailed enumeration of scores or experimental settings.
- The report should be concise, objective, and analysis-oriented, avoiding subjective speculation.
- Output a single, concise paragraph of coherent natural language analysis focused on trends and key insights.
"""

# ===================================== derivation_exp Formula Calculation (FC) ===================================================
derivation_FC_analyze_prompt = """
You are an expert analyst proficient in astronomy, physics, and mathematical reasoning. Your task is to analyze the model performance in the Formula Calculation (FC) task based on the model evaluation results.

Task definition description:
Formula Calculation (FC): This type of question requires an LLM to apply established astronomical or physical formulae to compute specific numerical results. It tests the LLM’s ability to correctly identify relevant equations, substitute appropriate parameters, handle units, and carry out accurate mathematical calculations.

Evaluation metrics description: use five process-oriented metrics and Accuracy to evaluate model responses
1. Correctness (0-10)
Are the core facts, logic, and conclusions consistent with the Reference Solution? Are there any factual errors or incorrect reasoning?
2. Completeness (0-10)
Does the Candidate Answer cover all key points present in the Reference Solution? Are any important elements missing?
3. Relevance (0-10)
Is the solution focused on the question? Does it avoid unnecessary or irrelevant information?
4. Clarity & Coherence (0-10)
Is the solution well-structured and easy to understand? Are explanations clear and logically connected?
5. Precision & Detail (0-10)
Does the level of detail appropriately match the Reference Solution? Are concepts expressed accurately without being vague or misleading?
6. Accuracy ('Consistent' or 'Inconsistent')
Whether the Candidate Answer is truly consistent with the Reference Answer.

Below are the evaluation results for the Formula Calculation (FC) task under different experimental settings:
Shuffle Sentence: Shuffle the order of sentences in the input.
Shuffle Word Order: Shuffle the order of words within sentences.
Redundant Background: Add extra irrelevant background information.
Redundant Conditions: Include additional unnecessary conditions in the question.
Condition Damage: Alter or corrupt some of the conditions in the question.
Condition Missing: Remove some essential conditions from the question.
Knowledge Redefinition: Change or redefine domain knowledge in the input.
Reasoning Forward: Encourage step-by-step reasoning in forward order.
Intermediate Reasoning: Mask some intermediate reasoning steps to test completion.
Reasoning Backward: Encourage reasoning in backward order from conclusion to premises.

Evaluation results:
{result}

Please generate a concise analysis report based on these evaluation results, focusing on:
1. The model's overall performance and trends in formula calculation ability across different experimental settings.
2. The relationship between Accuracy and process-oriented evaluation metrics.
3. Based on the above observations, a summary judgment of the model's capability boundaries for this task.

Requirements:
- Focus on overall trends and common patterns, avoiding a detailed enumeration of scores or experimental settings.
- The report should be concise, objective, and analysis-oriented, avoiding subjective speculation.
- Output a single, concise paragraph of coherent natural language analysis focused on trends and key insights.
"""

# ===================================== derivation_exp ===================================================
derivation_analyze_prompt = """
You are an expert analyst in large language model evaluation and scientific reasoning. Your task is to synthesize analysis reports from multiple tasks.

Task definition description:
Formula Derivation (FD): This type of question asks an LLM to derive a mathematical or physical formula related to astronomy from fundamental principles, known laws, or given conditions. It requires the LLM to understand the underlying astronomical concepts, physical assumptions, and logical steps involved in the derivation process.
Computational Reasoning (CR): This type of question evaluates an LLM’s ability to perform multi-step reasoning that involves quantitative analysis in astronomical contexts. Rather than focusing solely on final numerical results, it emphasizes the reasoning process that connects physical concepts, assumptions, and intermediate calculations. 
Formula Calculation (FC): This type of question requires an LLM to apply established astronomical or physical formulae to compute specific numerical results. It tests the LLM’s ability to correctly identify relevant equations, substitute appropriate parameters, handle units, and carry out accurate mathematical calculations.

Evaluation metrics description: use five process-oriented metrics and Accuracy to evaluate model responses
1. Correctness (0-10)
Are the core facts, logic, and conclusions consistent with the Reference Solution? Are there any factual errors or incorrect reasoning?
2. Completeness (0-10)
Does the Candidate Answer cover all key points present in the Reference Solution? Are any important elements missing?
3. Relevance (0-10)
Is the solution focused on the question? Does it avoid unnecessary or irrelevant information?
4. Clarity & Coherence (0-10)
Is the solution well-structured and easy to understand? Are explanations clear and logically connected?
5. Precision & Detail (0-10)
Does the level of detail appropriately match the Reference Solution? Are concepts expressed accurately without being vague or misleading?
6. Accuracy ('Consistent' or 'Inconsistent')
Whether the Candidate Answer is truly consistent with the Reference Answer.

Below are the evaluation results under different experimental settings:
Shuffle Sentence: Shuffle the order of sentences in the input.
Shuffle Word Order: Shuffle the order of words within sentences.
Redundant Background: Add extra irrelevant background information.
Redundant Conditions: Include additional unnecessary conditions in the question.
Condition Damage: Alter or corrupt some of the conditions in the question.
Condition Missing: Remove some essential conditions from the question.
Knowledge Redefinition: Change or redefine domain knowledge in the input.
Reasoning Forward: Encourage step-by-step reasoning in forward order.
Intermediate Reasoning: Mask some intermediate reasoning steps to test completion.
Reasoning Backward: Encourage reasoning in backward order from conclusion to premises.

Analyze results:
Formula Derivation (FD) Analyze Result:
{FD_analyze_result}
Computational Reasoning (CR) Analyze Result:
{CR_analyze_result}
Formula Calculation (FC) Analyze Result:
{FC_analyze_result}

Please generate a concise overall analysis based on these reports, focusing on:
1. The model’s overall performance and trends in computational reasoning ability across different experimental settings.
2. The relationship between process-oriented evaluation metrics and Accuracy across different tasks.
3. Any evaluation dimensions that consistently appear as strengths or weaknesses across multiple tasks.
4. A synthesized judgment of the model’s overall capability boundaries and limitations in astronomy-related computational reasoning tasks.

Requirements:
1. Focus on cross-task commonalities and differences; do not repeat details from single-task analyses.
2. The report should be concise, objective, and analysis-oriented, avoiding subjective speculation.
3. Output a single, concise paragraph of coherent natural language analysis focused on trends and key insights.
"""

