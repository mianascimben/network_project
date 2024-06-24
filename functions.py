# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 16:44:08 2024

@author: mima
"""
import random 
import networkx as nx
import numpy as np
from scipy.optimize import curve_fit
import statistics as sts

def fit_data(f, x, y):
    '''
    Fits the given data using the provided model function.

    This function utilizes the `curve_fit` function from the `scipy.optimize` module
    to fit the provided model function `f` to the data points `x` and `y`. It returns
    the optimal parameters and the estimated covariance of the parameters.

    Parameters
    ----------
    f : callable
        The model function to fit. It should take the independent variable as the first argument
        and the parameters to fit as separate remaining arguments.
    x : array-like
        The independent variable.
    y : array-like
        The dependent data.

    Returns
    -------
    popt : array
        Optimal values for the parameters such that the sum of the squared residuals is minimized.
    pcov : 2-D array
        The estimated covariance of popt. The diagonals provide the variance of the parameter estimate.
        To compute one standard deviation errors on the parameters, use `np.sqrt(np.diag(pcov))`.

    Examples
    --------
    >>> def model(x, a, b):
    ...     return a * np.exp(b * x)
    >>> x = np.array([1, 2, 3, 4])
    >>> y = np.array([2.7, 7.4, 20.1, 55.6])
    >>> popt, pcov = fit_data(model, x, y)
    >>> print(popt)
    [1. 2.]
    '''
    
    popt, pcov = curve_fit(f, x, y)
    return popt, pcov

    
def exp_model(data, alpha, beta):
    '''
    Applies an exponential model to the input data.

    This function computes the value of the expression `alpha * data ** beta`,
    where `alpha` and `beta` are parameters of the model and `data` is the input.

    Parameters
    ----------
    data : numeric or array-like
        The input data to which the exponential model is applied. This can be a 
        single numeric value or an array-like structure (such as a list or numpy array)
        containing multiple numeric values.
    alpha : numeric
        The coefficient parameter of the exponential model. It scales the result of 
        the power transformation.
    beta : numeric
        The exponent parameter of the exponential model. It determines the power to 
        which each element in `data` is raised.

    Returns
    -------
    numeric or array-like
        The output of the exponential model, computed as `alpha * data ** beta`. If `data`
        is a single numeric value, the return will be a single numeric value. If `data`
        is array-like, the return will be an array-like structure of the same shape
        containing the computed values.
    '''
    return alpha * data ** beta
 
def frequency_network_degree(G):
    '''
    Provides the degree of the nodes of the input graph, 'G', counting 
    their normalized frequency.

    This function computes the degree of each node in the input graph `G` and 
    then calculates the normalized frequency of each unique degree.

    Parameters
    ----------
    G : networkx.classes.graph.Graph
        Input graph from the NetworkX library.

    Returns
    -------
    G_deg_unique : numpy.ndarray
        An array of unique degrees of the nodes in the input graph.
    normalized_freq : numpy.ndarray
        An array of normalized frequencies corresponding to each unique degree.
        
    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> degree, frequency = frequency_degree(G)
    >>> print(degree, frequency)
    [1 2] [0.5 0.5] 

    '''
    
    # get the degree from max to min and its frequence
    G_deg = sorted((d for n,d in G.degree()),reverse=True)
    G_deg_unique, frequency = np.unique(G_deg, return_counts = True)
    normalized_freq = frequency/(frequency.sum())
    
    return G_deg_unique, normalized_freq

def generate_frequencies(max_frequency, num_points):
    '''
    Generate a list of evenly spaced frequency values.

    This function generates a list of frequency values that are evenly spaced 
    between 0 and the specified maximum frequency. The number of values generated
    is specified by the 'num_points' parameter.

      Parameters
      ----------
      max_frequency : float
          The maximum frequency value. The generated frequencies will range 
          from 0 to 'max_frequency', inclusive.
          num_points : int
          The number of frequency values to generate. This determines the number 
          of evenly spaced points in the range.
          
      Returns
      -------
      numpy.ndarray
      An array of evenly spaced frequency values from 0 to 'max_frequency'.
          
      Examples
      --------
      >>> generate_frequencies(0.1, 5)
          array([0.  , 0.025, 0.05 , 0.075, 0.1  ])
          
      >>> generate_frequencies(1.0, 4)
          array([0.        , 0.33333333, 0.66666667, 1.        ])
    '''
    return np.linspace(0, max_frequency, num_points)

def calculate_diameter(G):
    '''
    Calculate the average shortest path length (also known as the diameter) 
    of the graph 'G'.

    This function computes the average shortest path length, often referred to 
    as the diameter, of the input graph 'G'. 

    Parameters
    ----------
    G : networkx.classes.graph.Graph
        The input graph for which the diameter is 
        calculated.

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
    The average shortest path length is a measure of the efficiency of information flow in the graph, 
    representing the average distance between all pairs of nodes.
    '''
    # divided the cases of directed and undirected graphs because of the difference
    # in the definition of connected and strongly connected.
    if G.is_directed(): 
        if nx.is_strongly_connected(G):
            diameter = nx.average_shortest_path_length(G)
        else : 
            # To avoid errors because of isolated points using nx.average_shortest_path_length(G)
            # it is preferred to store the shortest path length among all pairs of nodes 
            # and then average it. This method works even with isolated points. 
            shortest_paths = nx.shortest_path_length(G)
            
            # Extract path lengths into a flat list, skipping paths of length 0 as irrilevant
            shortest_path_list = [
                length for node, paths in shortest_paths
                for length in paths.values() if length > 0
                ]

            shortest_path_list = np.array(shortest_path_list, dtype=np.int32)
            
            diameter = sts.mean(shortest_path_list)
    else : # undirected case   
        if nx.is_connected(G):
            diameter = nx.average_shortest_path_length(G) 
        
        else:    
            shortest_paths = nx.shortest_path_length(G)
            
            shortest_path_list = [
                length for node, paths in shortest_paths
                for length in paths.values() if length > 0
                ]

            shortest_path_list = np.array(shortest_path_list, dtype=np.int32)
        
            diameter = sts.mean(shortest_path_list)
    return diameter

def attack(G, num_attacks = 1):
    '''
    Perform multiple attacks on the input graph 'G' by removing the most 
    connected nodes.

    This function simulates attacks on the graph 'G' by identifying and 
    removing the most connected nodes (nodes with the highest degree). The 
    function returns a copy of the input graph after the specified number of 
    nodes have been removed.

    Parameters
    ----------
    G : networkx.classes.graph.Graph
        The input graph from which the most connected nodes are to be removed.
    
    num_attacks : int, optional
        The number of most connected nodes to remove from the graph. The default 
        value is 1.
        
    Returns
    -------
    G_with_attacks : networkx.classes.graph.Graph
        A copy of the input graph after the specified number of most connected 
        nodes have been removed.

    Examples
    --------
    >>> G = nx.erdos_renyi_graph(100, 0.05)
    >>> G_after_attack = attack(G, 5)
    >>> print(G_after_attack.number_of_nodes())
    95

    Notes
    -----
    The function performs attacks by removing nodes with the highest degree 
    first. In case of ties (multiple nodes having the same degree), the nodes 
    are removed in arbitrary order.

    '''
    G_with_attacks = G.copy()
    
    degrees = dict(G_with_attacks.degree())
    top_n_nodes = sorted(degrees, key=degrees.get, reverse=True)[:num_attacks]
    
    G_with_attacks.remove_nodes_from(top_n_nodes)
    
    return G_with_attacks

def error(G, num_errors = 1):
    '''
    Perform multiple errors on a copy of the input graph 'G' by randomly 
    removing nodes.

    This function simulates errors on the graph 'G' by randomly removing a 
    specified number of nodes. It returns a copy of the input graph after 
    the nodes have been removed.

    Parameters
    ----------
    G : networkx.classes.graph.Graph
        The input graph from which edges are to be removed.
        
    num_errors : int, optional
        The number of nodes to remove from the graph. The default value is 1.
        
    Returns
    -------
    G_with_errors : networkx.classes.graph.Graph
        A copy of the input graph after the specified number of nodes have been 
        randomly removed.

    Examples
    --------
    >>> G = nx.erdos_renyi_graph(100, 0.05)
    >>> G_after_error = error(G, 5)
    >>> print(G_after_error.number_of_nodes())
    95, 5 fewer than the original number of nodes

    Notes
    -----
    The function performs errors by randomly selecting nodes from the graph and 
    removing them. This simulates random failures or disruptions in the network.
    '''
    
    G_with_errors = G.copy()
    
    nodes = list(G_with_errors.nodes())
    nodes_to_remove = random.sample(nodes, num_errors)
    
    G_with_errors.remove_nodes_from(nodes_to_remove)
    
    return G_with_errors

def diameter_vs_errors(G, max_frequency_error = 0.05, num_points = 20):
    '''
    Examine the impact of error frequency on the diameter of the input graph 'G'.

    This function generates new versions of the input graph 'G', each subjected
    to a different frequency of errors (random node removals). It then calculates 
    the diameter (average shortest path length) of each modified graph and returns 
    the data for further analysis or plotting.

    Parameters
    ----------
    G : networkx.classes.graph.Graph
        The input graph to be analyzed.
    max_frequency_error : float, optional
        A float between 0 and 1 that represents the maximum error frequency, 
        expressed as a fraction of the number of nodes in the graph. The default 
        value is 0.05.
    num_points : int, optional
        The number of different error frequencies to generate. The frequencies 
        are evenly spaced based on this number. The default value is 20.
    
    Returns
    -------
    frequencies : list of float
        A list of error frequencies applied to the graph. These values are 
        evenly spaced between 0 and the specified maximum frequency.
    diameters : list of float
        A list of diameters corresponding to each error frequency. The diameter 
        is the average shortest path length of the graph after applying the 
        specified frequency of errors.
    
    Examples
    --------
    >>> G = nx.erdos_renyi_graph(100, 0.05)
    >>> freq, diam = diameter_vs_errors(G, max_frequency_error=0.1, num_points=20)
    >>> print(freq)
    [0.0, 0.00526316, 0.01052632, ..., 0.1]
    >>> print(diam)
    [2.3, 2.5, 2.8, ..., 5.1]
    
    Notes
    -----
    The function assumes the existence of an `error` function that can apply a 
    specified number of errors to a graph, and a `calculate_diameter` function 
    that computes the average shortest path length of a graph.
    '''
    number_of_nodes = G.number_of_nodes()
    frequencies = generate_frequencies(max_frequency_error, num_points)
    num_errors = (frequencies * number_of_nodes).astype(int)

    # avoid the repetition of equal numbers in num_errors
    num_errors_cleaned = np.unique(num_errors)
    
    diameters = []
    for i in num_errors_cleaned:
        G_error = error(G, i)
        diameters.append(nx.average_shortest_path_length(G_error))
       
    return frequencies.tolist(), diameters

def diameter_vs_attacks(G, max_frequency_attack = 0.05, num_points = 20):
   '''
    Analyze the impact of attack frequency on the diameter of the input graph 'G'.

    This function generates new versions of the input graph 'G', each subjected 
    to a different frequency of attacks (removal of the most connected nodes). 
    It calculates the diameters (average shortest path lengths) of these graphs 
    and provides the data to be used as inputs in the `diameter_plot(x, y)` function.

    Parameters
    ----------
    G : networkx.classes.graph.Graph
        The input graph to be analyzed.
    max_frequency_attack : float, optional
        A number between 0 and 1 representing the maximum attack frequency, 
        expressed as a fraction of the total number of nodes in the graph. 
        The default value is 0.05.
    num_points : int, optional
        The number of different attack frequencies to generate. The frequencies 
        are evenly spaced based on this number. The default value is 20.

    Returns
    -------
    frequency_of_attack : list of float
        A list of attack frequencies applied to the graph. These can be used 
        as the x-axis values in the `diameter_plot(x, y)` function.
    diameters : list of float
        A list of diameters corresponding to each attack frequency. These 
        represent the average shortest path lengths of the graph after 
        being subjected to the specified frequencies of attacks. They can 
        be used as the y-axis values in the `diameter_plot(x, y)` function.

    Examples
    --------
    >>> G = nx.erdos_renyi_graph(100, 0.05)
    >>> frequencies, diameters = diameter_vs_attacks(G, max_frequency_attack=0.1, num_points=10)
    >>> print(frequencies)
    [0.0, 0.0111, 0.0222, ..., 0.1]
    >>> print(diameters)
    [2.5, 2.8, 3.1, ..., 5.2]

    Notes
    -----
    The function avoids the repetition of equal numbers in the list of 
    calculated attack frequencies to ensure unique attack scenarios.
    '''
    
   number_of_nodes = G.number_of_nodes()
   frequencies = generate_frequencies(max_frequency_attack, num_points)
   num_attacks = (frequencies * number_of_nodes).astype(int)

   # avoid the repetition of equal numbers in num_attacks
   num_attacks_cleaned = np.unique(num_attacks)
    
   diameters = []
   for i in num_attacks_cleaned:
       G_attack = attack(G, i)
       diameters.append(nx.average_shortest_path_length(G_attack))
       
   return frequencies.tolist(), diameters
   
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
        The size of the largest connected component in the network.
        
    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> nx.add_path(G, [10, 11, 12])
    >>> giant_component_size(G)
    4
    
    Notes
    -----
    In graph theory, the way components are calculated are different for undirected 
    and directed graph. In the first type of netwroks a component is a subgraph of connected 
    vertices that are not connected to any node of other subgraphs, while, in directed 
    graph, there are strongly or weakly connected components. A component is said 
    strongly connected if every vertex is reachable from every other vertex; these types 
    of subgraphs can still communicate each other if all the edges between them
    go from one to the other and not viceversa.
    On the other hand, weakly connected components are subgraph whose vertices are 
    totally ordered by reachability.
    This function works with weakly connected components as they are isolated subgraphs
    like in the connected components of undirected graphs.
    
    
    '''
    # divided the case of directed and undirected graphs because of the difference
    # in the definition of components
    if G.is_directed() : 
        largest_cc = max(nx.weakly_connected_components(G), key=len)
        largest_cc_size = len(largest_cc)
    else :
        largest_cc = max(nx.connected_components(G), key=len)
        largest_cc_size = len(largest_cc)
    return largest_cc_size