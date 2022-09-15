from pathlib import Path
import pandas as pd

from dash import Dash, html, dcc, Input, Output
import plotly.express as px

app = Dash(__name__)

src_file = Path.cwd() / "data" / "raw" / "EPA_fuel_economy_summary.csv"
df = pd.read_csv(src_file)
fuel_types = df["fuel_type_summary"].unique()

app.layout = html.Div(
    children=[
        html.H1("Simple Histogram"),
        html.Div("Annual Fuel Cost Plot."),
        dcc.Graph(id="histogram"),
        dcc.Dropdown(
            id="fuel_id",
            options=[{"label": i, "value": i} for i in fuel_types],
            value=[i for i in fuel_types],
            multi=True,
        ),
    ]
)

@app.callback(Output("histogram", "figure"), Input("fuel_id", "value"))
def update_output(fuel_list):
    filtered_df = df[df["fuel_type_summary"].isin(fuel_list)]
    fig = px.histogram(
        filtered_df,
        x="fuelCost08",
        color="class_summary",
        labels={"fuelCost08": "Annual Fuel Cost"},
        nbins=40,
        title="Fuel Cost Distribution",
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)


