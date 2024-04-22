import pandas as pd
import radixSort
import heapSort

##Use this class. 
##Access all the data with access so I can make changes without breaking
##whatever functions you make.

class Data:
    
    def __init__(self):
        self.data = pd.read_csv('Data/all_seasons 2.csv')
        self.df = pd.DataFrame(self.data)

    def access(self, column, row):
        return self.df.at[column][row]
    #From stackoverflow on dataframes.
    def radix_sort(df, column):
        # Copy the specific column to a new list
        arr = self.df[column].tolist()
        # Sort the list using Radix Sort
        radix_sort(arr)
        # Create a rank dictionary
        rank_dict = {value: x + 1 for x, value in enumerate(arr)}
        # Map the ranks back to the DataFrame
        df[column+'Rank'] = self.df[column].map(rank_dict)
    
    def acces(self, column):
        return self.df[column]
    def columns(self):
        return self.df.columns
    def temp(self):
        return self.df
