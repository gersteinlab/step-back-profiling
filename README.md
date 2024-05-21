# Workflow of Step-back-Profiling

## Dataset Generation
1. Get sampled author list and paper list in JSON format: Dataset/data_construction.ipynb
2. Extract author's research interests: Dataset/s2orc-rq.ipynb 
3. Extract research questions from paper:  Dataset/research_question_extraction.ipynb

## For Results Generation for each task
1. Get User Profile: SSDatasetCode/author_profiling_cot.ipynb
2. Generate title for single author: SSDatasetCode/single_agent_title_generation.ipynb
3. Generate results for multiple authors & evaluation for each task: SSDatasetCode/taskx_solving.ipynb

## TO-DO:
1. Evaluation with BWS methods
2. Add more experiments if needed