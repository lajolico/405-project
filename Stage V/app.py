from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from datetime import datetime as dt


# United States of America Python Dictionary to translate States,
# Districts & Territories to Two-Letter codes and vice versa.
#
# Canonical URL: https://gist.github.com/rogerallen/1583593
#
# Dedicated to the public domain.  To the extent possible under law,
# Roger Allen has waived all copyright and related or neighboring
# rights to this code.  Data originally from Wikipedia at the url:
# https://en.wikipedia.org/wiki/ISO_3166-2:US
#
# Automatically Generated 2021-09-11 18:04:36 via Jupyter Notebook from
# https://gist.github.com/rogerallen/d75440e8e5ea4762374dfd5c1ddf84e0 

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

us_abbrev_to_state = {v: k for k, v in us_state_to_abbrev.items()}


LOG_FLAG = False
START_DATE = dt.now()
END_DATE = dt.now()

def get_us_confirmed_cases():
    df = pd.read_csv('../Stage IV/team_work/data/covid_confirmed_usafacts.csv')
    df = df.drop(['countyFIPS', 'County Name', 'StateFIPS'], axis=1)
    df = df.groupby('State').sum(numeric_only=True)
    df.columns = pd.to_datetime(df.columns)
    df = df.transpose()
    return df

def get_us_confirmed_deaths():
    df = pd.read_csv('../Stage IV/team_work/data/covid_deaths_usafacts.csv')
    df = df.drop(['countyFIPS', 'County Name', 'StateFIPS'], axis=1)
    df = df.groupby('State').sum(numeric_only=True)
    df.columns = pd.to_datetime(df.columns)
    df = df.transpose()
    return df


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

covid_states_cases_df = get_us_confirmed_cases()
covid_states_deaths_df = get_us_confirmed_deaths()

covid_cases_df = get_us_confirmed_cases_time_series()
covid_deaths_df = get_us_confirmed_deaths_time_series()

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='COVID-19 Dashboard', style={'textAlign':'center'}),
    html.Label('Date Range'),
    dcc.DatePickerRange(covid_cases_df.index[0], covid_cases_df.index[len(covid_cases_df.index)-1], id='date-picker-range', min_date_allowed=covid_cases_df.index[0], max_date_allowed=covid_cases_df.index[len(covid_cases_df.index)-1]),
    html.Br(),
    html.Label('Mode'),
    dcc.Dropdown(options=['Linear', 'Log'], id='mode-dropdown', value='Linear'),
    html.Label('State'),
    dcc.Dropdown(options=['All States'] + list(us_state_to_abbrev.keys()), value='All States', id='us-state-selector', multi=True),
    dcc.Graph(id='graph-cases-content'),
    dcc.Graph(id='graph-deaths-content')
])


@callback(
    Output('graph-cases-content', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('mode-dropdown', 'value'),
    Input('us-state-selector', 'value')
)
def update_cases_graph(start_date, end_date, value, states):
    START_DATE = start_date
    END_DATE = end_date
    if value == 'Log':
        LOG_FLAG = True
    else:
        LOG_FLAG = False
    if len(states) == 0 or 'All States' in states:
        selected_df = covid_states_cases_df.sum(axis=1)
        graph_title = 'Confirmed COVID-19 Cases in the US'
    else:
        selected_df = covid_states_cases_df[[us_state_to_abbrev[state] for state in states]].sum(axis=1)
        if len(states) > 1:
            graph_title = f'Confirmed COVID-19 Cases in multiple states'
        else:
            graph_title = f'Confirmed COVID-19 Casess in {states[0]}'
    figure = px.line(selected_df[START_DATE:END_DATE], title=graph_title, log_y=LOG_FLAG).update_layout(xaxis_title='Date', yaxis_title='Number of Confirmed Cases')
    figure.data[0].name = 'Confirmed Cases'
    return figure

@callback(
    Output('graph-deaths-content', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('mode-dropdown', 'value'),
    Input('us-state-selector', 'value')
)
def update_deaths_graph(start_date, end_date, value, states):
    START_DATE = start_date
    END_DATE = end_date
    if value == 'Log':
        LOG_FLAG = True
    else:
        LOG_FLAG = False
    if len(states) == 0 or 'All States' in states:
        selected_df = covid_states_deaths_df.sum(axis=1)
        graph_title = 'Confirmed COVID-19 Deaths in the US'
    else:
        selected_df = covid_states_deaths_df[[us_state_to_abbrev[state] for state in states]].sum(axis=1)
        if len(states) > 1:
            graph_title = f'Confirmed COVID-19 Deaths in multiple states'
        else:
            graph_title = f'Confirmed COVID-19 Deaths in {states[0]}'
    figure = px.line(selected_df[START_DATE:END_DATE], title=graph_title, log_y=LOG_FLAG).update_layout(xaxis_title='Date', yaxis_title='Number of Confirmed Deaths')
    figure.data[0].name= 'Confirmed Deaths'
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)