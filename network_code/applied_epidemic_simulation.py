'''

This script perfoms epidemic simulations on the Erdos-Renyi and the Scale-Free 
networks, and calculates the value of some epidemic features as the fraction 
of nodes removed increases.
'num_simulations' epidemics are runned on each network
after having been subjected to an increasing fraction of node removals. 
For each simulation epidemic properties are calculated, averaged over
all the simulations and finally displayed on a plot w.r.t.the removal frequencies.

'''
import networkx as nx
import numpy as np
import random  
from simulation_tools.tolerance_simulation import EpidemicToleranceSimulation
from simulation_tools.epidemic_functions import *
from simulation_tools.remotion_functions import error, attack
from simulation_tools.plot_functions import plot_multiple_data

# netwok constants
N = 1000   # number of nodes
p = 0.004  # probability to connect with other nodes
k = N*p   # average degree

# epidemic constants
mu = 0.2         # infection prob
nu = 0.05        # recovery prob
duration = 50     # duration of the simulation
infected_t0 = 1  # number of infected nodes at the fist time step

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


fig, ax = plot_multiple_data(x_data = [freq, freq, freq, freq], 
                             y_data = [duration_error_ER, duration_attack_ER, duration_error_SF, duration_attack_SF],  
                             labels=['error on ER', 'attack on ER', 'error on SF', 'attack on SF'],
                             colors=['blue', 'red', 'blue', 'red'],
                             markers=['o', 'o', 's', 's'],
                             linestyles=['--', '--', '-', '-'],
                             ylabel='Duration', xlabel='Frequency',
                             title='Epidemic Duration on SF and ER')


#____________ data for the t_peak of the epidemic ____________

# under error
freq, t_peak_attack_ER = ER_epid_sim.epidemic_property_vs_removals(t_peak, attack, num_simulations)
_, t_peak_attack_SF, = SF_epid_sim.epidemic_property_vs_removals(t_peak, attack, num_simulations)

# under attack
freq, t_peak_error_ER = ER_epid_sim.epidemic_property_vs_removals(t_peak, error, num_simulations)
_, t_peak_error_SF = SF_epid_sim.epidemic_property_vs_removals(t_peak, error, num_simulations)


fig, ax = plot_multiple_data(x_data = [freq, freq, freq, freq], 
                             y_data = [t_peak_error_ER, t_peak_attack_ER, t_peak_error_SF, t_peak_attack_SF],  
                             labels=['error on ER', 'attack on ER', 'error on SF', 'attack on SF'],
                             colors=['blue', 'red', 'blue', 'red'],
                             markers=['o', 'o', 's', 's'],
                             linestyles=['--', '--', '-', '-'],
                             ylabel='t_peak', xlabel='Frequency',
                             title='t_peak on SF and ER')

#____________ data for the infection peak of the epidemic ____________

# under error
freq, peak_attack_ER = ER_epid_sim.epidemic_property_vs_removals(peak, attack, num_simulations)
_, peak_attack_SF, = SF_epid_sim.epidemic_property_vs_removals(peak, attack, num_simulations)

# under attack
freq, peak_error_ER = ER_epid_sim.epidemic_property_vs_removals(peak, error, num_simulations)
_, peak_error_SF = SF_epid_sim.epidemic_property_vs_removals(peak, error, num_simulations)

fig, ax = plot_multiple_data(x_data = [freq, freq, freq, freq], 
                             y_data = [peak_error_ER, peak_attack_ER, peak_error_SF, peak_attack_SF],  
                             labels=['error on ER', 'attack on ER', 'error on SF', 'attack on SF'],
                             colors=['blue', 'red', 'blue', 'red'],
                             markers=['o', 'o', 's', 's'],
                             linestyles=['--', '--', '-', '-'],
                             ylabel='Peak', xlabel='Frequency',
                             title='Infection Peak on SF and ER')

#____________ data for the total fraction of infected at the end of the epidemic ____________

# under error
freq, infected_attack_ER = ER_epid_sim.epidemic_property_vs_removals(total_infected, attack, num_simulations)
_, infected_attack_SF, = SF_epid_sim.epidemic_property_vs_removals(total_infected, attack, num_simulations)

# under attack
freq, infected_error_ER = ER_epid_sim.epidemic_property_vs_removals(total_infected, error, num_simulations)
_, infected_error_SF = SF_epid_sim.epidemic_property_vs_removals(total_infected, error, num_simulations)


fig, ax = plot_multiple_data(x_data = [freq, freq, freq, freq], 
                             y_data = [infected_error_ER, infected_attack_ER, infected_error_SF, infected_attack_SF],  
                             labels=['error on ER', 'attack on ER', 'error on SF', 'attack on SF'],
                             colors=['blue', 'red', 'blue', 'red'],
                             markers=['o', 'o', 's', 's'],
                             linestyles=['--', '--', '-', '-'],
                             ylabel='Fraction of total infected cases', xlabel='Frequency',
                             title='Infected Cases on SF and ER')