'''
    This scripts contains the tests for the functions in 'remotion_functions'
'''

import pytest
import networkx as nx
import random as rn

from network_code.remotion_functions import attack, error
    
@pytest.fixture
def graph():
    return nx.erdos_renyi_graph(100,0.05)

def test_copy_graph_attack(graph):
    ''' This function check that the 'attack' works on a copy of the 
    input graph
    
    GIVEN: a valid input graph
    WHEN: the attack function is applied on the input graph, whithout performing
        any attack
    THEN: it returns an isomorphic graph, different from the input one; 
        
    NOTES:
    -----
    Two graphs are isomorphic is they have the same structure in terms of nodes 
    and archs between them
    If the graph G2 is a copy of G1, then the operation 'G1 is G2' returns False
    '''
    graph_copy = attack(graph,0)
    not_equal = graph_copy is not graph
    isomorphic =  nx.is_isomorphic(graph_copy, graph)
    assert not_equal and isomorphic
    
def test_copy_graph_error(graph):
    ''' This function check that the 'error' works on a copy of the 
    input graph
    
    GIVEN: a valid input graph
    WHEN: the attack function is applied on the input graph, whithout performing
        any error
    THEN: it returns an isomorphic graph, different from the input one; 
        
    NOTES:
    -----
    Two graphs are isomorphic is they have the same structure in terms of nodes 
    and archs between them
    If the graph G2 is a copy of G1, then the operation 'G1 is G2' returns False
    '''
    graph_copy = error(graph,0) 
    not_equal = graph_copy is not graph
    isomorphic =  nx.is_isomorphic(graph_copy, graph)
    assert not_equal and isomorphic
    
def test_random_pick_error(graph):
    ''' This function tests that the strategy for performing errors is random 
    
    GIVEN: a valid input graph and a seed to control randomness
    WHEN: the 'error' function is applied on the input graph performing a certain
        number of errors
    THEN: the nodes randomly chosen to be removed are always the same 
    '''
    rn.seed(70)
    G_error = error(graph, 5)
    removed_nodes = graph.nodes() - G_error.nodes()
    assert removed_nodes == {15, 37, 57, 58, 89}
    
def test_strategy_pick_attack(graph):
    ''' This function tests the strategy for performing attacks 
    
    GIVEN: a valid input graph
    WHEN: the 'attack' function is applied on the input graph performing one
        attack
    THEN: the node removed corresponds to the node with the highest degree 
    
    NOTES:
    -----
    By increasing the number of attacks you would rise an error as the function
    removed_nodes.pop() only works if the set 'removed_nodes' containes only 1 
    element
    '''
    G_attack = attack(graph, 1)
    degrees = dict(graph.degree())
    most_connected_node = max(degrees, key=degrees.get)
    removed_nodes = graph.nodes() - G_attack.nodes()
    assert removed_nodes.pop() == most_connected_node

def test_number_errors(graph):
    ''' This functions tests whether the number of eliminated nodes is equal 
    to the 'num_errors' passed into the function 'error(G, num_errors)'
    
    GIVEN: a valid input graph and a random value for 'num_errors' 
    WHEN: the 'error' function is applied on the input graph 
    THEN: the number of nodes removed must be equal to 'num_errors'
    '''
    num_errors = rn.choice(range(0,101))
    G_error = error(graph, num_errors)
    num_removed_nodes = graph.number_of_nodes() - G_error.number_of_nodes()
    assert num_removed_nodes == num_errors
    
def test_number_attacks(graph):
    ''' This functions tests whether the number of eliminated nodes is equal 
    to the 'num_attacks' passed into the function 'attack(G, num_attacks)'
    
    GIVEN: a valid input graph and a random value for 'num_attacks' 
    WHEN: the 'attack' function is applied on the input graph 
    THEN: the number of nodes removed must be equal to 'num_attacks'
    '''
    num_attacks = rn.choice(range(0,101))
    G_attack = attack(graph, num_attacks)
    num_removed_nodes = graph.number_of_nodes() - G_attack.number_of_nodes()
    assert num_removed_nodes == num_attacks
    ''' This functions tests whether the number of eliminated nodes is equal 
    to the 'num_errors' passed into the function 'error(G, num_errors)'
    
    GIVEN: a valid input graph and a random value for 'num_errors' 
    WHEN: the 'error' function is applied on the input graph 
    THEN: the number of nodes removed must be equal to 'num_errors'
    '''
    num_errors = rn.choice(range(0,101))
    G_error = error(graph, num_errors)
    num_removed_nodes = graph.number_of_nodes() - G_error.number_of_nodes()
    assert num_removed_nodes == num_errors
