from pathlib import Path
import pandas as pd

from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets=external_stylesheets)

styles = {"pre": {"border": "thin lightgrey solid", "overflowX": "scroll"}}

src_file = Path.cwd() / "data" / "raw" / "EPA_fuel_economy_summary.csv"
df = pd.read_csv(src_file)

# Define the input parameters
min_year = df["year"].min()
max_year = df["year"].max()
all_years = df["year"].unique()
transmission_types = df["transmission"].unique()

data_table_cols = [
    "make",
    "model",
    "year",
    "transmission",
    "drive",
    "class_summary",
    "cylinders",
    "displ",
    "fuelCost08",
]

# Need to keep track of button clicks to see if there is a change
total_clicks = 0

app.layout = html.Div(
    [
        html.H1("Fuel Cost Analysis"),
        html.Div([
            html.P("Talk Python Training Example"),
            dcc.Graph(id="histogram-with-slider",
                      config={"displayModeBar": False}),
            dcc.Graph(id="scatter-plot"),
            html.Label("Year Range"),
            dcc.RangeSlider(
                id="year-slider",
                min=min_year,
                max=max_year,
                value=(min_year, max_year),
                marks={str(year): str(year)
                       for year in all_years},
            ),
            html.Label("Transmission type"),
            dcc.Checklist(
                id="transmission-list",
                options=[{
                    "label": i,
                    "value": i
                } for i in transmission_types],
                value=transmission_types,
                labelStyle={"display": "inline-block"},
            ),
            html.Hr(),
            html.Button("Reset selections", id="reset", n_clicks=0),
            html.H3(id="selected_count"),
            dash_table.DataTable(
                id="data-table",
                data=[],
                page_size=10,
                columns=[{
                    "name": i,
                    "id": i
                } for i in data_table_cols],
            ),
        ]),
    ],
    style={"margin-bottom": "150px"},
)


@app.callback(
    Output("histogram-with-slider", "figure"),
    Output("scatter-plot", "figure"),
    Output("data-table", "data"),
    Output("selected_count", "children"),
    Input("year-slider", "value"),
    Input("transmission-list", "value"),
    Input("scatter-plot", "selectedData"),
    Input("reset", "n_clicks"),
)
def update_figure(year_range, transmission_list, selectedData, n_clicks):
    # Global variables may cause unexepcted behavior in multi-user setup
    global total_clicks
    filtered_df = df[df["year"].between(year_range[0], year_range[1])
                     & df["transmission"].isin(transmission_list)]
    
    fig_hist = px.histogram(
        filtered_df,
        x="fuelCost08",
        color="class_summary",
        labels={"fuelCost08": "Annual Fuel Cost"},
        nbins=40,
    )
    
    fig_scatter = px.scatter(
        filtered_df,
        x="displ",
        y="fuelCost08",
        hover_data=[filtered_df.index, "make", "model", "year"],
    )

    fig_scatter.update_layout(clickmode="event", uirevision=True)
    fig_scatter.update_traces(selected_marker_color="red")

    if n_clicks > total_clicks:
        # From here - https://community.plotly.com/t/applying-only-newest-selectedpoints-in-multiple-graphs-or-clearing-selection/31881
        fig_scatter.update_traces(selected_marker_color=None)
        total_clicks = n_clicks
        selectedData = None
    
    if selectedData:
        points = selectedData["points"]
        index_list = [
            points[x]["customdata"][0] for x in range(0, len(points))
        ]
        filtered_df = df[df.index.isin(index_list)]
        num_points_label = f"Showing {len(points)} selected points:"
    else:
        num_points_label = "No points selected - showing top 10 only"
        filtered_df = filtered_df.head(10)

    return fig_hist, fig_scatter, filtered_df.to_dict(
        "records"), num_points_label


if __name__ == "__main__":
    app.run_server(debug=True)  
