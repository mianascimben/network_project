# -*- coding: utf-8 -*-
import pickle
import random 
from graph_property_functions import get_diameter, largest_connected_component_size, average_size_connected_components
from tolerance_simulation import ToleranceSimulation, EpidemicToleranceSimulation
from epidemic_functions import *
from remotion_functions import error, attack
from plot_functions import plot_of_two_data

# Download the dataset for the airports
with open('flight.gpickle', 'rb') as f:
    G = pickle.load(f)

air_traffic_net = G

# for reproducibility
seed = 102
random.seed(seed)
np.random.seed(seed)

# constants for epidemic simulation
p_t = 0.2
p_i = 0.05
duration =50
infected_t0 = 1

num_simulations = 100  # Number of simulations to run
num_points = 15

## graph feature analysis
tol_sim = ToleranceSimulation(air_traffic_net, 0.5)

# data for the diameter
freq, d_error = tol_sim.graph_property_vs_removals(get_diameter, error)
_, d_attack = tol_sim.graph_property_vs_removals(get_diameter, attack)

fig, ax = plot_of_two_data(freq, d_error, 'error', True, freq, d_attack, label2 = 'attack', ylabel='Diameter', xlabel='Frequency', title = 'Diameter v/s Frequency of removals')   

# data for S
freq, S_error = tol_sim.graph_property_vs_removals(largest_connected_component_size, error)
_, S_attack = tol_sim.graph_property_vs_removals(largest_connected_component_size, attack)

# data for <s>
freq, s_error = tol_sim.graph_property_vs_removals(average_size_connected_components, error)
_, s_attack = tol_sim.graph_property_vs_removals(average_size_connected_components, attack)

fig, ax = plot_of_two_data(freq, S_error, 'S v/s error', True, freq, S_attack, label2 = 'S v/s attack', ylabel='S', xlabel='Frequency', title = 'S, <s> v/s Frequency of removals')   
ax.plot(freq, s_error, label = '<s> v/s error', color='blue', marker='s')
ax.plot(freq, s_attack, label = '<s> v/s attack', color='red', marker='s')
ax.legend()


## epidemic simulation 
epi_sim = EpidemicToleranceSimulation(air_traffic_net, p_t, p_i, duration, infected_t0, 0.5, num_points)


# data for the total infected
freq2, infected_error = epi_sim.epidemic_property_vs_removals(total_infected_percentage, error, num_simulations)
_, infected_attack = epi_sim.epidemic_property_vs_removals(total_infected_percentage, attack, num_simulations)

fig, ax = plot_of_two_data(freq2, infected_error, 'error', True, freq2, infected_attack, label2 = 'attack', ylabel='Total infected', xlabel='Frequency', title = 'Total infected v/s Frequency of removals')   


# data for the epidemic duration
freq2, duration_error = epi_sim.epidemic_property_vs_removals(epidemic_duration, error, num_simulations)
_, duration_attack = epi_sim.epidemic_property_vs_removals(epidemic_duration, attack, num_simulations)

fig, ax = plot_of_two_data(freq2, duration_error, 'error', True, freq2, duration_attack, label2 = 'attack', ylabel='Epidemic duration', xlabel='Frequency', title = 'Epidemic duration v/s Frequency of removals')   


# data for the peak value 
freq2, peak_error = epi_sim.epidemic_property_vs_removals(peak, error, num_simulations)
_, peak_attack = epi_sim.epidemic_property_vs_removals(peak, attack, num_simulations)

fig, ax = plot_of_two_data(freq2, peak_error, 'error', True, freq2, peak_attack, label2 = 'attack', ylabel='Peak', xlabel='Frequency', title = 'Peak v/s Frequency of removals')   


# data for the t_peak
freq2, t_peak_error = epi_sim.epidemic_property_vs_removals(t_peak, error, num_simulations)
_, t_peak_attack = epi_sim.epidemic_property_vs_removals(t_peak, attack, num_simulations)

fig, ax = plot_of_two_data(freq2, t_peak_error, 'error', True, freq2, t_peak_attack, label2 = 'attack', ylabel='t_peak', xlabel='Frequency', title = 't_peak v/s Frequency of removals')   