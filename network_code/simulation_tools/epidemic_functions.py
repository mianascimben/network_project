"""

This file contains the functions used to analyze epidemic features.
They can be use alone or as argument of the function 
'EpidemicToleranceSimulation.epidemic_property_vs_removals()' to study
how epidemic features behaves when subjected to node removals (error or attack)

"""
import numpy as np

def peak(infection_evolution):
    '''
    Finds the peak value of the infection evolution.
    
    If the input is a 1D array, it finds the peak for that single simulation.
    If the input is a 2D array, where each row corresponds to a single simulation,
    it finds the average peak over the simulations (rows).

    Parameters:
    ----------
    infection_matrix : numpy.ndarray
        A 1D array (single simulation) or 2D array (multiple simulations) where 
        each row represents a simulation and each column represents the infection 
        evolution over time.

    Returns:
    -------
    peak : numpy.float64 or numpy.int32
        If the input is 1D, returns the peak value as a float.
        If the input is 2D, returns the average peak over the number of simulations.
    
    Examples:
    --------
    >>> infected = np.array([0, 20, 50, 30, 10])
    >>> peak(infected)
    >>> 50
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
    If the input is a 2D array, where each row corresponds to a single simulation, 
    it finds the average time step over the simulations (rows) where the peak occurs.

    Parameters:
    ----------
    infection_evolution : numpy.ndarray
        A 1D array (single simulation) or a 2D array (multiple simulations) where 
        each row represents a simulation and each column represents the infection 
        evolution over time.

    Returns:
    -------
    t_peak : numpy.float64 or numpy.int64
        If the input is 1D, returns the time step (index) where the peak occurs 
        as an integer.
        If the input is 2D, returns the average time step across all simulations 
        where the peak occurs.
        
    Examples:
    --------
    >>> infected = np.array([0, 20, 50, 30, 10])
    >>> t_peak(infected)
    >>> 2
    '''
    
    # If the input is a 1D array, convert it to a 2D matrix with a single row
    if infection_evolution.ndim == 1:
        infection_evolution = infection_evolution[np.newaxis, :]
    
    # Find the time step (index) of the maximum value for each row (simulation)
    indices_maximum = np.argmax(infection_evolution, axis=1)
    
    # If the original input was 1D, return a single index value
    # If it 2D matrix, return the average index where the peak occurs over all simulations
    if indices_maximum.size == 1:
        return indices_maximum[0]
    else:
        return np.mean(indices_maximum)

def epidemic_duration (infection_evolution):
    '''
    Calculates the duration of the epidemic based on the infection evolution.

    The duration is determined as the time between the first and last non-zero 
    infection values.

    If the input is a 1D array, it calculates the duration for that single simulation.
    If the input is a 2D array, where each row corresponds to a single simulation,
    it calculates the duration for each simulation (row) and then 
    return the mean duration over the number of simulations.

    Parameters:
    ----------
    infection_evolution : numpy.ndarray
        A 1D array (single simulation) or 2D array (multiple simulations) where
        each row represents a simulation and each column represents the 
        infection evolution over time.

    Returns:
    -------
    duration : numpy.float64 or numpy.int64
        If the input is 1D, returns the duration as an integer.
        If the input is 2D, returns the average duration over all the simulations.
        If an epidemic never started, the duration will be 0.
        
    Examples:
    --------
    >>> infected = np.array([[0, 20, 50, 30, 10],
                             [0, 15, 35, 40, 0],
                             [10, 30, 70, 40, 50]])
    >>> epidemic_duration(infected)
    >>> 4.0
        
    Notes: 
    -----
    According to the 'SIR model', once the epidemic ends it cannot restars 
    spontaneously. So the end of the epidemic is reached by the absence of 
    infected cases.
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
    


def total_infected(infection_evolution, recovery_evolution):
    ''' 
    Calculates the total number of nodes that have been infected during the 
    epidemic, considering both the infected and recovered nodes.

    This function works with results obtained from the SIR model, as it considers
    the sum of the values of recovered and infected nodes at the end of the epidemic.

    Parameters
    ----------
    infection_evolution : numpy.ndarray
        A 1D array (single simulation) or 2D array (multiple simulations) representing 
        the number or the fraction of infected nodes over time. 
        
    recovery_evolution : numpy.ndarray
        A 1D array (single simulation) or 2D array (multiple simulations) representing 
        the number or the fraction of recovered nodes over time. 
    
    Returns
    -------
    numpy.float64 or numpy.int64
        The average number of nodes that have been infected during the epidemic 
        across all simulations (or just the number for a single simulation in 1D case).
    
    Examples
    --------
    >>> infected = np.array([0, 20, 50, 30, 10])
    >>> recovered = np.array([0, 10, 20, 50, 90])
    >>> total_infected(infected, recovered)
    100
    
    >>> infected = np.array([[0, 20, 50, 40, 10], [0, 15, 35, 40, 20]])
    >>> recovered = np.array([[0, 10, 20, 30, 40], [0, 5, 30, 40, 80]])
    >>> total_infected(infected, recovered)
    75.0
    '''
    
    # If the input is a 1D array, convert it to a 2D matrix with a single row
    # This allows the same code to compute the duration for both 1D arrays and 
    # 2D matrices.
    if infection_evolution.ndim == 1 and recovery_evolution.ndim == 1:
        infection_evolution = infection_evolution[np.newaxis, :]
        recovery_evolution = recovery_evolution[np.newaxis, :]
        
    totals = infection_evolution[:,-1] + recovery_evolution[:,-1]
    if totals.size == 1:
        return  totals[0]
    else: 
        return np.mean(totals)
    
