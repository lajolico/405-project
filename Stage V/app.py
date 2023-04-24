from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from datetime import datetime as dt


LOG_FLAG = False
START_DATE = dt.now()
END_DATE = dt.now()


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
    html.H1(children='COVID-19 Dashboard', style={'textAlign':'center'}),
    html.Label('Start Date'),
    dcc.DatePickerRange(covid_cases_df.index[0], covid_cases_df.index[len(covid_cases_df.index)-1], id='date-picker-range', min_date_allowed=covid_cases_df.index[0], max_date_allowed=covid_cases_df.index[len(covid_cases_df.index)-1]),
    dcc.Dropdown(options=['Linear', 'Log'], id='mode-dropdown', value='Linear'),
    dcc.Graph(id='graph-cases-content'),
    dcc.Graph(id='graph-deaths-content')
])


@callback(
    Output('graph-cases-content', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('mode-dropdown', 'value')
)
def update_cases_graph(start_date, end_date, value):
    START_DATE = start_date
    END_DATE = end_date
    if value == 'Log':
        LOG_FLAG = True
    else:
        LOG_FLAG = False
    return px.line(covid_cases_df[START_DATE:END_DATE], title='Confirmed COVID-19 Cases in the US', log_y=LOG_FLAG).update_layout(xaxis_title='Date', yaxis_title='Number of Confirmed Cases')

@callback(
    Output('graph-deaths-content', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('mode-dropdown', 'value')
)
def update_deaths_graph(start_date, end_date, value):
    START_DATE = start_date
    END_DATE = end_date
    if value == 'Log':
        LOG_FLAG = True
    else:
        LOG_FLAG = False
    return px.line(covid_deaths_df[START_DATE:END_DATE], title='Confirmed COVID-19 Deaths in the US', log_y=LOG_FLAG).update_layout(xaxis_title='Date', yaxis_title='Number of Confirmed Deaths')

if __name__ == '__main__':
    app.run_server(debug=True)