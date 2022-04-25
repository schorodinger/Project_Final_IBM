# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Create a dash application
app = dash.Dash(__name__)

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Import required libraries


# Read the airline data into pandas dataframe
path = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
spacex_df = pd.read_csv(path)
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

print(spacex_df.columns)


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        # dcc.Dropdown(id='site-dropdown',...)
        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {"label": "All Sites", "value": "ALL"},
                {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
                {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
            ],
            value="ALL",
            placeholder="Select a Launch Site here",
            searchable=True,
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            marks={0: "0", 2500: "2500", 5000: "5000", 7500: "7500", 10000: "10000"},
            value=[max_payload, min_payload],
        ),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


# Function decorator to specify function input and output
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(entered_site):

    filtered_df = spacex_df
    if entered_site == "ALL":
        fig = px.pie(
            filtered_df,
            values="class",
            names="Launch Site",
            title="Total Success Lauches By Site",
        )
        return fig
    else:
        # return the outcomes piechart for a selected site

        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        df_outcomes = (
            filtered_df.groupby(["Launch Site", "class"])
            .size()
            .reset_index(name="class count")
        )
        fig = px.pie(
            df_outcomes,
            values="class count",
            names="class",
            title=f"Total Success Launches for site {entered_site}",
        )
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def get_scatter_chart(entered_site, slider_range):

    low, high = slider_range

    marks = (spacex_df["Payload Mass (kg)"] > low) & (
        spacex_df["Payload Mass (kg)"] < high
    )

    filtered_df = spacex_df[marks]

    if entered_site == "ALL":
        fig = px.scatter(
            filtered_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Correlation between Payload and Success for all Sites",
        )
        return fig
    else:
        # return the outcomes piechart for a selected site

        df_pay = filtered_df[filtered_df["Launch Site"] == entered_site]

        fig = px.scatter(
            df_pay,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title=f"Correlation between Payload and Success for  Site {entered_site}",
        )
        return fig


if __name__ == "__main__":
    app.run_server()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
