import networkx as nx
import numpy as np
from scipy.optimize import curve_fit

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

def get_diameter(G):
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
        The size of the largest connected component in the network normalised for the total number of nodes.
        
    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> nx.add_path(G, [10, 11, 12])
    >>> largest_connected_component_size(G)
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
    # in the definition of the connected components
    if G.is_directed() : 
        largest_cc = max(nx.weakly_connected_components(G), key=len)
        largest_cc_size = len(largest_cc)
    else :
        largest_cc = max(nx.connected_components(G), key=len)
        largest_cc_size = len(largest_cc)
    return largest_cc_size/nx.number_of_nodes(G)

def average_size_connected_components(G):
    '''
    Calculate the average size among all the connected components of the network, but 
    the largest one. 
    
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
    # divided the case of directed and undirected graphs because of the difference
    # in the definition of the connected components
    if G.is_directed() : 
        sizes = [len(c) for c in sorted(nx.weakly_connected_components(G), key=len)]
        # erase the biggest (the last one) because we are interested in the behaviour 
        # of all the other components
        sizes_without_the_biggest = sizes[:-1]
        average_size = np.mean(sizes_without_the_biggest)
    else :
        sizes = [len(c) for c in sorted(nx.connected_components(G), key=len)]
        sizes_without_the_biggest = sizes[:-1]
        if len(sizes_without_the_biggest) == 0: 
            average_size = 0
        else: average_size = np.mean(sizes_without_the_biggest)
    return average_size
    
    
