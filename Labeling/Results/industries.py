import pandas as pd

Sectors = {
    "11": "Management Occupations",
    "13": "Business and Financial Operations Occupations",
    "15": "Computer and Mathematical Occupations",
    "17": "Architecture and Engineering Occupations",
    "19": "Life, Physical, and Social Science Occupations",
    "21": "Community and Social Service Occupations",
    "23": "Legal Occupations",
    "25": "Educational Instruction and Library Occupations",
    "27": "Arts, Design, Entertainment, Sports, and Media Occupations",
    "29": "Healthcare Practitioners and Technical Occupations",
    "31": "Healthcare Support Occupations",
    "33": "Protective Service Occupations",
    "35": "Food Preparation and Serving Related Occupations",
    "37": "Building and Grounds Cleaning and Maintenance Occupations",
    "39": "Personal Care and Service Occupations",
    "41": "Sales and Related Occupations",
    "43": "Office and Administrative Support Occupations",
    "45": "Farming, Fishing, and Forestry Occupations",
    "47": "Construction and Extraction Occupations",
    "49": "Installation, Maintenance, and Repair Occupations",
    "51": "Production Occupations",
    "53": "Transportation and Material Moving Occupations"
}
df = pd.read_csv("Occupations_With_Automation_Augmentation_Scores.csv")

df["Sector"] = df["O*NET-SOC Code"].str[:2].map(Sectors)
df.to_csv("Occupations_With_Automation_Augmentation_Scores_With_Sectors.csv", index=False)

#group by sector
grouped = df.groupby("Sector").agg({
    "Automation_Score": "mean",
    "Augmentation Score": "mean"
}).reset_index()
#grouped.to_csv("Sectors_With_Automation_Augmentation_Scores.csv", index=False)
#remove "occupations" from sector names
grouped["Sector"] = grouped["Sector"].str.replace(" Occupations", "")

#plot the results as a horizontal bar chart, each sector on the y-axis and the average automation and augmentation scores on the x-axis, with two bars for each sector, one for automation and one for augmentation
import plotly.express as px

order = grouped.sort_values("Automation_Score", ascending=True)["Sector"].tolist()
order2 = grouped.sort_values("Augmentation Score", ascending=True)["Sector"].tolist()

fig = px.bar(
    grouped,
    y="Sector",
    x=["Automation_Score"],
    orientation="h",
    barmode="group"
)
fig2 = px.bar(
    grouped,
    y="Sector",
    x=["Augmentation Score"],
    orientation="h",
    barmode="group"
)
fig.update_yaxes(categoryorder="array", categoryarray=order)
fig2.update_yaxes(categoryorder="array", categoryarray=order2)
fig.update_traces(marker_color="#1f77b4")
fig2.update_traces(marker_color="#ff7f0e")


fig.show()
fig2.show()