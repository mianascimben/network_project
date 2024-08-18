# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 18:16:01 2024

@author: mima

Downloading data of flight trasportation, cleaning them and creation of a graph 
"""
import os
import pandas as pd
import networkx as nx
import zipfile
import pickle


# Path al file ZIP
zip_path = os.path.join('data', 'airports_network.zip')

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

routes_clean2 = routes_clean.drop(routes_clean[~routes_clean['Source airport ID'].isin(airports_clean['Airport ID']) | ~routes_clean['Destination airport ID'].isin(airports_clean['Airport ID'])].index)

#creation of the dictionary for the airports positions
air_pos = dict(zip(airports_clean['Airport ID'], zip(airports_clean['Longitude'], airports_clean['Latitude'])))

# creation of a graph
G = nx.from_pandas_edgelist(routes_clean2, source = 'Source airport ID', target = 'Destination airport ID')

with open('flight.gpickle', 'wb') as f:
    pickle.dump(G, f, pickle.HIGHEST_PROTOCOL)

