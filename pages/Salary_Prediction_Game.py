import dash
dash.register_page(__name__, path="/")

from dash import Dash, dcc, html, Input, Output, callback, State
import plotly.express as px
import joblib
import numpy as np
import pandas as pd



#Import constants
from .constants import club_mapping,position_mapping,league_mapping,nation_mapping

# Load the model
loaded_model = joblib.load('/Users/victorovejero/Desktop/ICAI/GRADO/QUINTO/App_Viz/Proyecto_Final/App/Football_Salary_Predictions/models/wage_prediction_model.joblib')

# Mapping of Clubs to Leagues to filter dropdown options
df = pd.read_csv("/Users/victorovejero/Desktop/ICAI/GRADO/QUINTO/App_Viz/Proyecto_Final/App/Football_Salary_Predictions/data/df_club.csv", usecols = ['Club','League'])
club_league_map = pd.Series(df.League.values,index=df.Club).to_dict()

input = {"Age":20,
        "Total Games Played":100,
        "National Appearences":10,
        "Nationality":"ESP",
        "Current League":"La Liga",
        "Club":"R. Madrid",
        "Position":"Forward"}


layout = html.Div(
    [
        # html.H2("Let's try to Guess a Player's Salary..."),
        # html.P("But first, let me ask you a few questions about him!",style={"margin-bottom":"2rem"}),
        # html.Label("Age: ",style={"margin":"0.5rem"}),
        # dcc.Input(id="Age",type='number',value=input["Age"]),
        # html.P(""),
        # html.Label("Total Games Played: ",style={"margin":"0.5rem"}),
        # dcc.Input(id="Total-Games-Played",type='number',value=input["Total Games Played"]),
        # html.P(""),
        # html.Label("National Appearences: ",style={"margin":"0.5rem"}),
        # dcc.Input(id="National-Appearences",type='number',value=input["National Appearences"]),
        # html.P(""),
        # html.Label("Nationality: ",style={"margin":"0.5rem"}),
        # dcc.Dropdown(
        #     id="Nationality",
        #     options=list(nation_mapping.keys()),
        #     value=input["Nationality"],
        #     clearable=False,
        #     style={"width": "80%"}
        # ),
        # html.P(""),
        # html.Label("Current League: ",style={"margin":"0.5rem"}),
        # dcc.Dropdown(
        #     id="Current-League",
        #     options=list(league_mapping.keys()),
        #     value=input["Current League"],
        #     clearable=False,
        #     style={"width": "80%"}
        # ),
        # html.P(""),
        # html.Label("Current Club: ",style={"margin":"0.5rem"}),
        # dcc.Dropdown(
        #     id="Club",
        #     options=list(club_mapping.keys()),
        #     value=input["Club"],
        #     clearable=False,
        #     style={"width": "80%"}
        # ),
        # html.P(""),
        # html.Label("Position: ",style={"margin":"0.5rem"}),
        # dcc.Dropdown(
        #     id="Position",
        #     options=list(position_mapping.keys()),
        #     value=input["Position"],
        #     clearable=False,
        #     style={"width": "80%"}
        # ),
        # html.P(""),
        # html.Button('Make Prediction', id='Prediction-Button', n_clicks=0), 
        # html.Div(id="output-prediction",children="Enter the values and press the button")

        html.H2("Let's try to Guess a Player's Salary...", className='text-center'),
        html.P("But first, let me ask you a few questions about him!", className='text-center label-input'),

        html.Link(rel='stylesheet', href='/Users/victorovejero/Desktop/ICAI/GRADO/QUINTO/App_Viz/Proyecto_Final/App/Football_Salary_Predictions/assets/styles.css'),

        html.Div(
            [
                html.Label("Age: "),
                dcc.Input(id="Age", type='number', value=input["Age"], className='form-control label-input'),
                html.Label("Total Games Played: "),
                dcc.Input(id="Total-Games-Played", type='number', value=input["Total Games Played"], className='form-control label-input'),
                html.Label("National Appearences: "),
                dcc.Input(id="National-Appearences", type='number', value=input["National Appearences"], className='form-control label-input'),
                html.Label("Nationality: "),
                dcc.Dropdown(
                    id="Nationality",
                    options=list(nation_mapping.keys()),
                    value=input["Nationality"],
                    clearable=False,
                    className='form-control'
                ),
                html.Label("Current League: "),
                dcc.Dropdown(
                    id="Current-League",
                    options=list(league_mapping.keys()),
                    value=input["Current League"],
                    clearable=False,
                    className='form-control'
                ),
                html.Label("Club: "),
                dcc.Dropdown(
                    id="Club",
                    options=list(club_mapping.keys()),
                    value=input["Club"],
                    clearable=False,
                    className='form-control'
                ),
                html.Label("Position: "),
                dcc.Dropdown(
                    id="Position",
                    options=list(position_mapping.keys()),
                    value=input["Position"],
                    clearable=False,
                    className='form-control'
                ),
            ],
            className='container'
        ),

        html.Div(
            [
                html.Button('Make Prediction', id='Prediction-Button', n_clicks=0, className='btn btn-primary'),
            ],
            className='button-container'
        ),

        html.Div(id="output-prediction", children="Enter the values and press the button", className='output-text'),
    
    ]
)

# Define a callback to update the prediction
@callback(
    Output('output-prediction', 'children'),
    # [Input('Age', 'value'),
     State('Total-Games-Played','value'),
     State('National-Appearences', 'value'),
     State('Nationality','value'),
     State('Current-League', 'value'),
     State('Club','value'),
     State('Position', 'value'),
     State('Age', 'value'),
     [Input('Prediction-Button','n_clicks')],
     prevent_initial_call=True
)
def update_prediction(games_played,nat_app,nationality,current_league,club,position,value_age,n_clicks):
    # Use the loaded model to make predictions
    # games_played = 
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    ##### Converting categorical data to numerical data #####
    nationality = nation_mapping[nationality]
    current_league = league_mapping[current_league]
    club = club_mapping[club]
    position = position_mapping[position]
    ##############################

    if 'Prediction-Button' in changed_id:

        prediction = loaded_model.predict([[value_age,games_played,nat_app,nationality,current_league,club,position]])
        # prediction_format = f"{prediction:,}"
        # return html.P(f"The predicted salary is: {prediction_format}")
    # Convert the NumPy array to a Python scalar
        prediction_scalar = prediction.item()

        # Format the prediction with commas for thousands
        formatted_prediction = f"{prediction_scalar:,}"

        # Return a Paragraph component with the formatted prediction
        return html.P(f"The predicted salary is: {formatted_prediction}")
 

    

@callback(
    Output("Club", "options"),
    Input("Current-League", "value"),
    
)
def load_options(search_value):
    return [k for k, v in club_league_map.items() if v == search_value]
    

