'''
    This script tests the functions present in 'graph_property_functions'
'''


import pytest
import networkx as nx
import numpy as np

from network_code.analysis_functions import diameter, largest_connected_component_size, average_size_connected_components


@pytest.fixture
def G_directed():
    ''' Directed strongly connected graph '''
    G = nx.DiGraph()
    G.add_edges_from([(0, 1), (1, 2), (2, 0)])
    return G
@pytest.fixture
def G_dir_multi_components():
    ''' Directed not strongly connected graph, but with multiple components'''
    G = nx.DiGraph()
    G.add_edges_from([(0, 1), (1, 2), (2, 0), (2, 3), (1, 4)])
    G.add_edges_from([(10, 11), (11, 12), (12, 13)])
    G.add_edges_from([(20, 21), (20, 22), (21, 22)])
    return G
@pytest.fixture
def G_dir_isolated_nodes(G_directed):
    ''' Directed strongly connected graph with two isolated nodes '''
    G_directed.add_nodes_from([4, 10])
    return G_directed  

@pytest.fixture
def G_undirected():
    ''' Unirected connected graph '''
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 0)])
    return G
@pytest.fixture
def G_undir_multi_components():
    ''' Unirected graph with multiple components'''
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 0), (2, 3), (1, 4)])
    G.add_edges_from([(10, 11), (11, 12), (12, 13)])
    G.add_edges_from([(20, 21), (20, 22), (21, 22)])
    return G
@pytest.fixture
def G_undir_isolated_nodes(G_undirected):
    ''' Undirected connected graph with two isolated nodes '''
    G_undirected.add_nodes_from([4, 10])
    return G_undirected

@pytest.fixture
def G_empty():
    G = nx.Graph()
    return G

class TestDiameter:
    def test_diameter_directed_strongly_connected_graph(self, G_directed):
        ''' This function check that 'diameter' works properly with directed graphs 
        that don't contain isolated nodes
        
        GIVEN: a directed graph w/o isolated nodes 
        WHEN: I apply to it the 'diameter' function
        THEN: it returns the diameter of the input graph
        '''
        expected = nx.average_shortest_path_length(G_directed)
        result = diameter(G_directed)
        assert result == expected
          
    def test_diameter_directed_isolated_nodes_graph(self, G_dir_isolated_nodes):
        ''' This function check 'diameter' works properly with directed graphs 
        that contain isolated nodes
        
        GIVEN: a directed graph with isolated nodes 
        WHEN: I apply to it the 'diameter' function
        THEN: it returns the diameter of the input graph
        '''
        isolated_nodes = nx.isolates(G_dir_isolated_nodes) # keep out the isolated nodes
        G_dir_isolated_nodes.remove_nodes_from(list(isolated_nodes))
        expected = nx.average_shortest_path_length(G_dir_isolated_nodes)
        
        result = diameter(G_dir_isolated_nodes)
        assert result == expected
        
    def test_diameter_disconnected_graph(self):
        ''' This function check that 'diameter' returns zero when working with 
        graphs that have no edges
        
        GIVEN: a graph with no connections
        WHEN: I apply to it the 'diameter' function
        THEN: it returns the diameter equal to zero 
        '''
        G = nx.Graph()
        G.add_nodes_from([1,2,3,4])
        result = diameter(G)
        assert result == 0
        
    def test_diameter_undirected_connected_graph(self, G_undirected):
        ''' This function check that 'diameter' works properly with undirected 
        connected graphs (no multiple components)
        
        GIVEN: a connected undirected graph  
        WHEN: I apply to it the 'diameter' function
        THEN: it returns the diameter of the input graph
        '''
        expected = nx.average_shortest_path_length(G_undirected) 
        result = diameter(G_undirected)  
        assert result == expected
        
    def test_diameter_undirected_isolated_nodes_graph(self, G_undir_isolated_nodes):
        ''' This function check that 'diameter' works properly with undirected 
        graphs that contain isolated nodes
        
        GIVEN: an undirected graph with isolated nodes 
        WHEN: I apply to it the 'diameter' function
        THEN: it returns the diameter of the input graph
        '''
        isolated_nodes = nx.isolates(G_undir_isolated_nodes) # keep out the isolated nodes
        G_undir_isolated_nodes.remove_nodes_from(list(isolated_nodes))
        expected = nx.average_shortest_path_length(G_undir_isolated_nodes) 
        
        result = diameter(G_undir_isolated_nodes)
        assert result == expected
        
    def test_diameter_empty_graph(self, G_empty):
        ''' This function check that 'diameter' returns zero when working with 
        empty graphs
        
        GIVEN: an empty graph
        WHEN: I apply to it the 'diameter' function
        THEN: it returns the diameter equal to zero 
        '''
        result = diameter(G_empty)
        assert result == 0
        

class TestLargestConnectedComponentSize: 
    
    def test_largest_size_directed_graph(self, G_dir_multi_components):
        ''' This function tests that the function 'largest_connected_component_size'
        calculates the size of the giant component of directed graphs
        
        GIVEN: a directed graph
        WHEN: I apply to it the 'largest_connected_component_size' function
        THEN: the resulting state is the size of the giant component
        '''
              
        largest_cc = max(nx.weakly_connected_components(G_dir_multi_components), 
                         key=len)
        expected = len(largest_cc)/nx.number_of_nodes(G_dir_multi_components)
        
        result = largest_connected_component_size(G_dir_multi_components)
        assert result == expected
    
    def test_largest_size_undirected_graph(self):
        ''' This function tests that the function 'largest_connected_component_size'
        calculates the size of the giant component of generic undirected graphs
        
        GIVEN: an undirected graph
        WHEN: I apply to it the 'largest_connected_component_size' function
        THEN: the resulting state is the size of the giant component
        '''
        G = nx.erdos_renyi_graph(100, 0.01)
        
        largest_cc = max(nx.connected_components(G), key=len)
        expected = len(largest_cc)/nx.number_of_nodes(G)
        
        result = largest_connected_component_size(G)
        assert result == expected
    
    def test_largest_size_empty_graph(self, G_empty):
        ''' This function check that 'largest_connected_component_size' returns zero
        when working with empty graphs
        
        GIVEN: an empty graph
        WHEN: I apply to it the 'largest_connected_component_size' function
        THEN: it returns the size of the giant component equal to zero 
        '''
        result = largest_connected_component_size(G_empty)
        assert result == 0
        

class TestAverageSizeConnecteComponets:
    
    def test_average_multiple_components_graph(self, G_dir_multi_components):
        ''' This function tests that the function 'average_size_connected_components'
        calculates the average size of all the connected components but the
        giant component for directed graphs with multiple components 
        
        GIVEN: an directed graph
        WHEN: I apply to it the 'average_size_connected_components' function
        THEN: the resulting state is the average size of the connected components,
            but the largest one
        '''
        sizes = [len(c) for c in sorted(nx.weakly_connected_components(
            G_dir_multi_components),key=len)]
        expected = np.mean(sizes[:-1])
        
        result = average_size_connected_components(G_dir_multi_components)
        assert result == expected
    
    def test_average_size_undirected_graph(self, G_undir_multi_components):
        ''' This function tests that the function 'average_size_connected_components'
        calculates the average size of all the connected components but the
        giant component for undirected graphs with multiple components
        
        GIVEN: an undirected graph
        WHEN: I apply to it the 'average_size_connected_components' function
        THEN: the resulting state is the average size of the connected components,
            but the largest one
        '''
        sizes = [len(c) for c in sorted(nx.connected_components(
            G_undir_multi_components), key=len)]
        expected = np.mean(sizes[:-1])
        
        result = average_size_connected_components(G_undir_multi_components)
        assert result == expected
        
    def test_average_size_without_multi_components(self, G_directed):
        ''' This function tests that the function 'average_size_connected_components'
        calculates the size of the giant component for a directed graph 
        strongly connected (only composed by the giant component)
        
        GIVEN: an directed graph
        WHEN: I apply to it the 'average_size_connected_components' function
        THEN: the resulting state is zero as there are no smaller components 
            outside the giant components
        '''
        result = average_size_connected_components(G_directed)
        assert result == 0
        
    def test_average_size_empty_graph(self, G_empty):
        ''' This function check that 'average_size_connected_components' returns zero
        when working with empty graphs
        
        GIVEN: an empty graph
        WHEN: I apply to it the 'average_size_connected_components' function
        THEN: it returns the average size of the connected components but the 
            largest one equal to zero 
        '''
        result = average_size_connected_components(G_empty)
        assert result == 0
 
@pytest.mark.parametrize( 
    "graph_type", 
    [
        'G_directed',
        'G_dir_multi_components',
        'G_dir_isolated_nodes',
        'G_undirected',
        'G_undir_multi_components',
        'G_undir_isolated_nodes',
        'G_empty',
        ]
    )
      
class TestOutputType:
    ''' Tests the output type of the functions in in 'graph_property_functions'
        by using different graph inputs. Each graph covers the output obtained
        by following one precise logical path
    '''
    
    def test_diameter_valid_output_directed_graph(self, request, graph_type):
        ''' This function checks that the output of 'diameter' is a number
        
        GIVEN: a directed graph
        WHEN: I apply to it the 'diameter' function
        THEN: the resulting state is a single number (int or float)
        '''
        graph_type = request.getfixturevalue(graph_type)

        output = diameter(graph_type)
        assert isinstance(output, (int, float, np.integer, np.floating))
        
    
    def test_average_size_valid_output(self, request, graph_type):
        ''' This function checks that the output of 'average_size_connected_components' 
        is a number
        
        GIVEN: an undirected graph
        WHEN: I apply to it the 'average_size_connected_components' function
        THEN: the resulting state is a single number (int or float)
        '''
        graph_type = request.getfixturevalue(graph_type)

        output = average_size_connected_components(graph_type)
        assert isinstance(output, (int, float, np.integer, np.floating))
    
           
    def test_largest_size_valid_output_undirected_graph(self, request, graph_type):
        ''' This function checks that the output of 'largest_connected_component_size' 
        is a number
        
        GIVEN: an undirected graph
        WHEN: I apply to it the 'largest_connected_component_size' function
        THEN: the resulting state is a single number (int or float)
        '''
        graph_type = request.getfixturevalue(graph_type)

        output = largest_connected_component_size(graph_type)
        assert isinstance(output, (int, float, np.integer, np.floating))