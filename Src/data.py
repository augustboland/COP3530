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
