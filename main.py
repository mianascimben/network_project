# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 18:16:01 2024

@author: mima
"""

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import zipfile
import io

# Path al file ZIP
zip_path = 'C:/Users/mima/Desktop/Network_project/archive.zip'

# open zip file and read the CSV
with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open('routes.csv') as file1:
        routes=pd.read_csv(file1, delimiter=',', na_values=r'\N')
    with z.open('airports.csv') as file2:
        airports=pd.read_csv(file2, delimiter=',', na_values=r'\N')

#cleaning data
routes_clean = routes.dropna(subset=['Source airport', 'Destination airport'])
airports_clean = airports.dropna(subset = ['IATA'])

routes_clean2 = routes_clean.drop(routes_clean[~routes_clean['Source airport'].isin(airports_clean['IATA']) | ~routes_clean['Destination airport'].isin(airports_clean['IATA'])].index)

#creation of the dictionary for the airports positions
air_pos = dict(zip(airports_clean['IATA'], zip(airports_clean['Longitude'], airports_clean['Latitude'])))

# creation of a graph
G = nx.from_pandas_edgelist(routes_clean2, source = 'Source airport', target = 'Destination airport')

#visualization of the data
fig = plt.scatter('Longitude', 'Latitude', data = airports_clean, s=8)

nx.draw(G, air_pos, node_color='lightblue', edge_color='gray', node_size=10)
