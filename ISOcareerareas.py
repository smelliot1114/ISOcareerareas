import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load Data
top_ai_career_data = pd.read_csv("TopAICareerDataV2.csv")

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("AI Career Areas Comparison", style={"textAlign": "center", "color": "#ffffff", "fontFamily": "Arial, sans-serif"}),

    html.Label("Select State 1:", style={"color": "#ffffff"}),
    dcc.Dropdown(
        id="career_state_1",
        options=[{"label": state, "value": state} for state in top_ai_career_data["state_name"].unique()],
        value="California",
        clearable=False
    ),

    html.Label("Select State 2:", style={"color": "#ffffff"}),
    dcc.Dropdown(
        id="career_state_2",
        options=[{"label": state, "value": state} for state in top_ai_career_data["state_name"].unique()],
        value="Texas",
        clearable=False
    ),

    dcc.Graph(id="career_comparison_chart")
], style={"backgroundColor": "#3a3a3a", "padding": "20px", "fontFamily": "Arial, sans-serif"})


@app.callback(
    dash.Output("career_comparison_chart", "figure"),
    [dash.Input("career_state_1", "value"), dash.Input("career_state_2", "value")]
)
def update_career_chart(state1, state2):
    filtered_data = top_ai_career_data[top_ai_career_data["state_name"].isin([state1, state2])].copy()

    # Convert proportion to percentage and round
    filtered_data["proportion"] = (filtered_data["proportion"] * 100).round(2)

    fig = px.bar(
        filtered_data,
        x="lot_career_area_name",
        y="proportion",
        color="state_name",
        title=f"Top 12 AI Career Areas: {state1} vs {state2}",
        labels={"lot_career_area_name": "Career Area", "proportion": "Percentage of AI Listings (%)"},
        barmode="group"
    )
    return fig

server = app.server

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, host="0.0.0.0", port=port)
