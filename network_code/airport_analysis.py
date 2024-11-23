'''

This script perfoms simulations of errors and attacks on the air traffic 
network. For each fraction of node removals the 'diameter', the 
'largest_connected_component_size' and the 'average_size_connected_components' 
are calculated and plotted w.r.t. the removal frequencies. 
Then 'num_simulations' epidemics are runned over the same network after having 
been subjected to an increasing fraction of node removals. For each simulation some 
epidemic properties are calculated, averaged over all the simulations and 
finally displayed on a plot w.r.t.the removal frequencies.  

'''


import pickle
import random 
from simulation_tools.graph_property_functions import diameter, largest_connected_component_size, average_size_connected_components
from simulation_tools.tolerance_simulation import ToleranceSimulation, EpidemicToleranceSimulation
from simulation_tools.epidemic_functions import *
from simulation_tools.remotion_functions import error, attack
from simulation_tools.plot_functions import plot_multiple_data

# Download the dataset for the airports
with open('flight.gpickle', 'rb') as f:
    G = pickle.load(f)

air_traffic_net = G

# for reproducibility
seed = 102
random.seed(seed)
np.random.seed(seed)

# epidemic constants
mu = 0.2         # infection prob
nu = 0.05        # recovery prob
duration =50     # duration of the simulation
infected_t0 = 1  # number of infected nodes at the fist time step

num_simulations = 100  # Number of simulations to run
num_points = 15

# graph features analysis
tol_sim = ToleranceSimulation(air_traffic_net, 0.5)

# data for the diameter
freq, d_error = tol_sim.graph_property_vs_removals(diameter, error)
_, d_attack = tol_sim.graph_property_vs_removals(diameter, attack)

fig, ax = plot_multiple_data(x_data = [freq, freq], 
                             y_data = [d_error, d_attack],  
                             labels=['error', 'attack'],
                             colors=['blue', 'red'],
                             markers=['o', 'o'],
                             linestyles=['-', '-'],
                             ylabel='Diameter', xlabel='Frequency',
                             title='Diameter on Air Traffic')
# data for S
freq, S_error = tol_sim.graph_property_vs_removals(largest_connected_component_size, error)
_, S_attack = tol_sim.graph_property_vs_removals(largest_connected_component_size, attack)

# data for <s>
freq, s_error = tol_sim.graph_property_vs_removals(average_size_connected_components, error)
_, s_attack = tol_sim.graph_property_vs_removals(average_size_connected_components, attack)

fig, ax = plot_multiple_data(x_data = [freq, freq, freq, freq], 
                             y_data = [S_error, S_attack, s_error, s_attack],  
                             labels=['S vs error', 'S vs attack', '<s> vs error', '<s> vs attack'],
                             colors=['blue', 'red', 'blue', 'red'],
                             markers=['o', 'o', 's', 's'],
                             linestyles=['--', '--', '-', '-'],
                             ylabel='S, <s>', xlabel='Frequency',
                             title='Air Traffic: S and <s>')

# epidemic simulation 
epi_sim = EpidemicToleranceSimulation(air_traffic_net, mu, nu, duration, infected_t0, 0.5, num_points)


# data for the total infected
freq2, infected_error = epi_sim.epidemic_property_vs_removals(total_infected, error, num_simulations)
_, infected_attack = epi_sim.epidemic_property_vs_removals(total_infected, attack, num_simulations)

fig, ax = plot_multiple_data(x_data = [freq2, freq2], 
                             y_data = [infected_error, infected_attack],  
                             labels=['error', 'attack'],
                             colors=['blue', 'red'],
                             markers=['o', 'o'],
                             linestyles=['-', '-'],
                             ylabel='Fraction of total infected cases', xlabel='Frequency',
                             title='Infected Cases on Air Traffic')

# data for the epidemic duration
freq2, duration_error = epi_sim.epidemic_property_vs_removals(epidemic_duration, error, num_simulations)
_, duration_attack = epi_sim.epidemic_property_vs_removals(epidemic_duration, attack, num_simulations)

fig, ax = plot_multiple_data(x_data = [freq2, freq2], 
                             y_data = [duration_error, duration_attack],  
                             labels=['error', 'attack'],
                             colors=['blue', 'red'],
                             markers=['o', 'o'],
                             linestyles=['-', '-'],
                             ylabel='Duration', xlabel='Frequency',
                             title='Epidemic Duration on Air Traffic')

# data for the peak value 
freq2, peak_error = epi_sim.epidemic_property_vs_removals(peak, error, num_simulations)
_, peak_attack = epi_sim.epidemic_property_vs_removals(peak, attack, num_simulations)

fig, ax = plot_multiple_data(x_data = [freq2, freq2], 
                             y_data = [peak_error, peak_attack],  
                             labels=['error', 'attack'],
                             colors=['blue', 'red'],
                             markers=['o', 'o'],
                             linestyles=['-', '-'],
                             ylabel='Infection Peak', xlabel='Frequency',
                             title='Infection Peak on Air Traffic')

# data for the t_peak
freq2, t_peak_error = epi_sim.epidemic_property_vs_removals(t_peak, error, num_simulations)
_, t_peak_attack = epi_sim.epidemic_property_vs_removals(t_peak, attack, num_simulations)

fig, ax = plot_multiple_data(x_data = [freq2, freq2], 
                             y_data = [t_peak_error, t_peak_attack],  
                             labels=['error', 'attack'],
                             colors=['blue', 'red'],
                             markers=['o', 'o'],
                             linestyles=['-', '-'],
                             ylabel='t_peak', xlabel='Frequency',
                             title='t_peak on Air Traffic')