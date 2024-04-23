#pip install pandas, plotly, dash, dash_core_components, dash_html_components, dash_bootstrap_components

import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import time
from data import Data
import heapSort as hs
import radixSort as rs


# heap sort (change later)
def heap_sort(arr):
    start_time = time.time()
    hs.heap_sort(arr)
    end_time = time.time()
    return end_time - start_time


# radix sort (change later)
def radix_sort(arr):
    start_time = time.time()
    rs.radix_sort(arr)
    end_time = time.time()
    return end_time - start_time


# sample data (change later)
player_names = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5"]
seasons = [2020, 2021, 2022, 2020, 2021]
pts = [20, 18, 22, 25, 19]
reb = [8, 6, 10, 7, 9]
ast = [5, 7, 4, 6, 3]
net_rating = [10, 8, 12, 9, 11]
oreb_pct = [0.2, 0.15, 0.25, 0.18, 0.22]
dreb_pct = [0.3, 0.25, 0.35, 0.28, 0.32]
usg_pct = [0.25, 0.22, 0.28, 0.3, 0.21]
ts_pct = [0.58, 0.62, 0.56, 0.6, 0.55]
ast_pct = [0.2, 0.25, 0.18, 0.22, 0.15]

# pandas dataframe (change later)
data = pd.DataFrame({
    'Player Name': player_names,
    'Season': seasons,
    'Points': pts,
    'Rebounds': reb,
    'Assists': ast,
    'Net Rating': net_rating,
    'Offensive Rebound %': oreb_pct,
    'Defensive Rebound %': dreb_pct,
    'Usage %': usg_pct,
    'True Shooting %': ts_pct,
    'Assist %': ast_pct
})
data = Data().temp()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Entire page layout
app.layout = dbc.Container([
    # title
    dbc.Row(dbc.Col(html.H1('Player Statistics Radar Plot', className='text-center mb-4'), width=12)),
    dbc.Row([
        dbc.Col([
            # player selection, drop down menu
            html.Label('Select Players:', className='mb-2'),
            dcc.Dropdown(
                id='player-dropdown',
                options=[{'label': player, 'value': player} for player in data['player_name'].unique()],
                multi=True,
                className='mb-3'
            )
        ], width=4),
        dbc.Col([
            # year selection, drop down menu (based on years avaliable within selected players)
            html.Label('Select Seasons:', className='mb-2'),
            dcc.Dropdown(
                id='season-dropdown',
                multi=True,
                className='mb-3'
            )
        ], width=4),
        # column selection, select which statistics to go into the radar plot
        dbc.Col([
            html.Label('Select Statistics:', className='mb-2'),
            dcc.Dropdown(
                id='column-dropdown',
                options=[{'label': col, 'value': col} for col in data.columns[2:]],
                multi=True,
                className='mb-3'
            )
        ], width=4)
    ]),
    # insert radar plot
    dbc.Row(dbc.Col(dcc.Graph(id='radar-plot', config={'displayModeBar': False}), className='mt-4')),
    dbc.Row([
        # insert time variables for sorting algorithms
        dbc.Col(html.Div(id='heap-sort-time', className='text-center'), width=6),
        dbc.Col(html.Div(id='radix-sort-time', className='text-center'), width=6)
    ], className='mt-4')
], fluid=True)


# Update sorting times each time a new plot is ran
@app.callback(
    Output('heap-sort-time', 'children'),
    [Input('player-dropdown', 'value'),
     Input('season-dropdown', 'value'),
     Input('column-dropdown', 'value')]
)
def update_heap_sort_time(selected_players, selected_seasons, selected_columns):
    # make sure columns are selected
    if not selected_players or not selected_seasons or not selected_columns:
        return ""

    # sort only selected columns for now (make sorting more interesting)
    data_to_sort = data[selected_columns].copy()
    for col in data_to_sort.columns:
        data_to_sort[col] = pd.to_numeric(data_to_sort[col], errors='coerce')
    data_to_sort.dropna(inplace=True)
    data_to_sort = data_to_sort.values.tolist()

    heap_sort_time = heap_sort(data_to_sort)

    return f"Heap Sort Time: {heap_sort_time:.9f} seconds"


# Callback to update radix sort time
@app.callback(
    Output('radix-sort-time', 'children'),
    [Input('player-dropdown', 'value'),
     Input('season-dropdown', 'value'),
     Input('column-dropdown', 'value')]
)
def update_radix_sort_time(selected_players, selected_seasons, selected_columns):
    if not selected_players or not selected_seasons or not selected_columns:
        return ""

    # sort only selected columns for now (make sorting more interesting)
    data_to_sort = data[selected_columns].copy()
    for col in data_to_sort.columns:
        data_to_sort[col] = pd.to_numeric(data_to_sort[col], errors='coerce')
    data_to_sort.dropna(inplace=True)
    data_to_sort = data_to_sort.values.tolist()

    radix_sort_time = radix_sort(data_to_sort)

    return f"Radix Sort Time: {radix_sort_time:.9f} seconds"


# update drop down options everytime one is selected
@app.callback(
    Output('season-dropdown', 'options'),
    [Input('player-dropdown', 'value')]
)
def update_season_options(selected_players):
    if not selected_players:
        return []  # Return empty options if no players are selected

    # Get the unique seasons for the selected players
    selected_seasons = data[data['player_name'].isin(selected_players)]['season'].unique()

    return [{'label': str(season), 'value': season} for season in selected_seasons]


# Update the radar plot every time something is selected
@app.callback(
    Output('radar-plot', 'figure'),
    [Input('player-dropdown', 'value'),
     Input('season-dropdown', 'value'),
     Input('column-dropdown', 'value')]
)
def update_radar_plot(selected_players, selected_seasons, selected_columns):
    # Check if any selection is empty
    if not selected_players or not selected_seasons or not selected_columns:
        # Return an empty plot
        return go.Figure()

    # Filter data based on user selections
    filtered_data = data[
        (data['player_name'].isin(selected_players)) &
        (data['season'].isin(selected_seasons))
        ].copy()

    # Create a new plot
    fig = go.Figure()

    # Add traces for each player and season
    for player in filtered_data['player_name'].unique():
        player_data = filtered_data[filtered_data['player_name'] == player]
        for season in player_data['season'].unique():
            season_data = player_data[player_data['season'] == season]
            fig.add_trace(go.Scatterpolar(
                r=season_data[selected_columns].values.tolist()[0],
                theta=selected_columns,
                fill='toself',
                name=f"{player} ({season})"
            ))

    # Update plot layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(filtered_data[selected_columns].max()) * 1.1]
            )
        )
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
