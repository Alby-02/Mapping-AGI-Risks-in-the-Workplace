import pandas as pd

N = 10
file_name = "Stable_AGI,AII Score Dataset (Without Sectors).csv"
df = pd.read_csv(file_name)
#order by rank difference
df_rank_diff = df.sort_values(by="Auto-AII Rank-Diff", ascending=False).reset_index(drop=True)
#select only the columns "Auto-AII Rank-Diff", "Title", "Automation Rank", "AII Rank", "Auto-AII Rank-Diff"
df_aut = df_rank_diff[["Auto-AII Rank-Diff", "Title", "Automation Rank", "AII Rank", "Auto-AII Rank-Diff"]]
df_aut.head(N).to_csv(f"Top_{N}_Occupations_By_Rank_Diff_Auto.csv", index=True)
df_rank_diff = df.sort_values(by="Aug-AII Rank-Diff", ascending=False).reset_index(drop=True)
#select only the columns "Aug-AII Rank-Diff", "Title", "Augmentation Rank", "AII Rank", "Aug-AII Rank-Diff"
df_aug = df_rank_diff[["Aug-AII Rank-Diff", "Title", "Augmentation Rank", "AII Rank", "Aug-AII Rank-Diff"]]
df_aug.head(N).to_csv(f"Top_{N}_Occupations_By_Rank_Diff_Aug.csv", index=True)