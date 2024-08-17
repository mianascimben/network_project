
"""
Created on Sun Jun 16 11:08:45 2024

@author: mima
"""

# here we study ER and scale_free_net networks and we get the result of the paper
#import numpy as np
import networkx as nx
#import matplotlib.pyplot as plt
import random 
import time 
from functions import diameter_vs_removals, SizeLargestComponent_vs_removals, AverageSize_vs_removals
from plot_functions import plot_of_two_data

start = time.time()
N = 1000  #number of nodes
p = 0.004  #probability to connect with other nodes
k = N*p   # average degree
seed = 102

# for reproducibility
random.seed(seed)

erdos_renyi_net = nx.erdos_renyi_graph(N, p, directed=False)
# set k/2 because the graph is undirected
scale_free_net = nx.barabasi_albert_graph(N, int(k/2))

nx.draw(erdos_renyi_net)
#nx.draw(scale_free_net)

# check the degree distribution by plot

#degree_ER, freq_ER = frequency_network_degree(erdos_renyi_net)


#get the data for the diameter plot
freq_error_ER, d_error_ER = diameter_vs_removals(erdos_renyi_net, True, 0.5)
freq_error_SF, d_error_SF = diameter_vs_removals(scale_free_net, True, 0.5)
freq_attack_ER, d_attack_ER = diameter_vs_removals(erdos_renyi_net, False, 0.5)
freq_attack_SF, d_attack_SF = diameter_vs_removals(scale_free_net, False, 0.5)

#get the data for the size plot

freq_error_ER, sizes_error_ER =SizeLargestComponent_vs_removals(erdos_renyi_net, True, 0.5)
freq_error_SF, sizes_error_SF = SizeLargestComponent_vs_removals(scale_free_net, True, 0.5)
freq_attack_ER, sizes_attack_ER = SizeLargestComponent_vs_removals(erdos_renyi_net, False, 0.5)
freq_attack_SF, sizes_attack_SF = SizeLargestComponent_vs_removals(scale_free_net, False, 0.5)

# get the data for the average size plot

freq_error_ER, average_size_error_ER =AverageSize_vs_removals(erdos_renyi_net, True, 0.5)
freq_error_SF, average_size_error_SF = AverageSize_vs_removals(scale_free_net, True, 0.5)
freq_attack_ER, average_size_attack_ER = AverageSize_vs_removals(erdos_renyi_net, False, 0.5)
freq_attack_SF, average_size_attack_SF = AverageSize_vs_removals(scale_free_net, False, 0.5)

# plot for the diameter
fig, ax = plot_of_two_data(freq_error_ER, d_error_ER, 'error on Erdos Renyi net', True, freq_error_SF, d_error_SF, label2 = 'error on Scale Free net', ylabel='Diamater', xlabel='Frequency', title = 'Diameter v/s Frequency of removals')   
ax.plot(freq_attack_ER, d_attack_ER, label = 'attack on Erdos Renyi net', color='red', marker='o', linestyle ='--')
ax.plot(freq_attack_SF, d_attack_SF, label = 'attack on Scale Free net', color='red', marker='s')
ax.legend()

# plot for the S
fig, ax = plot_of_two_data(freq_error_ER, sizes_error_ER, 'error on Erdos Renyi net', True, freq_error_SF, sizes_error_SF, label2 = 'error on Scale Free net', ylabel='S', xlabel='Frequency', title = 'S v/s Frequency of removals')   
ax.plot(freq_attack_ER, sizes_attack_ER, label = 'attack on Erdos Renyi net', color='red', marker='o', linestyle ='--')
ax.plot(freq_attack_SF, sizes_attack_SF, label = 'attack on Scale Free net', color='red', marker='s')
ax.legend()

# plot for the S and <s> for ER
fig, ax = plot_of_two_data(freq_error_ER, sizes_error_ER, 'S vs error', True, freq_error_ER, average_size_error_ER, label2 = '<s> vs error', ylabel='S, <s>', xlabel='Frequency', title = 'Erdos Renyi: S and <s>')   
ax.plot(freq_attack_ER, sizes_attack_ER, label = 'S v/s attack', color='red', marker='o', linestyle ='--')
ax.plot(freq_attack_ER, average_size_attack_ER, label = '<s> v/s attack', color='red', marker='s')
ax.legend()

# plot for the S and <s> for SF
fig, ax = plot_of_two_data(freq_error_SF, sizes_error_SF, 'S vs error', True, freq_error_SF, average_size_error_SF, label2 = '<s> vs error', ylabel='S, <s>', xlabel='Frequency', title = 'Scale Free: S and <s>')   
ax.plot(freq_attack_SF, sizes_attack_SF, label = 'S v/s attack', color='red', marker='o', linestyle ='--')
ax.plot(freq_attack_SF, average_size_attack_SF, label = '<s> v/s attack', color='red', marker='s')
ax.legend()

time.time()-start