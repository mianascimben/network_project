# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 15:17:06 2024

@author: mima
"""
import pandas as pd
import networkx as nx
import zipfile
import pickle
from functions import diameter_vs_removals, SizeLargestComponent_vs_removals, AverageSize_vs_removals
from plot_functions import plot_of_two_data


'''
# Path al file ZIP
zip_path = 'C:/Users/mima/Desktop/network-project/archive.zip'

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
'''    

air_traffic_net = G

# data for the diameter
freq_error, d_error = diameter_vs_removals(air_traffic_net, True)
freq_attack, d_attack = diameter_vs_removals(air_traffic_net, False)

# plot of diameter
fig, ax = plot_of_two_data(freq_error, d_error, 'error', True, freq_attack, d_attack, label2 = 'attack', ylabel='Diamater', xlabel='Frequency', title = 'Diameter v/s Frequency of removals')   

#data for the size 
freq_error, sizes_error =SizeLargestComponent_vs_removals(air_traffic_net, True, 0.5)
freq_attack, sizes_attack = SizeLargestComponent_vs_removals(air_traffic_net, False, 0.5)

# get the data for the average size plot
freq_error, average_size_error =AverageSize_vs_removals(air_traffic_net, True, 0.5)
freq_attack, average_size_attack = AverageSize_vs_removals(air_traffic_net, False, 0.5)

# plot of S and <s>

fig, ax = plot_of_two_data(freq_error, sizes_error, 'S vs error', True, freq_error, average_size_error, label2 = '<s> vs error', ylabel='S, <s>', xlabel='Frequency', title = 'Erdos Renyi: S and <s>')   
ax.plot(freq_attack, sizes_attack, label = 'S v/s attack', color='red', marker='o', linestyle ='--')
ax.plot(freq_attack, average_size_attack, label = '<s> v/s attack', color='red', marker='s')
ax.legend()