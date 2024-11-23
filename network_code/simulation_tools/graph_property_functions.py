'''

This scripts includes functions to calculate some properties of networks.
They can be use alone or as argument of the function 
ToleranceSimulation.graph_property_vs_removals() to study
how network features behave when subjected to node removals (error or attack)

'''

import networkx as nx
import numpy as np

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
    
    
