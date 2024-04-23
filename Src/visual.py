import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from data import Data
import radixSort as rs
import heapSort as hs

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
    stat_options = [{'label': col, 'value': col} for col in data.columns if col not in ['player_name', 'season']]
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

    data = Data().get_season_data(selected_season)
    filtered_data = data[data['player_name'].isin(selected_players)].copy()

    for stat in selected_stats:
        # Sort the stats and assign ranks
        stat_values = filtered_data[stat].tolist()
        sorted_values = rs.radix_sort(stat_values) if sorting_method == 'radix' else hs.heap_sort(stat_values)
        rank_series = pd.Series(sorted_values).rank(method='min')
        rank_mapping = {value: rank for value, rank in zip(sorted_values, rank_series)}
        filtered_data[stat + ' Rank'] = filtered_data[stat].map(rank_mapping)

    # Construct the radar plot
    fig = go.Figure()
    for player in selected_players:
        player_data = filtered_data[filtered_data['player_name'] == player]
        fig.add_trace(go.Scatterpolar(
            r=[player_data[stat + ' Rank'].iloc[0] for stat in selected_stats],
            theta=[stat + ' Rank' for stat in selected_stats],
            fill='toself',
            name=player
        ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
