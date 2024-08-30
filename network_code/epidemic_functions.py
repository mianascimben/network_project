# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 10:33:18 2024

@author: mima
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


# def evolution_epidemy_SIS(G, starting_state, p_t, p_r, duration, plot_spread = False):
    
#     state = np.array(starting_state) #save the node
    
#     if plot_spread:
#         pos = nx.kamada_kawai_layout(G)  # fixed layout for the graph
#         node_colors = ['skyblue' if not starting_state[node] else 'red' for node in G.nodes()]
#         nx.draw(G, pos, with_labels=True, node_color=node_colors)
#         plt.title("Time = 0, SIS model")
#         plt.show() 
        
#     infection_rate = []
#     for i in range(1, duration + 1):
         
#         infected_state = infection_with_for(G, state, p_t)
    
#         recovered_state = recovery(state, infected_state, p_r)
        
#         infection_rate.append(recovered_state.mean())
        
#         state = recovered_state
#         if plot_spread:
#             node_colors = ['skyblue' if not recovered_state[node] else 'red' for node in G.nodes()]
#             nx.draw(G, pos, with_labels=True, node_color=node_colors)
#             plt.title(f"Time = {i}")
#             plt.show()
            
#     return np.array(infection_rate)
    
     
def FWHM(infection_function):
    '''
    Calculates the Full Width at Half Maximum (FWHM) of the infection function..

    Parameters:
    ----------
    infection_function : numpy.ndarray
        The array representing the infection function over time.

    Returns:
    -------
    fwhm : int
        The width of the infection function at half of its maximum value, in terms of time steps.
    
    Examples
    --------
    >>> infected = np.array([1, 5, 7, 5, 3])
    >>> FWHM(infected)
        2
    
    '''
    
    half_max = peak(infection_function)[0] / 2

    # Find where the data crosses half maximum
    indices = np.where(infection_function >= half_max)[0]
    
    # as the time-steps go on by 1, the x-axis corresponds to the indeces
    fwhm = indices[-1] - indices[0]
    
    return fwhm 

def peak(infection_function):
    '''
    Finds the peak value of the infection function and its corresponding index.

    Parameters:
    ----------
    infection_function : numpy.ndarray
        The array representing the infection function over time.

    Returns:
    -------
    maximum : float
        The maximum value of the infection function.
    index_maximum : numpy.ndarray
        The index (or indices) where the maximum value occurs.
        
    '''
    maximum = np.max(infection_function)
    index_maximum = np.where(infection_function == maximum)
    return maximum, index_maximum

def epidemic_duration (infection_function):
    '''
    Calculates the duration of the epidemic based on the infection function.

    The duration is determined as the time between the first and last non-zero infection values.

    Parameters:
    ----------
    infection_function : numpy.ndarray
        The array representing the infection function over time.

    Returns:
    -------
    duration : int or str
        The duration of the epidemic in terms of time steps. If the epidemic never started,
        returns the string "Epidemic never started".
        
    '''
    
    indices = np.where(infection_function > 0)[0]
    
    #check if there are indices or not
    if len(indices) > 1:
        duration = indices[-1] - indices[0] + 1 #it starts from zero, not from 1
    else: duration = "Epidemic never started"
        
    return duration

def half_life (infection_function):
    '''
    Calculates the half-life of the epidemic's growth and decay phases.

    The half-life is the time it takes for the infection function to reach half of its peak value 
    during the growth and decay phases.

    Parameters:
    ----------
    infection_function : numpy.ndarray
        The array representing the infection function over time.

    Returns:
    -------
    half_life_growth : int
        The time it takes for the infection function to grow from zero to half of its maximum value.
    half_life_decay : int
        The time it takes for the infection function to decay from its maximum value to half.

    Notes
    -----
    This function handle just functions that have these features:
        -just one global maximum
        -if local maxima are present, either their peak value is less than the half of the heighest peak
         or the function, between the local and the global maximum, is always above the global peak.  
    '''

    maximum, max_index = peak(infection_function)
    indices = np.where(infection_function >= maximum/2)[0]
    
    # cases to distinguish the presence or not of both the half-lifes  
    if len(indices) > 2: #we must take into account the max_index within indices array 
        half_life_growth = indices[0] - max_index
        half_life_decay = indices[-1] - max_index
    elif len(indices) == 2:
        if indices[0] == max_index:  #too sharp growth to be recorded
            half_life_growth = 0
            half_life_decay = indices 
        else:                        #too sharp decay to be recorded
            half_life_growth = indices
            half_life_decay = 0
    else: 
        half_life_growth = 0
        half_life_decay = 0
        print("There has been no epidemic")

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
    numpy.float64
        The percentage of nodes that have been infected during the epidemy
    
    '''
    
    return  infection_function[-1] + recovery_function[-1]
    
