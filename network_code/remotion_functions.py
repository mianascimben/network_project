# -*- coding: utf-8 -*-

import random 

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
