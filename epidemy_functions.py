# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 10:33:18 2024

@author: mima
"""

import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt

#reproducibility
seed = 1
random.seed(seed)
np.random.seed(seed)

#G = nx.erdos_renyi_graph(1000, 0.4, False)
G = nx.barabasi_albert_graph(1000, 2)

# for SIR better 10^-2 
p_t = 0.07
p_r = 0.04
p_i = 0.04
duration = 500
# healthy
state = np.zeros(G.number_of_nodes())

# the first infected
index_infected = random.sample(range(G.number_of_nodes()),1)

state[index_infected] = 1

def evolution_epidemy_SIS(G, starting_state, p_t, p_r, duration, plot_spread = False):
    
    state = np.array(starting_state) #save the node
    
    if plot_spread:
        pos = nx.kamada_kawai_layout(G)  # fixed layout for the graph
        node_colors = ['skyblue' if not starting_state[node] else 'red' for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=node_colors)
        plt.title("Time = 0, SIS model")
        plt.show() 
        
    infection_rate = []
    for i in range(1, duration + 1):
         
        infected_state = infection_with_for(G, state, p_t)
    
        recovered_state = recovery(state, infected_state, p_r)
        
        infection_rate.append(recovered_state.mean())
        
        state = recovered_state
        if plot_spread:
            node_colors = ['skyblue' if not recovered_state[node] else 'red' for node in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_color=node_colors)
            plt.title(f"Time = {i}")
            plt.show()
            
    return np.array(infection_rate)

def evolution_epidemy_SIR(G, starting_state, p_t, p_i, duration, plot_spread = False):
    
    state = np.array(starting_state) #save the node
    
    if plot_spread:
        pos = nx.kamada_kawai_layout(G)  # fixed layout for the graph
        node_colors = ['red' if starting_state[node] == 1 else 'green' if starting_state[node] == -1 else 'skyblue' for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=node_colors)
        plt.title("Time = 0, SIR model")
        plt.show() 
        
    infection_rate = []
    immunized_rate = []
    for i in range(1, duration + 1):
        
        infected_state = infection_with_for(G, state, p_t)
    
        immunized_state = immunity(state, infected_state, p_i)
        
        infection_rate.append(np.mean(immunized_state == 1))
        immunized_rate.append(np.mean(immunized_state == -1))
        
        state = immunized_state
        if plot_spread:
            node_colors = ['red' if immunized_state[node] == 1 else 'green' if immunized_state[node] == -1 else 'skyblue' for node in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_color=node_colors)
            plt.title(f"Time = {i}")
            plt.show()
            
    return np.array(infection_rate), np.array(immunized_rate)

def recovery(starting_state, final_state, p_r):
    
    infected_nodes = np.where(starting_state == 1)
    recovery = np.random.binomial(1, p_r, len(infected_nodes[0])).astype(bool)
    recovered_nodes = infected_nodes[0][recovery]
    final_state[recovered_nodes] = 0
    return final_state
    
def infection_with_for(G, starting_state, p_t):
    
    state = np.array(starting_state)
    discordant_links = [(u, v) for u, v in G.edges() if state[u] + state[v] == 1]
    transmit = np.random.binomial(1, p_t, len(discordant_links))
        
    #Update the infection status
    for j, (u, v) in enumerate(discordant_links):
        if transmit[j]:
            state[u] = state[v] = 1 
    
    return state

def infection_without_for(G, starting_state, p_t):
    
     state = np.array(starting_state)
     u, v = np.array(G.edges()).T
     discordant_mask = state[u] != state[v]
     discordant_edges = np.where(discordant_mask)[0]
        
     transmissions = np.random.binomial(1, p_t, len(discordant_edges))
     edges_to_update = discordant_edges[transmissions == 1]

     state[u[edges_to_update]] = 1
     state[v[edges_to_update]] = 1
     
     return state

def immunity(starting_state, final_state, p_i):
    
    infected_nodes = np.where(starting_state == 1)
    immunity = np.random.binomial(1, p_i, len(infected_nodes[0])).astype(bool)
    immunized_nodes = infected_nodes[0][immunity]
    final_state[immunized_nodes] = -1
    return final_state
    #here I could erase the immunized nodes, in order to not change the code
    # in the infection functions. but in this case I cannot visualize them.
    '''def evolution_epidemy(G, initial_state, p_t, p_r, duration, plot_spread = False):
        
        if plot_spread:
            pos = nx.kamada_kawai_layout(G)  # fixed layout for the graph
            node_colors = ['skyblue' if not state[node] else 'red' for node in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_color=node_colors)
            plt.title("Time = 0")
            plt.show() 
            
        infection_rate = []
        for i in range(1, duration + 1):
            starting_state = np.array(initial_state) #save the node 
            
            infected_state = infection_with_for(G, starting_state, p_t)
        
            recovered_state = recovery(starting_state, infected_state, p_r)
            
            infection_rate.append(recovered_state.mean())
            
            if plot_spread:
                node_colors = ['red' if state[node] else 'skyblue' for node in G.nodes()]
                nx.draw(G, pos, with_labels=True, node_color=node_colors)
                plt.title(f"Time = {i}")
                plt.show()
                
        return infection_rate

    def recovery(starting_state, final_state, p_r):
        
        infected_nodes = np.where(starting_state == 1)
        recovery = np.random.binomial(1, p_r, len(infected_nodes[0])).astype(bool)
        recovered_nodes = infected_nodes[0][recovery]
        final_state[recovered_nodes] = 0
        return final_state
        
    def infection_with_for(G, initial_state, p_t):
        
        state = np.array(initial_state)
        discordant_links = [(u, v) for u, v in G.edges() if state[u] != state[v]]
        transmit = np.random.binomial(1, p_t, len(discordant_links))
            
        #Update the infection status
        for j, (u, v) in enumerate(discordant_links):
            if transmit[j]:
                state[u] = state[v] = 1 
        
        return state

    def infection_without_for(G, initial_state, p_t):
        
         state = np.array(initial_state)
         u, v = np.array(G.edges()).T
         discordant_mask = state[u] != state[v]
         discordant_edges = np.where(discordant_mask)[0]
            
         transmissions = np.random.binomial(1, p_t, len(discordant_edges))
         edges_to_update = discordant_edges[transmissions == 1]

         state[u[edges_to_update]] = 1
         state[v[edges_to_update]] = 1
         
         return state'''
     
def FWHM(function):
    # Calculate half maximum
    half_max = peak(function) / 2.0

    # Find where the data crosses half maximum
    indices = np.where(function >= half_max)[0]
    
    # as the time-steps go on by 1, the x-axis corresponds to the indeces
    fwhm = indices[-1] - indices[0]
    
    return fwhm 

def peak(function):
    
    return np.max(function)

def duration_epidemy (function, N, threshold = 0.05):
    
    threshold_population = N*threshold
    indices = np.where(function >= threshold_population)
    duration = indices[-1] - indices[0]
    
    return duration

def half_life (function):
    
    maximum = peak(function)
    max_index = np.where(funtion == maximum)
    indices = np.where(function >= maximum/2)[0]
    half_life_growth = indices[0] - max_index
    half_life_decay = indices[-1] - max_index
    
    return half_life_growth, half_life_decay 

def total_infected_percentage(infection_function, recovery_function):
    ''' 
    Calculate the total number of nodes that have been infected during the 
    epidemy. The value is expressed in percentage. 
    
    This funtion works for results obtained by SIR model, as it considers
    the sum between the value of the recovered nodes and the infected nodes 
    at the end of the epidemy. 
    
    
    Parameters
    ----------
    infection_function : numpy.ndarray
        Array with the percentage of infected nodes in time. 
        The first output of the function 'evolution_epidemy_SIR()'
        
    recovery_function : numpy.ndarray
        Array with the percentage of recovered nodes in time. 
        The second output of the function 'evolution_epidemy_SIR()'
    Returns
    -------
    
    '''
    
    return  infection_function[-1] + recovery_function[-1]
    
