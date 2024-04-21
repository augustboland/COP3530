import pandas as pd

##Use this class. 
##Access all the data with access so I can make changes without breaking
##whatever functions you make.

class Data:
    
    def __init__(self):
        self.data = pd.read_csv('data.csv')
        self.df = pd.DataFrame(self.data)

    def access(self, column, row):
        return self.df[column][row]

    def add_rank_to_dataframe(df, column):
    # Copy the specific column to a new list
    arr = df[column].tolist()
    # Sort the list using Radix Sort
    radix_sort(arr)
    # Create a rank dictionary
    rank_dict = {value: x + 1 for x, value in enumerate(arr)}
    # Map the ranks back to the DataFrame
    df['Rank'] = df[column].map(rank_dict)
