import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data


# Read in global data
cars = data.cars()

# Setup app and layout/frontend
app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server

app.layout = dbc.Container(
    [
    dbc.Jumbotron(
        [
            html.H1("Jumbotron", className="display-3"),
            html.P(
                "Use a jumbotron to call attention to "
                "featured content or information.",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P(
                "Jumbotrons use utility classes for typography and "
                "spacing to suit the larger container."
            ),
            html.P(dbc.Button("Learn more", color="primary"), className="lead"),
            html.P(dbc.Button("Learn more", color="danger"), className="lead2"),
        ]),
        dbc.Button(
            "Click to toggle popover", id="popover-target", color="danger"
        ),
        # dbc.Popover(
        #     [
        #         dbc.PopoverHeader("Popover header"),
        #         dbc.PopoverBody("And here's some amazing content. Cool!"),
        #     ],
        #     id="popover",
        #     is_open=False,
        #     target="popover-target",
        # ),
        dbc.Alert("This is a dashboard currently in progress", color="danger"),

        dbc.Tabs([
            dbc.Tab([
                html.H1('A heading for Tab 1'),
                html.Iframe(
                    id="scatter",
                    style={"border-width": "0", "width": "100%", "height": "400px"},
                ),
                html.Div(id='mean-x-div'),
                html.Br(),
                html.Label([
                    'Click here to choose the X Column',
                    dcc.Dropdown(
                    id="xcol-widget",
                    value="Horsepower",  # REQUIRED to show the plot on the first page load
                    options=[{"label": col, "value": col} for col in cars.columns],
                )
                ]),
                html.Br(),
                html.Div(id='mean-y-div'),
                dcc.Dropdown(
                    id="ycol-widget",
                    value="Displacement",
                    options=[{"label": col, "value": col} for col in cars.columns],
                ),
            ],label='Analysis 1'),
            dbc.Tab('This will be analysis 2', label='Analysis 2'),
        ]),
    ],
)

# Set up callbacks/backend
@app.callback(Output("scatter", "srcDoc"), 
              Output("mean-x-div","children"),
              Output("mean-y-div","children"),
              Input("xcol-widget", "value"),
              Input("ycol-widget", "value"))
def plot_altair(xcol,ycol):
    chart = (
        alt.Chart(cars)
        .mark_point()
        .encode(x=xcol, 
                y=ycol, tooltip="Horsepower")
        .interactive()
    )
    return chart.to_html(), f'The mean of {xcol} is {cars[xcol].mean().round(1)}', f'The mean of {ycol} is {cars[ycol].mean().round(1)}'

# @app.callback(
#     Output("popover", "is_open"),
#     [Input("popover-target", "n_clicks")],
#     [State("popover", "is_open")],
# )
# def toggle_popover(n, is_open):
#     if n:
#         return not is_open
#     return is_open

if __name__ == "__main__":
    app.run_server(debug=True)
