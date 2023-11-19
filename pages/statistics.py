import dash
import pandas as pd
dash.register_page(__name__)

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px



# READ DATA
df = pd.read_csv("/Users/victorovejero/Desktop/ICAI/GRADO/QUINTO/App_Viz/Proyecto_Final/App/Football_Salary_Predictions/data/df_estadistica.csv")
df_num = df
choices = ["League","Age","Position","Club"]




layout = html.Div(
    [
        html.H2("Group players by:"),
        dcc.Dropdown(
            id="dropdown",
            options=choices,
            value=choices[0],
            clearable=False,
            style={"width": "80%"}
        ),
        dcc.Graph(id="correlation-matrix"),
        dcc.Graph(id="correlation-scatter"),
    ]
)

@callback(Output("correlation-scatter", "figure"), Input("dropdown", "value"))
def correlation_scatter(choice):
    
    fig = px.scatter_matrix(df_num.loc[:,["Wage","Apps","Caps",choice]],title="Correlation Scatter")
    return fig

@callback(Output("correlation-matrix", "figure"), Input("dropdown", "value"))
def update_correlation_matrix(choice):
    # Average numeric columns and group by Age
    df_num = df.loc[:,["Wage","Apps","Caps",choice]]

    if("Age" in df_num.columns):
        df_num = df_num.groupby(choice).mean()
        df_num["Age"] = df_num.index

    else:
        df_num = df.loc[:,["Wage","Apps","Caps","Age",choice]].groupby(choice).mean()
        
    corr_matrix = df_num.corr()
    
    fig = px.imshow(corr_matrix,
                labels=dict(color="Correlation"),
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                color_continuous_scale='greens',
                title='Correlation Matrix')    
    return fig


