import networkx as nx
import numpy as np
import random 
from simulation_tools.tolerance_simulation import ToleranceSimulation
from simulation_tools.graph_property_functions import get_diameter, largest_connected_component_size, average_size_connected_components
from simulation_tools.remotion_functions import attack, error
from simulation_tools.plot_functions import plot_of_two_data

# netwok constants
N = 1000 #number of nodes
p = 0.004  #probability to connect with other nodes
k = N*p   # average degree

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

#under error
freq, d_error_ER = Tol_Sim_ER.graph_property_vs_removals(get_diameter, error)
_, d_error_SF = Tol_Sim_SF.graph_property_vs_removals(get_diameter, error)

#under attack
_, d_attack_ER = Tol_Sim_ER.graph_property_vs_removals(get_diameter, attack)
_, d_attack_SF = Tol_Sim_SF.graph_property_vs_removals(get_diameter, attack)

fig, ax = plot_of_two_data(freq, d_error_ER, 'error on ER', True, freq, d_error_SF, label2 = 'error on SF', ylabel='Diamater', xlabel='Frequency', title = 'Diameter v/s Frequency of removals')   
ax.plot(freq, d_attack_ER, label = 'attack on ER', color='red', marker='o', linestyle ='--')
ax.plot(freq, d_attack_SF, label = 'attack on SF', color='red', marker='s')
ax.legend()

# ____________ data for S ________________________________________

#under error
freq, S_error_ER = Tol_Sim_ER.graph_property_vs_removals(largest_connected_component_size, error)
_, S_error_SF = Tol_Sim_SF.graph_property_vs_removals(largest_connected_component_size, error)

#under attack
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
fig, ax = plot_of_two_data(freq, S_error_ER, 'S vs error', True, freq, s_error_ER, label2 = '<s> vs error', ylabel='S, <s>', xlabel='Frequency', title = 'Erdos Renyi: S and <s>')   
ax.plot(freq, S_attack_ER, label = 'S v/s attack', color='red', marker='o', linestyle ='--')
ax.plot(freq, s_attack_ER, label = '<s> v/s attack', color='red', marker='s')
ax.legend()

# plot for the S and <s> for SF
fig, ax = plot_of_two_data(freq, S_error_SF, 'S vs error', True, freq, s_error_SF, label2 = '<s> vs error', ylabel='S, <s>', xlabel='Frequency', title = 'Scale Free: S and <s>')   
ax.plot(freq, S_attack_SF, label = 'S v/s attack', color='red', marker='o', linestyle ='--')
ax.plot(freq, s_attack_SF, label = '<s> v/s attack', color='red', marker='s')
ax.legend()
