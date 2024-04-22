import pandas as pd
# Implementing heap sort
def heap_sort(arr):
    def heapify(arr, n, i):
        largest = i  # Initialize largest as root
        l = 2 * i + 1  # left = 2*i + 1
        r = 2 * i + 2  # right = 2*i + 2

        # See if left child of root exists and is greater than root
        if l < n and arr[l][1] > arr[largest][1]:
            largest = l

        # See if right child of root exists and is greater than the largest so far
        if r < n and arr[r][1] > arr[largest][1]:
            largest = r

        # Change root, if needed
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]  # swap

            # Heapify the root
            heapify(arr, n, largest)

    n = len(arr)

    # Build a maxheap.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        heapify(arr, i, 0)

# Read the dataset into a DataFrame
df = pd.read_csv('Data/all_seasons 2.csv')

# Create tuples containing (player name, points, season) for each player
pts_data_points = [(row['player_name'], row['pts'], row['season']) for index, row in df.iterrows()]
reb_data_points = [(row['player_name'], row['reb'], row['season']) for index, row in df.iterrows()]
ast_data_points = [(row['player_name'], row['ast'], row['season']) for index, row in df.iterrows()]
net_rating_data_points = [(row['player_name'], row['net_rating'], row['season']) for index, row in df.iterrows()]
oreb_pct_data_points = [(row['player_name'], row['oreb_pct'], row['season']) for index, row in df.iterrows()]
dreb_pct_data_points = [(row['player_name'], row['dreb_pct'], row['season']) for index, row in df.iterrows()]
usg_pct_data_points = [(row['player_name'], row['usg_pct'], row['season']) for index, row in df.iterrows()]
ts_pct_data_points = [(row['player_name'], row['ts_pct'], row['season']) for index, row in df.iterrows()]
ast_pct_data_points = [(row['player_name'], row['ast_pct'], row['season']) for index, row in df.iterrows()]

# Apply heap sort to the list of tuples based on points
heap_sort(pts_data_points)
heap_sort(reb_data_points)
heap_sort(ast_data_points)
heap_sort(net_rating_data_points)
heap_sort(oreb_pct_data_points)
heap_sort(dreb_pct_data_points)
heap_sort(usg_pct_data_points)
heap_sort(ts_pct_data_points)
heap_sort(ast_pct_data_points)

# Reconstruct the DataFrame with the sorted data
pts_sorted_data = pd.DataFrame(pts_data_points, columns=['player_name', 'pts', 'season'])
reb_sorted_data = pd.DataFrame(reb_data_points, columns=['player_name', 'reb', 'season'])
ast_sorted_data = pd.DataFrame(ast_data_points, columns=['player_name', 'ast', 'season'])
net_rating_sorted_data = pd.DataFrame(net_rating_data_points, columns=['player_name', 'net_rating', 'season'])
oreb_pct_sorted_data = pd.DataFrame(oreb_pct_data_points, columns=['player_name', 'oreb_pct', 'season'])
dreb_pct_sorted_data = pd.DataFrame(dreb_pct_data_points, columns=['player_name', 'dreb_pct', 'season'])
usg_pct_sorted_data = pd.DataFrame(usg_pct_data_points, columns=['player_name', 'usg_pct', 'season'])
ts_pct_sorted_data = pd.DataFrame(ts_pct_data_points, columns=['player_name', 'ts_pct', 'season'])
ast_pct_sorted_data = pd.DataFrame(ast_pct_data_points, columns=['player_name', 'ast_pct', 'season'])


# Print the sorted DataFrame
#print(pts_sorted_data)
#print(reb_sorted_data)
#print(ast_sorted_data)
#print(net_rating_sorted_data)
#print(oreb_pct_sorted_data)
#print(dreb_pct_sorted_data)
#print(usg_pct_sorted_data)
#print(ts_pct_sorted_data)
#print(ast_pct_sorted_data)
