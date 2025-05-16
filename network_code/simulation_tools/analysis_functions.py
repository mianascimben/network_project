'''
    This file contains different functions useful for the analysis of network 
    connectivity and epidemic features. 
    
    > GRAPH FEATURES: includes functions to calculate the connectivity 
        of networks. They can be use alone or as argument of the function 
        'ToleranceSimulation.graph_property_vs_removals()' to study
        how network features behave when subjected to node removals (error or attack)
    > EPIDEMIC FRATURES: contains the functions used to analyze epidemic features.
        They can be use alone or as argument of the function 
        'EpidemicToleranceSimulation.epidemic_property_vs_removals()' to study
        how epidemic features behaves when subjected to node removals (error or attack)
    > ANALYSIS FUNCTIONS: group of functions to get the data of a function in 
        GRAPH or EPIDEMIC FEATURE while the network undergoes errors/attacks. 
        
        
    
'''

import networkx as nx
import numpy as np
import pickle 
from simulation_tools.remotion_functions import error, attack 

#-------------------------------GRAPH FEATURES---------------------------------

def diameter(G):
    '''
    Calculate the average shortest path length (also known as the diameter) 
    of the graph 'G'.

    Parameters
    ----------
    G : networkx.classes.graph.Graph
        The input graph for which the diameter is calculated.

    Returns
    -------
    float
        The diameter of the graph 'G'.

    Examples
    --------
    >>> G = nx.erdos_renyi_graph(100, 0.05)
    >>> diameter = calculate_diameter(G)
    >>> print(diameter)
    2.8

    Notes
    -----
    The function works with both directed and undirected graphs and even with 
    not connected graphs. 
    The term 'diameter' is used here to refer to the average shortest path 
    length. In graph theory, the diameter is often defined as the longest 
    shortest path between any two nodes in the graph. However, in the context 
    of this function, it refers to the average shortest path length.
    The average shortest path length is a measure of the efficiency of 
    information flow in the graph, representing the average distance between 
    all pairs of nodes.
    '''
    
    # The cases of directed and undirected graphs need different definition
    # of 'connected' and 'strongly connected'.
    if G.is_directed(): 
        if nx.is_strongly_connected(G):
            diameter = nx.average_shortest_path_length(G)  
        else : 
            # nx.average_shortest_path_length(G) gives error if isolated points
            # are met. To avoid this, it is preferred to store 
            # the shortest path length among all pairs of nodes 
            # and then average it. This method works even with isolated points. 
            shortest_paths = nx.shortest_path_length(G)
            
            # Extract path lengths into a list, skipping paths of length 
            # 0 (because irrilevant)
            shortest_path_list = [
                length for node, paths in shortest_paths
                for length in paths.values() if length > 0
                ]

            shortest_path_list = np.array(shortest_path_list, dtype=np.int32)
            
            diameter = np.mean(shortest_path_list)
            
    else : # undirected case   
        if nx.is_connected(G):
            diameter = nx.average_shortest_path_length(G) 
        
        else:    
            shortest_paths = nx.shortest_path_length(G)
            
            shortest_path_list = [
                length for node, paths in shortest_paths
                for length in paths.values() if length > 0
                ]
            
            if len(shortest_path_list) == 0: 
                diameter = 0
                
            else:
                shortest_path_list = np.array(shortest_path_list, dtype=np.int32)
        
                diameter = np.mean(shortest_path_list)
    return diameter
  
def largest_connected_component_size(G):
    '''
    Calculates the size of the largest connected component in the network. 
    
    The size is the total number of nodes the largest component is composed of.
    
    Parameters
    ----------
    G : networkx.classes.graph.Graph
        The input graph.

    Returns
    -------
    largest_cc_size : int
        The size of the largest connected component in the network normalised 
        for the total number of nodes.
        
    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> nx.add_path(G, [10, 11, 12])
    >>> largest_connected_component_size(G)
    4
    
    Notes
    -----
    In graph theory, the way components are calculated are different for 
    undirected and directed graph.
    In the first type of netwroks a component is a subgraph of connected vertices 
    that are not connected to any node of other subgraphs (isolated), while in directed
    graph the components divide in two definitions: strongly or weakly 
    connected components.
    
    This function works with weakly connected components as they are isolated 
    subgraphs like in the connected components of undirected graphs.
    
    A component is said strongly connected if there exist a direct path from 
    u to v and a directed path from v to u for each couple of verteces (u,v). 
    Note that this type of subgraphs can still communicate with other 
    subgraphs, if all the edges between them go from one to the other and not 
    viceversa.
    On the other hand, a component is called weakly connected if replacing all 
    of its directed edges with undirected edges produces a connected 
    (undirected) component. 
    
    '''
    # divide the case of directed and undirected graphs because of the difference
    # in the definition of the connected components
    if G.is_directed() : 
        largest_cc = max(nx.weakly_connected_components(G), key=len)
        largest_cc_size = len(largest_cc)
    else : # undirected case
        largest_cc = max(nx.connected_components(G), key=len)
        largest_cc_size = len(largest_cc)
    return largest_cc_size/nx.number_of_nodes(G)

def average_size_connected_components(G):
    '''
    Calculate the average size among all the connected components of the network, 
    but the largest one. 
    
    Parameters
    ----------
    G : networkx.classes.graph.Graph
        The input graph.

    Returns
    -------
    average_size : numpy.float64
        The average size of all the connected components, but the largest one.
        
    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> nx.add_path(G, [10, 11, 12])
    >>> nx.add_path(G, [13])
    >>> average_size_connected_components(G)
    2
    
    '''
    # divide the case for directed and undirected graphs because of the difference
    # in the definition of the connected components 
    #(see docstring of 'largest_connected_component_size()')
    if G.is_directed() : 
        sizes = [len(c) for c in sorted(nx.weakly_connected_components(G), key=len)]
        # erase the biggest (the last one) because we are interested in the behaviour 
        # of all the other components
        sizes_without_the_biggest = sizes[:-1]
        average_size = np.mean(sizes_without_the_biggest)
    else :  # undirected case
        sizes = [len(c) for c in sorted(nx.connected_components(G), key=len)]
        sizes_without_the_biggest = sizes[:-1]
        if len(sizes_without_the_biggest) == 0: 
            average_size = 0
        else: average_size = np.mean(sizes_without_the_biggest)
    return average_size
    
    
#-------------------------------EPIDEMIC FEATURES------------------------------

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
    
# ------------------------------ANALYSIS FUNCTIONS-----------------------------


def generate_network(network_type, *kwargs):
    """
    Generates the type of network indicated.

    Parameters
    ----------
    network_type : str
        The type of network you want to generate.
        - "ER" -> Erdos-Renyi network
        - "SF" -> Scale-Free network
        - "airports" -> Global air traffic network
        
    **kwargs : dict 
        If the network_type is "ER" or "SF", then it will contain in the following order:
        - N: int
            number of nodes
        - p: float
            probability of connection

    Returns
    -------
    networkx.classes.graph.Graph

    """

    match network_type:
        case "ER":
            N = kwargs[0]
            p = kwargs[1]
            G = nx.erdos_renyi_graph(N, p, directed=False)
            return G
        case "SF":
            N = kwargs[0]
            p = kwargs[1]
            k = N * p  
            G = nx.barabasi_albert_graph(N, int(k/2))
            return G
        case "airports":
            with open('flight.gpickle', 'rb') as f:
                G = pickle.load(f)
            return G
        case _:
            print("Error: Type of network not supported.")
            
def connectivity_analysis(sim):
    '''
    Analyzes the diameter of a network under the increasing of node removals 
    due to errors and attacks.
    
    The analysis is performed
    separately for random errors and targeted attacks.
    
    Parameters
    ----------
    sim : ToleranceSimulation
        An instance of the ToleranceSimulation class, which manages node removal 
        and metric evaluation.
        
    Returns
    -------
    freq : np.ndarray
        Array of node removal frequencies (fractions of nodes removed from the network).

    results_error : list of float
        Values of the netwrok diameter computed at each removal frequency under 
        random errors.

    results_attack : list of float
        Values of the network diameter computed at each removal frequency under 
        targeted attacks.
    
    '''
    
    freq, results_error = sim.graph_property_vs_removals(diameter, error)
    _, results_attack = sim.graph_property_vs_removals(diameter, attack)
    
    return freq, results_error, results_attack
    
def fragmentation_analysis(sim):
    """
    Analyzes the fragmentation of a network under node removals due to errors 
    and attacks.

    The function computes two structural metrics over increasing fractions of 
    node removals:
    - The size of the largest connected component (S)
    - The average size of the remaining connected components (<s>)

    Both metrics are computed separately under random errors and targeted attacks.

    Parameters
    ----------
    sim : ToleranceSimulation
        An instance of the ToleranceSimulation class, which manages node removal 
        and metric evaluation.

    Returns
    -------
    freq : np.ndarray
        Array of node removal frequencies (i.e., fractions of removed nodes).

    S_error : list of float
        Size of the largest connected component at each removal frequency under 
        random errors.

    S_attack : list of float
        Size of the largest connected component at each removal frequency under 
        targeted attacks.

    s_error : list of float
        Average size of non-giant connected components at each removal frequency 
        under random errors.

    s_attack : list of float
        Average size of non-giant connected components at each removal frequency 
        under targeted attacks.
    """

    freq, S_error = sim.graph_property_vs_removals(largest_connected_component_size, error)
    _, S_attack = sim.graph_property_vs_removals(largest_connected_component_size, attack)

    # data for <s>
    _, s_error = sim.graph_property_vs_removals(average_size_connected_components, error)
    _, s_attack = sim.graph_property_vs_removals(average_size_connected_components, attack)

    return freq, S_error, S_attack, s_error, s_attack

def epidemic_feature_analysis(sim, feature, num_simulations = 100):
    """
    Analyzes how an epidemic feature evolves as nodes are progressively removed
    from the network due to errors or targeted attacks.

    The specified epidemic feature (e.g. duration, peak) is
    computed across a range of node removal fractions. The analysis is performed
    separately for random errors and targeted attacks.

    Parameters
    ----------
    sim : EpidemicToleranceSimulation
        An instance of the EpidemicToleranceSimulation class that handles
        epidemic spreading and tolerance analysis under node removals.

    feature : function
        A function that computes the epidemic metric of interest (e.g. total_infected,
        epidemic_duration, peak, t_peak) on simulation results.

    Returns
    -------
    freq : np.ndarray
        Array of node removal frequencies (fractions of nodes removed from the network).

    results_error : list of float
        Values of the epidemic metric computed at each removal frequency under random errors.

    results_attack : list of float
        Values of the epidemic metric computed at each removal frequency under targeted attacks.
    """
    
    freq, results_error = sim.epidemic_property_vs_removals(feature, error, num_simulations)
    _, results_attack = sim.epidemic_property_vs_removals(feature, attack, num_simulations)
    
    return freq, results_error, results_attack