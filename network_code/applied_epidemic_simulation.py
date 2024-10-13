import networkx as nx
import numpy as np
import random  
from tolerance_simulation import EpidemicToleranceSimulation
from epidemic_functions import *
from remotion_functions import error, attack
from plot_functions import plot_of_two_data

# netwok constants
N = 1000  #number of nodes
p = 0.004 #probability to connect with other nodes
k = N*p   # average degree

# epidemic data 
mu = 0.2
nu = 0.05
duration =50
infected_t0 = 1

# for reproducibility
seed = 102
random.seed(seed)
np.random.seed(seed)

# for multiple simulations (multiple simulation are kept on to include randomness in the results)
num_simulations = 100  # Number of simulations to run
num_points = 15

# creation of the network
erdos_renyi_net = nx.erdos_renyi_graph(N, p, directed=False)
# set k/2 because the graph is undirected
scale_free_net = nx.barabasi_albert_graph(N, int(k/2))

ER_epid_sim = EpidemicToleranceSimulation(erdos_renyi_net, mu, nu, duration, infected_t0, 0.5, num_points)
SF_epid_sim = EpidemicToleranceSimulation(scale_free_net, mu, nu, duration, infected_t0, 0.5, num_points)


#____________ data for the epidemic duration _________________

# under error 
freq, duration_attack_ER = ER_epid_sim.epidemic_property_vs_removals(epidemic_duration, attack, num_simulations)
_, duration_attack_SF = SF_epid_sim.epidemic_property_vs_removals(epidemic_duration, attack, num_simulations)

# under attack 
freq, duration_error_ER = ER_epid_sim.epidemic_property_vs_removals(epidemic_duration, error, num_simulations)
_, duration_error_SF = SF_epid_sim.epidemic_property_vs_removals(epidemic_duration, error, num_simulations)

fig, ax = plot_of_two_data(freq, duration_error_ER, 'error on ER', True, freq, duration_error_SF, label2 = 'error on SF', ylabel='Epidemic duration', xlabel='Frequency', title = 'Epidemic duration v/s Frequency of removals')   
ax.plot(freq, duration_attack_ER, label = 'attack on ER', color='red', marker='o', linestyle ='--')
ax.plot(freq, duration_attack_SF, label = 'attack on SF', color='red', marker='s')
ax.legend()

#____________ data for the t_peak of the epidemic ____________

# under error
freq, t_peak_attack_ER = ER_epid_sim.epidemic_property_vs_removals(t_peak, attack, num_simulations)
_, t_peak_attack_SF, = SF_epid_sim.epidemic_property_vs_removals(t_peak, attack, num_simulations)

# under attack
freq, t_peak_error_ER = ER_epid_sim.epidemic_property_vs_removals(t_peak, error, num_simulations)
_, t_peak_error_SF = SF_epid_sim.epidemic_property_vs_removals(t_peak, error, num_simulations)

fig, ax = plot_of_two_data(freq, t_peak_error_ER, 'error on ER', True, freq, t_peak_error_SF, label2 = 'error on SF', ylabel='Time infection peak', xlabel='Frequency', title = 'Time infection peak v/s Frequency of removals')   
ax.plot(freq, t_peak_attack_ER, label = 'attack on ER', color='red', marker='o', linestyle ='--')
ax.plot(freq, t_peak_attack_SF, label = 'attack on SF', color='red', marker='s')
ax.legend()


#____________ data for the peak of the epidemic ____________

# under error
freq, peak_attack_ER = ER_epid_sim.epidemic_property_vs_removals(peak, attack, num_simulations)
_, peak_attack_SF, = SF_epid_sim.epidemic_property_vs_removals(peak, attack, num_simulations)

# under attack
freq, peak_error_ER = ER_epid_sim.epidemic_property_vs_removals(peak, error, num_simulations)
_, peak_error_SF = SF_epid_sim.epidemic_property_vs_removals(peak, error, num_simulations)

fig, ax = plot_of_two_data(freq, peak_error_ER, 'error on ER', True, freq, peak_error_SF, label2 = 'error on SF', ylabel='Infection peak', xlabel='Frequency', title = 'Infection peak v/s Frequency of removals')   
ax.plot(freq, peak_attack_ER, label = 'attack on ER', color='red', marker='o', linestyle ='--')
ax.plot(freq, peak_attack_SF, label = 'attack on SF', color='red', marker='s')
ax.legend()


#____________ data for the total percentage of infected at the end of the epidemic ____________

# under error
freq, infected_attack_ER = ER_epid_sim.epidemic_property_vs_removals(total_infected_percentage, attack, num_simulations)
_, infected_attack_SF, = SF_epid_sim.epidemic_property_vs_removals(total_infected_percentage, attack, num_simulations)

# under attack
freq, infected_error_ER = ER_epid_sim.epidemic_property_vs_removals(total_infected_percentage, error, num_simulations)
_, infected_error_SF = SF_epid_sim.epidemic_property_vs_removals(total_infected_percentage, error, num_simulations)

fig, ax = plot_of_two_data(freq, infected_error_ER, 'error on ER', True, freq, infected_error_SF, label2 = 'error on SF', ylabel='Total infected', xlabel='Frequency', title = 'Total infected v/s Frequency of removals')   
ax.plot(freq, infected_attack_ER, label = 'attack on ER', color='red', marker='o', linestyle ='--')
ax.plot(freq, infected_attack_SF, label = 'attack on SF', color='red', marker='s')
ax.legend()