"""

This file downloads the data of the global airlines and cleans them.
Then it creates a graph of type "classes.graph.Graph" and saves it as gpickle 
file under the name "flight"

"""

import os
import pandas as pd
import networkx as nx
import zipfile
import pickle


# Path to ZIP file: 'airports_network.zip' should be in the 'data' folder as
# downloaded by the github repository 'https://github.com/mianascimben/network-project/tree/main/data'
# If you change the name of the forlder 'data', change 'data_dir' variable with the new name
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Directory of the script
data_dir = 'data'
file_name = 'airports_network.zip'
zip_path = os.path.join(script_dir, data_dir, file_name)


# open zip file and read the CSV
with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open('routes.csv') as file1:
        routes=pd.read_csv(file1, delimiter=',', na_values=r'\N')
    with z.open('airports.csv') as file2:
        airports=pd.read_csv(file2, delimiter=',', na_values=r'\N')

# cleaning data: erase routes if the source or the destination is NAN
routes_clean = routes.dropna(subset=['Source airport ID', 'Destination airport ID'])
# cleaning data: erase all airport information if its ID is NAN
airports_clean = airports.dropna(subset = ['Airport ID'])
# clening data: erase all the routes that have only either the destination or the starting airport
routes_clean2 = routes_clean.drop(routes_clean[~routes_clean['Source airport ID'].isin(airports_clean['Airport ID']) | ~routes_clean['Destination airport ID'].isin(airports_clean['Airport ID'])].index)

# creation of the dictionary for the airports positions
air_pos = dict(zip(airports_clean['Airport ID'], zip(airports_clean['Longitude'], airports_clean['Latitude'])))

# creation of a graph from the cleaned dataset
G = nx.from_pandas_edgelist(routes_clean2, source = 'Source airport ID', target = 'Destination airport ID')

# save the graph 'G'
with open('flight.gpickle', 'wb') as f:
    pickle.dump(G, f, pickle.HIGHEST_PROTOCOL)


