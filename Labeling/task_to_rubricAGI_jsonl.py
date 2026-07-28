import pandas as pd
import json
from pathlib import Path

#Start and end index for partitioning the dataset and wether the dataset should be partitioned in the first place
PARTITION_DATASET = False #VERY IMPORTANT TO CHECK THIS TO TRUE IN CASE OF TESTING PURPOSES
PARTITION_START = 150
PARTITION_END = 200


labeling_prompt = Path("Prompts") / "Labeling" / "Labeling_Prompt_AGIv2.txt"
patent_dataset_path = Path("Dataset") / "patent_task_matches_percentile.csv"
full_dataset_path = Path("Dataset") / "TaskStatements.xlsx"


df_patent_tasks = pd.read_csv(patent_dataset_path)
df_full_tasks = pd.read_excel(full_dataset_path)
# Filter to get unique task_id and their descriptions
df_patent_tasks_unique = df_patent_tasks.drop_duplicates(subset=['task_id']).sort_values('task_id').reset_index(drop=True)
df_patent_tasks_unique.rename(columns={'task_id': 'Task ID'}, inplace=True)
df_patent_tasks_unique = df_patent_tasks_unique[['Task ID']]

#Eliminate tasks that are in the patent dataset from the full dataset
df_full_tasks = df_full_tasks[~df_full_tasks['Task ID'].isin(df_patent_tasks_unique['Task ID'])]
print("Full Tasks after eliminating patent tasks:")
print(f"Number of tasks: {len(df_full_tasks)}")
#print(df_full_tasks.head())
df_full_tasks_reduced = df_full_tasks[['Task ID', 'Title', 'Task']].sort_values('Task ID').reset_index(drop=True)
#print(df_full_tasks_reduced.head())

df_unique_tasks = df_full_tasks_reduced

# iterate over elemets of the dataframe
start_idx = PARTITION_START if PARTITION_DATASET else 0
end_idx = len(df_unique_tasks) if not PARTITION_DATASET else min(PARTITION_END, len(df_unique_tasks))


# Read the labeling prompt
with open(labeling_prompt, 'r', encoding='utf-8') as f:
    system_prompt = f.read().strip()

# Create JSONL file for batch processing
jsonl_filename = 'batch_input_full_no_patents.jsonl'

with open(jsonl_filename, 'w', encoding='utf-8') as f:
    for idx in range(start_idx, end_idx):
        task_id = df_unique_tasks.loc[idx, 'Task ID']
        task_description = df_unique_tasks.loc[idx, 'Task']
        occupation = df_unique_tasks.loc[idx, 'Title']

        # Create the JSON structure
        batch_request = {
            "custom_id": f"task-{task_id}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-5-nano",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f" Occupation: {occupation} \n Task: {task_description}"}
                ],
                "max_completion_tokens": 5000,
                "response_format": {"type": "json_object"}
            }
        }

        # Write to JSONL file
        f.write(json.dumps(batch_request) + '\n')
print(f"JSONL file '{jsonl_filename}' created with tasks from index {start_idx} to {end_idx-1}.")