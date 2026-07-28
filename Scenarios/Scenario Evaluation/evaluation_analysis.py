import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("Merged_AUG_Evaluation.xlsx")
#only keep rows where AGI_Specificity is YES
df = df[df['AGI_Specificity'] == 'YES']
criteria = ['Connection', 'Usefulness', 'Plausibility', 'Actionability', 'Complexity' ,'Detail', 'Novelty']
df['Complexity'] = df['Complexity'].apply(lambda x: 5-x) #invert the complexity score so that higher is better
#sum up the scores for each row but complexity and plot them in a bar chart, ordered by total score
#for ylabelling the y axis, use the occupation title and the scenario index
#only keep top15 rows with highest total score
df = df.head(15)
df['Total_Score'] = df[criteria].sum(axis=1)
df = df.sort_values('Total_Score', ascending=False)
plt.figure(figsize=(10, 20))
plt.barh(df['Occupation_Title'] + " - " + df['Scenario_Index'].astype
(str), df['Total_Score'])
plt.xlabel('Total Score')
plt.title('AUG Total Score for Each Occupation and Scenario')
plt.gca().invert_yaxis()

#plt.savefig("AUG_Total_Score_Bar_Chart.png")
plt.show()
