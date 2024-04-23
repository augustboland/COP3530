import pandas as pd
import radixSort as rs
import heapSort as hs

class Data:
    def __init__(self):
        self.df = pd.read_csv('Data/all_seasons 2.csv')

    def get_seasons(self):
        return self.df['season'].unique()

    def get_players(self, season):
        return self.df[self.df['season'] == season]['player_name'].unique()

    def get_stats(self):
        # Return all column names except 'player_name' and 'season'
        return [col for col in self.df.columns if col not in ['player_name', 'season']]

    def get_season_data(self, season):
        # Return data for the selected season
        return self.df[self.df['season'] == season].copy()

    def temp(self):
        # Temporary access to the DataFrame for debugging
        return self.df
