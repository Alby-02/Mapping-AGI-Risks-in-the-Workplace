import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("Theme based scenarios.csv")
#just keep the theme label and occpation name
df = df[["theme_label", "occupation"]] 

labels = ["Other", "AGI-AGI Collaboration", "Human-AGI interactions", "Autonomy"]
#order size by theme label, and if the theme label is not in the labels list, put it in the "Other" category
df["theme_label"] = df["theme_label"].apply(lambda x: x if x in labels else "Other")
sizes = df["theme_label"].value_counts().reindex(["Other", "AGI-AGI Collaboration", "Human-AGI interactions", "Autonomy"]).fillna(0).tolist()

color1 = ["#929699"]
color2 = ["#221f21"]


color1 = "#221f2138"
color2 = "#221f21"
colors = ["rgba(34, 31, 33, 0.5)", color2, color2, color2]

fig = go.Figure(go.Bar(
    x=sizes,
    y=labels,
    orientation="h",
    marker=dict(color=colors),
    text=sizes,
    textposition="outside",
    cliponaxis=False,
    width=0.25,
    hovertemplate="%{y}: %{x}<extra></extra>"
))

fig.update_layout(
    title={
        "text": ""
    },
    xaxis_title="",
    yaxis_title="",
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    width=700,
    height=400,
    margin=dict(l=300, r=40, t=90, b=50),
    font=dict(size=14, color="black")
)

fig.update_xaxes(
     range=[0, max(sizes) + 3],
    automargin=True,
    gridcolor="rgba(0,0,0,0.08)",
    zeroline=True,
    showline=True,
    linecolor="black",
    linewidth=1.2
    
)

fig.update_yaxes(
    showticklabels=False,
    zeroline=True,
    showline=True,
    linecolor="black",
    linewidth=1.2,
    ticks="outside",
    ticklen=3,
    tickwidth=1.2,
    tickcolor="black"
)

for label in labels:
    fig.add_annotation(
        x=-0.53,  # Adjust the x position as needed
        y=label,
        xref="paper",
        yref="y",
        xanchor="left",
        yanchor="middle",
        text=label,
        showarrow=False,
        font=dict(size=14, color="black"),
        align="left"
    )

fig.show()