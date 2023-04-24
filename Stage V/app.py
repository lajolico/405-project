from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from datetime import datetime as dt


def get_us_confirmed_cases_time_series():
    df = pd.read_csv('../Stage IV/team_work/data/covid_confirmed_usafacts.csv')
    df = df.drop(['countyFIPS', 'County Name', 'State', 'StateFIPS'], axis=1)
    df = df.transpose()
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d")
    df = df.sum(axis=1)
    df.name = 'cases'
    return df

def get_us_confirmed_deaths_time_series():
    df = pd.read_csv('../Stage IV/team_work/data/covid_deaths_usafacts.csv')
    df = df.drop(['countyFIPS', 'County Name', 'State', 'StateFIPS'], axis=1)
    df = df.transpose()
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d")
    df = df.sum(axis=1)
    df.name = 'deaths'
    return df

covid_cases_df = get_us_confirmed_cases_time_series()
covid_deaths_df = get_us_confirmed_deaths_time_series()

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='COVID-19 Data Analysis', style={'textAlign':'center'}),
    html.Label('Start Date'),
    dcc.DatePickerRange(covid_cases_df.index[0], covid_cases_df.index[len(covid_cases_df.index)-1], id='date-picker-range', min_date_allowed=covid_cases_df.index[0], max_date_allowed=covid_cases_df.index[len(covid_cases_df.index)-1]),
    dcc.Graph(id='graph-cases-content'),
    dcc.Graph(id='graph-deaths-content')
])

@callback(
    Output('graph-cases-content', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_cases_graph(start_date, end_date):
    dff = covid_cases_df[start_date:end_date]
    return px.line(dff, title='Confirmed COVID-19 Cases in the US').update_layout(xaxis_title='Date', yaxis_title='Number of Confirmed Cases')

@callback(
    Output('graph-deaths-content', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_deaths_graph(start_date, end_date):
    dff = covid_deaths_df[start_date:end_date]
    return px.line(dff, title='Confirmed COVID-19 Deaths in the US').update_layout(xaxis_title='Date', yaxis_title='Number of Confirmed Deaths')

if __name__ == '__main__':
    app.run_server(debug=True)