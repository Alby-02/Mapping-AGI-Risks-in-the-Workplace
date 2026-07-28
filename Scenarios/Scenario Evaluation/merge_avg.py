#take different evaluation files and merge them by averaging the scores for each user and for each criteria

import pandas as pd
import matplotlib.pyplot as plt
aug_df_1 = pd.read_excel("AUG_Evaluation_Alberto.xlsx")
aug_df_2 = pd.read_excel("AUG_Evaluation_Jonas.xlsx")
aug_df_3 = pd.read_excel("AUG_Evaluation_Sina.xltx")
aug_df_4 = pd.read_excel("AUG_Evaluation_MEIRAT.xlsx")
#merge the four dataframes by averaging the scores for each user and for each criteria
#Index(['Occupation_Title', 'Scenario_Index', 'AGI_Specificity', 'Connection', 'Usefulness', 'Plausibility', 'Actionability', 'Detail', 'Complexity', 'Novelty'], dtype='object')
merged_df = pd.merge(aug_df_1, aug_df_2, on=['Occupation_Title', 'Scenario_Index'], suffixes=('', '_2'))
merged_df = pd.merge(merged_df, aug_df_3, on=['Occupation_Title', 'Scenario_Index'], suffixes=('', '_3'))
merged_df = pd.merge(merged_df, aug_df_4, on=['Occupation_Title', 'Scenario_Index'], suffixes=('', '_4'))
#merged_df.to_excel("Merged_AUG_Evaluation.xlsx", index=False)

#calulate standard deviation for each criteria from the merged dataframe and plot them for 
#average the scores for each criteria
#AGI_Specificity is YES or NO, so we will not average it, but we will keep the majority vote    
for criteria in ['AGI_Specificity', 'Connection', 'Usefulness', 'Plausibility', 'Actionability', 'Detail', 'Complexity', 'Novelty']:
    if criteria == 'AGI_Specificity':
        #use some function to get the majority vote for AGI_Specificity
        merged_df[criteria] = merged_df[[criteria, criteria+'_2', criteria+'_3', criteria+'_4']].mode(axis=1)[0]
    else:
        merged_df[criteria + '_std'] = merged_df[[criteria, criteria+'_2', criteria+'_3', criteria+'_4']].std(axis=1)
        merged_df[criteria] = merged_df[[criteria, criteria+'_2', criteria+'_3', criteria+'_4']].mean(axis=1)
#keep only the relevant columns
std_df = merged_df[[col for col in merged_df.columns if col.endswith('_std')]]
std_df.columns = [col.replace('_std', '') for col in std_df.columns]
std_df.to_excel("Merged_AUG_Evaluation_Std.xlsx", index=False)
merged_df = merged_df[['Occupation_Title', 'Scenario_Index', 'AGI_Specificity', 'Connection', 'Usefulness', 'Plausibility', 'Actionability', 'Detail', 'Complexity', 'Novelty']]
#save the merged dataframe to an excel file
print(merged_df)
merged_df.to_excel("Merged_AUG_Evaluation.xlsx", index=False)



