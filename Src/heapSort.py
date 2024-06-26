import pandas as pd
# Implementing heap sort
# https://www.geeksforgeeks.org/python-program-for-heap-sort/ 
def heap_sort(arr):
    def heapify(arr, n, i):
        largest_value = i
        left_child = 2 * i + 1
        right_child = 2 * i + 2

        # Check if left child of root exists and is greater than root
        if left_child < n and arr[left_child] > arr[largest_value]:
            largest_value = left_child

        # Check if right child of root exists and is greater than the largest so far
        if right_child < n and arr[right_child] > arr[largest_value]:
            largest_value = right_child

        # Change root, if needed
        if largest_value != i:
            arr[i], arr[largest_value] = arr[largest_value], arr[i]  # swap
            heapify(arr, n, largest_value)

    n = len(arr)
    # Create a max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # One by one extract elements
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        heapify(arr, i, 0)

    return arr

# read the data set into a data frame
# https://www.geeksforgeeks.org/python-pandas-dataframe/
data_frame = pd.read_csv('Data/all_seasons 2.csv')

# create tuples containing stats for each player and season for each player
# https://www.geeksforgeeks.org/creating-a-pandas-dataframe-using-list-of-tuples/
pts_data_points = [(row['player_name'], row['pts'], row['season']) for index, row in data_frame.iterrows()]
reb_data_points = [(row['player_name'], row['reb'], row['season']) for index, row in data_frame.iterrows()]
ast_data_points = [(row['player_name'], row['ast'], row['season']) for index, row in data_frame.iterrows()]
net_rating_data_points = [(row['player_name'], row['net_rating'], row['season']) for index, row in data_frame.iterrows()]
oreb_pct_data_points = [(row['player_name'], row['oreb_pct'], row['season']) for index, row in data_frame.iterrows()]
dreb_pct_data_points = [(row['player_name'], row['dreb_pct'], row['season']) for index, row in data_frame.iterrows()]
usg_pct_data_points = [(row['player_name'], row['usg_pct'], row['season']) for index, row in data_frame.iterrows()]
ts_pct_data_points = [(row['player_name'], row['ts_pct'], row['season']) for index, row in data_frame.iterrows()]
ast_pct_data_points = [(row['player_name'], row['ast_pct'], row['season']) for index, row in data_frame.iterrows()]

# heap sort each player stat being sorted
heap_sort(pts_data_points)
heap_sort(reb_data_points)
heap_sort(ast_data_points)
heap_sort(net_rating_data_points)
heap_sort(oreb_pct_data_points)
heap_sort(dreb_pct_data_points)
heap_sort(usg_pct_data_points)
heap_sort(ts_pct_data_points)
heap_sort(ast_pct_data_points)

# reconstruct the data frame with the sorted data
pts_sorted_data = pd.DataFrame(pts_data_points, columns=['player_name', 'pts', 'season'])
reb_sorted_data = pd.DataFrame(reb_data_points, columns=['player_name', 'reb', 'season'])
ast_sorted_data = pd.DataFrame(ast_data_points, columns=['player_name', 'ast', 'season'])
net_rating_sorted_data = pd.DataFrame(net_rating_data_points, columns=['player_name', 'net_rating', 'season'])
oreb_pct_sorted_data = pd.DataFrame(oreb_pct_data_points, columns=['player_name', 'oreb_pct', 'season'])
dreb_pct_sorted_data = pd.DataFrame(dreb_pct_data_points, columns=['player_name', 'dreb_pct', 'season'])
usg_pct_sorted_data = pd.DataFrame(usg_pct_data_points, columns=['player_name', 'usg_pct', 'season'])
ts_pct_sorted_data = pd.DataFrame(ts_pct_data_points, columns=['player_name', 'ts_pct', 'season'])
ast_pct_sorted_data = pd.DataFrame(ast_pct_data_points, columns=['player_name', 'ast_pct', 'season'])
