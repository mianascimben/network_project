import pytest
import random as rn
import networkx as nx
import numpy as np
from network_code.simulation import GetRemotionFrequencies


@pytest.fixture
def graph():
    G = nx.erdos_renyi_graph(100, 0.2)
    return G
    
def test_number_of_frequencies(graph):
    ''' This function checks the number of generated frequencies is never bigger
    than that specified in 'points'.
    
    GIVEN: an input graph  
    WHEN: an instance of the class 'GetRemotionFrequencies' is created
    THEN: check the length of the generated array is not bigger than 'points'
    '''
    points = rn.choice(range(0, 50))
    max_rate = rn.choice(range(0,1))
    
    freq = GetRemotionFrequencies(graph, max_rate, points)
    assert len(freq.frequencies_cleaned) <= points
    
def test_number_of_remotions(graph):
    ''' This function checks the length of the array 'num_removals_cleaned' 
    created by the functoin 'GetRemotionFrequencies.generate_frequencies()' is 
    never bigger than that specified in 'num_points'.
    
    GIVEN: an input graph  
    WHEN: an instance of the class 'GetRemotionFrequencies' is created
    THEN: check the length of the generated array is not bigger than 'num_points'
    '''
    points = rn.choice(range(0, 50))
    freq = GetRemotionFrequencies(graph, num_points = points)
    assert len(freq.num_removals_cleaned) <= points
    
def test_uniqueness_frequencies(graph):
    '''This function tests that there are no repeated values in the array
    'frequencies_cleaned' (attribute of 'GetRemotionFrequencies' class)
    
    GIVEN: an input graph  
    WHEN: instances of the class 'GetRemotionFrequencies' are created
    THEN: the attribute 'frequencies_unique' does't contain repeated values
    '''
    points = rn.choice(range(0, 50))
    freq = GetRemotionFrequencies(graph, num_points = points)
    assert len(freq.frequencies_cleaned) == len(np.unique(freq.frequencies_cleaned))
  
def test_uniqueness_removals(graph):
    '''This function tests that there are no repeated values in the array
    'num_removals_cleaned' (attribute of 'GetRemotionFrequencies' class)
    
    GIVEN: an input graph 
    WHEN: instances of the class 'GetRemotionFrequencies' are created
    THEN: the attribute 'num_removals_unique' does't contain repeated values
    '''
    points = rn.choice(range(0, 50))
    freq = GetRemotionFrequencies(graph, num_points = points)
    assert len(freq.num_removals_cleaned) == len(np.unique(freq.num_removals_cleaned))

def test_output_length_generate_frequencies(graph):
    '''This function tests that the array outputs of the method 'generate_frequencies'
    in the class 'GetRemotionFrequencies' have the same length
    
    GIVEN: an input graph  
    WHEN: instances of the class 'GetRemotionFrequencies' are created
    THEN: their attributes 'num_removals_unique' and 'frequencies_cleaned'
        have the same length
    '''
    points = rn.choice(range(0, 50))
    freq = GetRemotionFrequencies(graph, num_points = points)
    assert len(freq.frequencies_cleaned) == len(freq.num_removals_cleaned)
    
def test_type_frequencies_cleaned(graph):
    ''' This function tests the type of the attribute 'frequencies_cleaned'
    of the class 'GetRemotionFrequencies'
    
    GIVEN: an input graph  
    WHEN: instances of the class 'GetRemotionFrequencies' are created
    THEN: their attribute 'frequencies_cleaned' is an array-type or list-type
    '''
    num_points = rn.choice(range(0, 50))
    freq = GetRemotionFrequencies(graph, num_points)
    assert isinstance(freq.frequencies_cleaned, (list, np.ndarray))
    
def test_type_num_removals_cleaned(graph):
    ''' This function tests the type of the attribute 'num_removals_cleaned'
    of the class 'GetRemotionFrequencies'
    
    GIVEN: an input graph  
    WHEN: instances of the class 'GetRemotionFrequencies' are created
    THEN: their attribute 'num_removals_cleaned' is an array-type or list-type
    '''
    num_points = rn.choice(range(0, 50))
    freq = GetRemotionFrequencies(graph, num_points)
    assert isinstance(freq.num_removals_cleaned, (list, np.ndarray))
    
