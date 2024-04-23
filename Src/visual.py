import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from data import Data
import radixSort as rs
import heapSort as hs
from scipy.stats import percentileofscore

# Initialize the Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1('Dynamic Statistic Ranking and Visualization', className='text-center mb-4'), width=12)),
    dbc.Row([
        dbc.Col([
            html.Label('Select Season:', className='mb-2'),
            dcc.Dropdown(
                id='season-dropdown',
                className='mb-3'
            ),
            html.Label('Select Sorting Method:', className='mb-2'),
            dcc.Dropdown(
                id='sorting-method-dropdown',
                options=[
                    {'label': 'Radix Sort', 'value': 'radix'},
                    {'label': 'Heap Sort', 'value': 'heap'}
                ],
                value='radix',
                className='mb-3'
            ),
            html.Label('Select Players:', className='mb-2'),
            dcc.Dropdown(
                id='player-dropdown',
                multi=True,
                className='mb-3'
            ),
            html.Label('Select Statistics:', className='mb-2'),
            dcc.Dropdown(
                id='stat-dropdown',
                multi=True,
                className='mb-3'
            )
        ], width=4),
        dbc.Col([
            dcc.Graph(id='radar-plot')
        ], width=8)
    ])
])

@app.callback(
    [Output('season-dropdown', 'options'),
     Output('season-dropdown', 'value')],
    Input('sorting-method-dropdown', 'value')  # Trigger update on sorting method change, assuming data refresh might be needed.
)
def set_season_options(_):
    data = Data().temp()  # Assuming Data().temp() returns DataFrame
    seasons = [{'label': str(season), 'value': season} for season in data['season'].unique()]
    return seasons, seasons[0]['value'] if seasons else None

@app.callback(
    [Output('player-dropdown', 'options'),
     Output('stat-dropdown', 'options')],
    [Input('season-dropdown', 'value')],
    [State('sorting-method-dropdown', 'value')]
)
def update_dropdowns(selected_season, sorting_method):
    data = Data().temp()  # Load fresh data
    data = data[data['season'] == selected_season]
    player_options = [{'label': player, 'value': player} for player in data['player_name'].unique()]
    stat_options = [{'label': col, 'value': col} for col in data.columns if col not in ['player_name', 'season'] and data[col].dtype in [float, int]]
    return player_options, stat_options

@app.callback(
    Output('radar-plot', 'figure'),
    [Input('player-dropdown', 'value'),
     Input('stat-dropdown', 'value'),
     Input('sorting-method-dropdown', 'value'),
     Input('season-dropdown', 'value')]
)
def update_radar_plot(selected_players, selected_stats, sorting_method, selected_season):
    if not selected_players or not selected_stats:
        return go.Figure()

    # Get data for the specified season
    season_data = Data().get_season_data(selected_season)

    # Calculate the percentile for each statistic across all players for the season
    for stat in selected_stats:
        season_data[stat + ' Percentile'] = season_data[stat].rank(pct=True) * 100

    # Filter the data to only include the selected players
    filtered_data = season_data[season_data['player_name'].isin(selected_players)]

    # Construct the radar plot
    fig = go.Figure()
    for player in selected_players:
        player_data = filtered_data[filtered_data['player_name'] == player]
        if not player_data.empty:
            fig.add_trace(go.Scatterpolar(
                r=[player_data[stat + ' Percentile'].iloc[0] for stat in selected_stats],
                theta=[stat + ' Percentile' for stat in selected_stats],
                fill='toself',
                name=player
            ))

    # Update the layout to set the range of the radial axis from 0 to 100
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]  # Set the range from 0 to 100%
            )
        ),
        # Additional layout parameters can be set here
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

# References:
    
# dash-bootstrap-components documentation
# https://dash-bootstrap-components.opensource.faculty.ai/docs/quickstart/
    
# Scipy Documentation
# https://docs.scipy.org/doc/scipy/tutorial/stats.html
    
# Plotly documentation
# https://dash.plotly.com/basic-callbacks
