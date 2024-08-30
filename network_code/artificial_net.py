# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 16:24:11 2024

@author: mima
"""

import networkx as nx
import numpy as np
#import matplotlib.pyplot as plt
import random 
import time 
from Tolerance_Simulation import *
from functions import *
from plot_functions import plot_of_two_data

start = time.time()
N = 1000  #number of nodes
p = 0.004  #probability to connect with other nodes
k = N*p   # average degree
seed = 102

# for reproducibility
random.seed(seed)
np.random.seed(seed)

#G = nx.random_regular_graph(int(k), N)
erdos_renyi_net = nx.erdos_renyi_graph(N, p, directed=False)
# set k/2 because the graph is undirected
scale_free_net = nx.barabasi_albert_graph(N, int(k/2))

Tol_Sim_ER = ToleranceSimulation(erdos_renyi_net, max_removal_rate = 0.5)
Tol_Sim_SF = ToleranceSimulation(scale_free_net, max_removal_rate = 0.5)

freq, d_attack_ER = Tol_Sim_ER.graph_property_vs_removals(get_diameter, attack)
_, d_error_ER = Tol_Sim_ER.graph_property_vs_removals(get_diameter, error)

_, d_attack_SF = Tol_Sim_SF.graph_property_vs_removals(get_diameter, attack)
_, d_error_SF = Tol_Sim_SF.graph_property_vs_removals(get_diameter, error)

fig, ax = plot_of_two_data(freq, d_error_ER, 'error on Erdos Renyi net', True, freq, d_error_SF, label2 = 'error on Scale Free net', ylabel='Diamater', xlabel='Frequency', title = 'Diameter v/s Frequency of removals')   
ax.plot(freq, d_attack_ER, label = 'attack on Erdos Renyi net', color='red', marker='o', linestyle ='--')
ax.plot(freq, d_attack_SF, label = 'attack on Scale Free net', color='red', marker='s')
ax.legend()

#_____________________________________________________________________________


freq, S_attack_ER = Tol_Sim_ER.graph_property_vs_removals(largest_connected_component_size, attack)
_, S_error_ER = Tol_Sim_ER.graph_property_vs_removals(largest_connected_component_size, error)

_, S_attack_SF = Tol_Sim_SF.graph_property_vs_removals(largest_connected_component_size, attack)
_, S_error_SF = Tol_Sim_SF.graph_property_vs_removals(largest_connected_component_size, error)


freq, s_attack_ER = Tol_Sim_ER.graph_property_vs_removals(average_size_connected_components, attack)
_, s_error_ER = Tol_Sim_ER.graph_property_vs_removals(average_size_connected_components, error)

_, s_attack_SF = Tol_Sim_SF.graph_property_vs_removals(average_size_connected_components, attack)
_, s_error_SF = Tol_Sim_SF.graph_property_vs_removals(average_size_connected_components, error)


fig, ax = plot_of_two_data(freq, S_error_ER, 'S vs error', True, freq, s_error_ER, label2 = '<s> vs error', ylabel='S, <s>', xlabel='Frequency', title = 'Erdos Renyi: S and <s>')   
ax.plot(freq, S_attack_ER, label = 'S v/s attack', color='red', marker='o', linestyle ='--')
ax.plot(freq, s_attack_ER, label = '<s> v/s attack', color='red', marker='s')
ax.legend()

# plot for the S and <s> for SF
fig, ax = plot_of_two_data(freq, S_error_SF, 'S vs error', True, freq, s_error_SF, label2 = '<s> vs error', ylabel='S, <s>', xlabel='Frequency', title = 'Scale Free: S and <s>')   
ax.plot(freq, S_attack_SF, label = 'S v/s attack', color='red', marker='o', linestyle ='--')
ax.plot(freq, s_attack_SF, label = '<s> v/s attack', color='red', marker='s')
ax.legend()
print(time.time()-start)