'''

This script perfoms simulations of errors and attacks on the Erdos-Renyi and 
the Scale-Free networks.
For each fraction of node removals the 'diameter', the 
'largest_connected_component_size' and the 'average_size_connected_components' 
are calculated and plotted w.r.t. the removal frequencies. 

'''

import networkx as nx
import numpy as np
import random 
from simulation_tools.tolerance_simulation import ToleranceSimulation
from simulation_tools.graph_property_functions import diameter, largest_connected_component_size, average_size_connected_components
from simulation_tools.remotion_functions import attack, error
from simulation_tools.plot_functions import plot_multiple_data

# netwok constants
N = 1000   #number of nodes
p = 0.004  #probability to connect with other nodes
k = N*p    # average degree

# for reproducibility
seed = 102
random.seed(seed)
np.random.seed(seed)


# creation of the artificial networks
erdos_renyi_net = nx.erdos_renyi_graph(N, p, directed=False)

# set k/2 because the graph is undirected
scale_free_net = nx.barabasi_albert_graph(N, int(k/2))

Tol_Sim_ER = ToleranceSimulation(erdos_renyi_net, max_removal_rate = 0.5)
Tol_Sim_SF = ToleranceSimulation(scale_free_net, max_removal_rate = 0.5)

# ____________ data for diameter ________________________________________

# under error
freq, d_error_ER = Tol_Sim_ER.graph_property_vs_removals(diameter, error)
freq, d_error_SF = Tol_Sim_SF.graph_property_vs_removals(diameter, error)

# under attack
_, d_attack_ER = Tol_Sim_ER.graph_property_vs_removals(diameter, attack)
_, d_attack_SF = Tol_Sim_SF.graph_property_vs_removals(diameter, attack)

fig, ax = plot_multiple_data(x_data = [freq, freq, freq, freq], 
                             y_data = [d_error_ER, d_attack_ER, d_error_SF, d_attack_SF],  
                             labels=['error on ER', 'attack on ER', 'error on SF', 'attack on SF'],
                             colors=['blue', 'red', 'blue', 'red'],
                             markers=['o', 'o', 's', 's'],
                             linestyles=['--', '--', '-', '-'],
                             ylabel='Diameter', xlabel='Frequency',
                             title='Diameter on SF and ER')

# ____________ data for S ________________________________________

# under error
freq, S_error_ER = Tol_Sim_ER.graph_property_vs_removals(largest_connected_component_size, error)
_, S_error_SF = Tol_Sim_SF.graph_property_vs_removals(largest_connected_component_size, error)

# under attack
_, S_attack_ER = Tol_Sim_ER.graph_property_vs_removals(largest_connected_component_size, attack)
_, S_attack_SF = Tol_Sim_SF.graph_property_vs_removals(largest_connected_component_size, attack)


# ____________ data for <s> ________________________________________

# under error
freq, s_error_ER = Tol_Sim_ER.graph_property_vs_removals(average_size_connected_components, error)
_, s_error_SF = Tol_Sim_SF.graph_property_vs_removals(average_size_connected_components, error)

# under attack
_, s_attack_ER = Tol_Sim_ER.graph_property_vs_removals(average_size_connected_components, attack)
_, s_attack_SF = Tol_Sim_SF.graph_property_vs_removals(average_size_connected_components, attack)

# plot for the S and <s> for ER
fig, ax = plot_multiple_data(x_data = [freq, freq, freq, freq], 
                             y_data = [S_error_ER, S_attack_ER, s_error_ER, s_attack_ER],  
                             labels=['S vs error', 'S vs attack', '<s> vs error', '<s> vs attack'],
                             colors=['blue', 'red', 'blue', 'red'],
                             markers=['o', 'o', 's', 's'],
                             linestyles=['--', '--', '-', '-'],
                             ylabel='S, <s>', xlabel='Frequency',
                             title='Erdos Renyi: S and <s>')

# plot for the S and <s> for SF
fig, ax = plot_multiple_data(x_data = [freq, freq, freq, freq], 
                             y_data = [S_error_SF, S_attack_SF, s_error_SF, s_attack_SF],  
                             labels=['S vs error', 'S vs attack', '<s> vs error', '<s> vs attack'],
                             colors=['blue', 'red', 'blue', 'red'],
                             markers=['o', 'o', 's', 's'],
                             linestyles=['--', '--', '-', '-'],
                             ylabel='S, <s>', xlabel='Frequency',
                             title='Scale-Free: S and <s>')

