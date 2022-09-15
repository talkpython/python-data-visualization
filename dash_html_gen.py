from dash import Dash, html, dcc
import plotly.express as px

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1("Simple HTML Only Site"),
        html.H2("TalkPython Training"),
        html.Div(
            [
                html.P("Annual Fuel Cost Plot",
                       className="my-p-class",
                       id="my-p-id")
            ],
            style={
                "color": "green",
                "fontSize": 18
            },
        ),
        dcc.Markdown("""
                #### Dash Supports Markdown

                You can write simple text and format it with markup like
                **bold text** and *italics*, [links](http://commonmark.org/help).
                You can also use:
                * lists
                * inline `code` snippets
                * and more
            """),
    ],
    style={
        "margin-left": "25px",
        "width": "55%",
        "backgroundColor": "lightgray"
    },
)


if __name__ == "__main__":
    app.run_server(debug=True)


