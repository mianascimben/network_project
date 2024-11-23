'''

This script aims to visualize how the average degree <k> of a network changes
by increasing the fraction of node removals it is subjected to.
To get <k>, the following steps are followed:
    The network gets errors/attacks
    Its degree pdf is analysed 
    <k> is extracet from the degree pdf
    
'''
import numpy as np
import networkx as nx
import random 
from simulation_tools.tolerance_simulation import GetRemotionFrequencies
from simulation_tools.remotion_functions import attack, error
from simulation_tools.pdf_functions import degree_pdf
from simulation_tools.plot_functions import plot_multiple_data

# netwok constants
N = 10   # number of nodes
p = 0.4  # probability of connection
k = N*p    # starting average degree

# for reproducibility
seed = 102
random.seed(seed)
np.random.seed(seed)

# creation of the artificial netwotyperks
erdos_renyi_net = nx.erdos_renyi_graph(N, p, directed = False)

freq = GetRemotionFrequencies(erdos_renyi_net, 0.9,15).frequencies_cleaned

# lists to save <k> for errors and attacks respectively
k_e = []
k_a = []

# get <k> under increasing errors and attacks
for i in freq:
    ER_error = error(erdos_renyi_net, int(N*i))
    ER_attack = attack(erdos_renyi_net, int(N*i))

    degree_e, pdf_e = degree_pdf(ER_error)
    degree_a, pdf_a = degree_pdf(ER_attack)

    k_e.append(np.sum(degree_e * pdf_e))
    k_a.append(np.sum(degree_a * pdf_a))
    
fig, ax = plot_multiple_data(x_data = [freq, freq], 
                             y_data = [k_e, k_a],  
                             labels=['<k> for error', '<k> for attack'],
                             colors=['blue', 'red'],
                             markers=['o', 'o'],
                             linestyles=['-', '-'],
                             ylabel='<k>', xlabel='Frequency',
                             title='ER: <k> v/s remotion frequency')
# line for <k> = 1 
ax.plot(freq, np.ones(len(freq)), linestyle='--', color='black')



