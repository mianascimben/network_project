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
    
     
def FWHM(infection_evolution):
    '''
    Calculates the Full Width at Half Maximum (FWHM) of the infection evolution..

    Parameters:
    ----------
    infection_evolution : numpy.ndarray
        The array representing the infection evolution over time.

    Returns:
    -------
    fwhm : int
        The width of the infection evolution at half of its maximum value, in terms of time steps.
    
    Examples
    --------
    >>> infected = np.array([1, 5, 7, 5, 3])
    >>> FWHM(infected)
        2
    
    '''
    
    half_max = peak(infection_evolution)[0] / 2

    # Find where the data crosses half maximum
    indices = np.where(infection_evolution >= half_max)[0]
    
    # as the time-steps go on by 1, the x-axis corresponds to the indeces
    fwhm = indices[-1] - indices[0]
    
    return fwhm 

def peak(infection_evolution):
    '''
    Finds the peak value of the infection evolution and its corresponding time index.
    
    If the input is a 1D array, it finds the peak for that single simulation.
    If the input is a 2D array, it finds the average peak over the simulations (row).

    Parameters:
    ----------
    infection_matrix : numpy.ndarray
        A 1D array (single simulation) or 2D array (multiple simulations) where each row 
        represents a simulation and each column represents the infection evolution over time.

    Returns:
    -------
    peak : numpy.ndarray or float
        If the input is 1D, returns the peak value as a float.
        If the input is 2D, returns the average peak over the number of simulations.
    '''
    
    # If the input is a 1D array, convert it to a 2D matrix with a single row
    if infection_evolution.ndim == 1:
        infection_evolution = infection_evolution[np.newaxis, :]
    
    # Find the maximum value for each row (simulation)
    peaks = np.max(infection_evolution, axis=1)
    
    # If the original input was 1D, return a single value instead of an array
    # If it was 2D, return the average value over all the simulation
    if peaks.size == 1:
        return peaks[0]
    else: 
        return np.mean(peaks)

def t_peak(infection_evolution):
    '''
    Finds the time step at which the peak of the infection evolution occurs.

    If the input is a 1D array, it finds the time step for that single simulation.
    If the input is a 2D array, it finds the average time step over the simulations (rows) where the peak occurs.

    Parameters:
    ----------
    infection_evolution : numpy.ndarray
        A 1D array (single simulation) or a 2D array (multiple simulations) where each row 
        represents a simulation and each column represents the infection evolution over time.

    Returns:
    -------
    t_peak : numpy.ndarray or float
        If the input is 1D, returns the time step (index) where the peak occurs as an integer.
        If the input is 2D, returns the average time step across all simulations where the peak occurs.
    '''
    
    # If the input is a 1D array, convert it to a 2D matrix with a single row
    if infection_evolution.ndim == 1:
        infection_evolution = infection_evolution[np.newaxis, :]
    
    # Find the time step (index) of the maximum value for each row (simulation)
    indices_maximum = np.argmax(infection_evolution, axis=1)
    
    # If the original input was 1D, return a single index value
    if indices_maximum.size == 1:
        return indices_maximum[0]
    else:
        # For 2D input, return the average index where the peak occurs
        return np.mean(indices_maximum)

def epidemic_duration (infection_evolution):
    '''
    Calculates the duration of the epidemic based on the infection evolution.

    The duration is determined as the time between the first and last non-zero infection values.

    Calculates the duration of the epidemic for each simulation based on the infection evolution.

    If the input is a 1D array, it calculates the duration for that single simulation.
    If the input is a 2D array, it calculates the duration for each simulation (row) and return the 
    mean duration over the number of simulations.

    Parameters:
    ----------
    infection_evolution : numpy.ndarray
        A 1D array (single simulation) or 2D array (multiple simulations) where each row 
        represents a simulation and each column represents the infection evolution over time.

    Returns:
    -------
    duration : numpy.ndarray or int
        If the input is 1D, returns the duration as an integer.
        If the input is 2D, returns the average duration over all the simulations.
        If an epidemic never started, the duration will be 0.
    '''
    
    # If the input is a 1D array, convert it to a 2D matrix with a single row
    # This allows the same code to compute the duration for both 1D arrays and 
    # 2D matrices.
    if infection_evolution.ndim == 1:
        infection_evolution = infection_evolution[np.newaxis, :]
    
    durations = np.count_nonzero(infection_evolution, axis=1)
    
    # If the original input was 1D, return a single value instead of an array
    # If it was 2D, return the average value over all the simulation
    if durations.size == 1:
        return  durations[0]
    else: 
        return np.mean(durations)
    


def total_infected_percentage(infection_evolution, recovery_evolution):
    ''' 
    Calculates the total percentage of nodes that have been infected during the 
    epidemic, considering both the infected and recovered nodes.

    This function works with results obtained from the SIR model, as it considers
    the sum of the values of recovered and infected nodes at the end of the epidemic.

    Parameters
    ----------
    infection_evolution : numpy.ndarray
        A 1D array (single simulation) or 2D array (multiple simulations) representing 
        the percentage of infected nodes over time. 
        The first output of the function 'evolution_epidemy_SIR()'.
        
    recovery_evolution : numpy.ndarray
        A 1D array (single simulation) or 2D array (multiple simulations) representing 
        the percentage of recovered nodes over time. 
        The second output of the function 'evolution_epidemy_SIR()'.
        
    Returns
    -------
    numpy.float64
        The average percentage of nodes that have been infected during the epidemic 
        across all simulations (or just the percentage for a single simulation).
    
    Examples
    --------
    >>> infected = np.array([0, 20, 50, 30, 10])
    >>> recovered = np.array([0, 10, 20, 50, 90])
    >>> total_infected_percentage(infected, recovered)
    1.0
    
    >>> infected = np.array([[0, 20, 50, 40, 10], [0, 15, 35, 40, 20]])
    >>> recovered = np.array([[0, 10, 20, 30, 40], [0, 5, 30, 40, 80]])
    >>> total_infected_percentage(infected, recovered)
    0.75
    '''
    # If the input is a 1D array, convert it to a 2D matrix with a single row
    # This allows the same code to compute the duration for both 1D arrays and 
    # 2D matrices.
    if infection_evolution.ndim == 1 and recovery_evolution.ndim == 1:
        infection_evolution = infection_evolution[np.newaxis, :]
        recovery_evolution = recovery_evolution[np.newaxis, :]
        
    totals = infection_evolution[:,-1] + recovery_evolution[:,-1]
    return  np.mean(totals)
    
