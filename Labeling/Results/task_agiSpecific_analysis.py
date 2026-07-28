import pandas as pd
#read the merged output file, wich was printed by df.to_txt
import pandas as pd

all_tasks_df = pd.read_excel("TaskStatements.xlsx")
all_tasks_df = all_tasks_df[["Task ID", "Title"]]
all_tasks_df.rename(columns={"Task ID": "task_id", "Title": "occupation"}, inplace=True)

df = pd.read_csv("merged_output_full_no_patents.csv")
df = df[["task_id", "label"]]

df_patent = pd.read_csv("patent_task_matches_percentile.csv")
df_patent = df_patent[["task_id"]].drop_duplicates().reset_index(drop=True)
df_patent["label"] = "P"

# Merge the df on task_id
all_tasks_df = all_tasks_df.merge(df, on="task_id", how="left")
all_tasks_df = all_tasks_df.merge(df_patent, on="task_id", how="left")
all_tasks_df["label"] = all_tasks_df["label_y"].combine_first(all_tasks_df["label_x"])
all_tasks_df = all_tasks_df[["task_id", "occupation", "label"]]

all_tasks_df.to_csv("merged_output_full_with_patents.csv", index=False)

#group by occupation and count the number of tasks in each label
occupation_counts = all_tasks_df.groupby("occupation")["label"].value_counts().unstack(fill_value=0).reset_index()
occupation_counts["AGI-specific"] = occupation_counts["A1"] + occupation_counts["A2"] + occupation_counts["A3"] + occupation_counts["A4"]
occupation_counts["NOT AGI-specific"] = occupation_counts["A0"] + occupation_counts["P"]
occupation_counts = occupation_counts[["occupation", "AGI-specific", "NOT AGI-specific"]]
occupation_counts = occupation_counts.sort_values("NOT AGI-specific", ascending=True)
occupation_counts.to_csv("occupation_counts.csv", index=False)
