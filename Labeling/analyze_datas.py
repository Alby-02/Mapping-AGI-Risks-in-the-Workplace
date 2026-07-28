import json
import re
from pathlib import Path
import pandas as pd

PLOT_LABEL_DISTRIBUTION = True  # Set to True to plot label distribution bar chart


# Load needed files
DATASET_FILE = Path("Dataset") /  "taskStatements.xlsx"
BATCH_OUTPUT_FILE = "output_full_no_patents.jsonl"
OUTPUT_MERGED_FILE = "merged_output_full_no_patents.txt"

# Load dataset
if not Path(DATASET_FILE).exists():
    raise FileNotFoundError(f"Dataset file not found: {DATASET_FILE}")
dataset_df = pd.read_excel(DATASET_FILE)
print(f"Loaded dataset with {len(dataset_df)} records.")

# Load batch output
if not Path(BATCH_OUTPUT_FILE).exists():
    raise FileNotFoundError(f"Batch output file not found: {BATCH_OUTPUT_FILE}")

# Parse batch output into a DataFrame
batch_records = []
with open(BATCH_OUTPUT_FILE, "r", encoding="utf-8") as f:
    current_custom_id = None
    current_json_lines = []
    for line in f:
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("[") and stripped.endswith("]"):
            # Save previous record if present
            if current_custom_id is not None and current_json_lines:
                raw_json = "\n".join(current_json_lines)
                data = json.loads(raw_json)
                batch_records.append({
                    "task_id": current_custom_id.split("-")[-1],
                    "label": data.get("Automation Score"),
                    "reasoning": data.get("Explanation")
                })
                current_json_lines = []

            current_custom_id = stripped[1:-1]
        else:
            current_json_lines.append(line)
# Save last record
if current_custom_id is not None and current_json_lines:
    raw_json = "\n".join(current_json_lines)
    data = json.loads(raw_json)
    batch_records.append({
        "task_id": current_custom_id.split("-")[-1],
        "label": data.get("Automation Score"),
        "reasoning": data.get("Explanation")
    })
batch_df = pd.DataFrame(batch_records)
print(f"Loaded batch output with {len(batch_df)} records.")


# Merge dataset with batch output on task_id

dataset_df = dataset_df[["Task ID", "Task", "Title"]] # Ensure task_id is string for merging
dataset_df = dataset_df.rename(columns={"Task ID": "task_id", "Task": "task_description", "Title": "occupation"})
dataset_df["task_id"] = dataset_df["task_id"].astype(str)

merged_df = pd.merge(dataset_df, batch_df, on="task_id", how="right")
merged_df = merged_df[["task_id", "label", "occupation", "task_description", "reasoning"]]
merged_df = merged_df.rename(columns={"reasoning": "label_explanation"})

#task_id    task_description    occupation    label   reasoning

print(f"Merged dataset has {len(merged_df)} records.")
print(merged_df.head())
with open(OUTPUT_MERGED_FILE, "w", encoding="utf-8") as f:
        f.write(merged_df.to_string(index=False))

#print label distribution
label_counts = merged_df["label"].value_counts()
print("Label distribution:")
print(label_counts)

#plot a bar chart of label distribution
if PLOT_LABEL_DISTRIBUTION:
    import matplotlib.pyplot as plt
    label_counts.plot(kind="bar")
    plt.title("Label Distribution")
    plt.xlabel("Label")
    plt.ylabel("Count")
    plt.xticks(rotation=0)
    plt.savefig("label_distribution.png")
#    plt.show()


df = merged_df
# Group by occupation, count occurrences of each label
grouped = df.groupby('occupation')['label'].value_counts().unstack(fill_value=0)

# Ensure all A-level columns are present even if missing in data
for col in ['A0', 'A1', 'A2', 'A3', 'A4']:
    if col not in grouped.columns:
        grouped[col] = 0

# Reorder columns and add a total count
grouped = grouped[['A0', 'A1', 'A2', 'A3', 'A4']]
grouped['total'] = grouped.sum(axis=1)

# Sort by total descending and reset index
grouped = grouped.sort_values('total', ascending=False).reset_index()
grouped = grouped[['occupation', 'A0', 'A1', 'A2', 'A3', 'A4', 'total']]

# Save to CSV
grouped.to_string('occupation_label_clusters.txt', index=False)

#redo but only consider A3 and A4
grouped_a3_a4 = df[df['label'].isin(['A3', 'A4'])].groupby('occupation')['label'].value_counts().unstack(fill_value=0)
grouped_a3_a4['total'] = grouped_a3_a4.sum(axis=1)
grouped_a3_a4 = grouped_a3_a4.sort_values('total', ascending=False).reset_index()
grouped_a3_a4 = grouped_a3_a4[['occupation', 'A3', 'A4', 'total']]
grouped_a3_a4.to_string('occupation_label_clusters_a3_a4.txt', index=False)
