import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import numpy as np # pip install numpy
import plotly.io as pio
import pandas as pd
import plotly.graph_objects as go
import dash_mantine_components as dmc



dash.register_page(__name__,suppress_callback_exceptions=True)


df_club = pd.read_csv("/Users/victorovejero/Desktop/ICAI/GRADO/QUINTO/App_Viz/Proyecto_Final/App/Football_Salary_Predictions/data/df_club.csv")
df_league = pd.read_csv("/Users/victorovejero/Desktop/ICAI/GRADO/QUINTO/App_Viz/Proyecto_Final/App/Football_Salary_Predictions/data/df_wage_by_league.csv")

leagues = df_league["League"].unique()
min_wage = 0

layout = html.Div(
    [
        dcc.Graph(id="bar-graph"),
        html.P("League:"),
        dmc.MultiSelect(id="bar-league", 
                        value=leagues, 
                        data = leagues,
                        clearable=False,
                        style={"width": "80%"}),
        
               
        html.Div(id='output',style={"margin-top": "1.5rem", "margin-bottom":"1.5rem"}),
        dcc.Slider(id="bar-wage", min=0, max=15000000, value=0, marks={0: "0",1000000:"1000000",5000000:"5000000",10000000:"10000000"}),
        
    ]
)

@callback(
    Output('output', 'children'),
    Input('bar-wage', 'value'))
def update_output(value):
    return 'Mininum Average Wage "{}"'.format(value)

@callback(
    Output("bar-graph", "figure"),
    Input("bar-league", "value"),
    Input("bar-wage", "value"),
)
def display_color(leagues,min_wage):
    


    filtered_df_leagues = df_league[df_league["League"].map(lambda x: np.isin(x, leagues).all())]
    filtered_df_clubs = df_club[df_club["League"].map(lambda x: np.isin(x, leagues).all())]
    filtered_df_clubs = filtered_df_clubs[filtered_df_clubs["Wage"] >= min_wage]
    data = [
        go.Scatter(
            x=filtered_df_clubs["League"],
            y=filtered_df_clubs["Wage"],
            text=filtered_df_clubs["Club"],
            mode='markers',
    #         transforms=[
    #             dict(
    #                 type='groupby',
    #                 groups=df_club.index,
    #                 styles=[
    #                     dict(target=club, value=dict(marker=dict(color='blue'))) for club in df_club.index
    #                 ]
    #             )
    #         ]
        ),
        go.Scatter(
            x=filtered_df_leagues["League"],
            y=filtered_df_leagues["Wage"],
            mode='lines+markers',
            line=dict(color='blue'),
            name='Average Score'
        )
    ]
    
    layout = go.Layout(title="Wage by League and Clubs", showlegend=False)
    fig = go.Figure(data=data, layout = layout)
    return fig