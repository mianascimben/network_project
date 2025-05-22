''' 

Tests the remaining functions in analysis_functions
'''
import pytest
import networkx as nx
import numpy as np
from network_code.analysis_functions import generate_network, connectivity_analysis, fragmentation_analysis, epidemic_feature_analysis
from network_code.simulation import ToleranceSimulation, EpidemicToleranceSimulation
from network_code import diameter, largest_connected_component_size, average_size_connected_components
from network_code import peak, t_peak, epidemic_duration, total_infected
from network_code import error, attack

# constants for network creation
N = 100 # number of nodes
p = 0.4 # prob of connection

@pytest.mark.parametrize("network_label", [('ER'),('SF'),('airports')])
def test_valid_output(network_label):
    G = generate_network(network_label, N , p) 
    assert isinstance(G, nx.classes.graph.Graph)
    
@pytest.fixture
def graph():
    G = nx.erdos_renyi_graph(N, p)
    return G
@pytest.fixture
def structural_sim(graph):
    sim = ToleranceSimulation(graph)
    return sim 
@pytest.fixture
def connectivity_output(structural_sim):
    return connectivity_analysis(structural_sim)

def test_connectivity_output_length(structural_sim, connectivity_output):
    '''
    Tests that the outputs of the 'connectivity_analysis' have the same length
    
    GIVEN: an istance of the 'ToleranceSimulation' class and the results from
        the 'connectivity_analysis' function
    WHEN: considering the three function outputs
    THEN: they have the same length
    '''
    freq, results_error, results_attack = connectivity_output
    len_freq = len(freq)
    len_error = len(results_error)
    len_attack = len(results_error)
    assert len_freq == len_error == len_attack

def test_connectivity_check_freq (structural_sim, connectivity_output):
    '''
    Tests that the first output of 'connectivity_analysis' are the frequencies 
    that are attributes of the 'ToleranceSimulation' class.
    
    GIVEN: an istance of the 'ToleranceSimulation' class and the results from
        the 'connectivity_analysis' function
    WHEN: subtracting pairwise the expected frequencies from the first output 
        of the 'connectivity_analysis' 
    THEN: all the elements are zero
    '''
    expected = structural_sim.frequencies_cleaned
    array_expected = np.array(expected)
    array_output = np.array(connectivity_output[0])
    assert (array_output - array_expected).all() < 1e-7
   
def test_connectivity_check_d_error (structural_sim, connectivity_output):
    '''
    Tests that the second output of 'connectivity_analysis' are the diameter values
    of the graph which undergoes errors.
    
    GIVEN: an istance of the 'ToleranceSimulation' class and the results from
        the 'connectivity_analysis' function
    WHEN: subtracting pairwise the expected diameter values from the second output 
        of the 'connectivity_analysis' 
    THEN: all the elements are zero
    '''
    _, expected = structural_sim.graph_property_vs_removals(diameter, error)
    array_expected = np.array(expected)
    array_output = np.array(connectivity_output[1])
    assert (array_output - array_expected).all() < 1e-7
    
def test_connectivity_check_d_attack (structural_sim, connectivity_output):
    '''
    Tests that the second output of 'connectivity_analysis' are the diameter values
    of the graph which undergoes attacks.
    
    GIVEN: an istance of the 'ToleranceSimulation' class and the results from
        the 'connectivity_analysis' function
    WHEN: subtracting pairwise the expected diameter values from the second output 
        of the 'connectivity_analysis' 
    THEN: all the elements are zero
    '''
    _, expected = structural_sim.graph_property_vs_removals(diameter, attack)
    array_expected = np.array(expected)
    array_output = np.array(connectivity_output[2])
    assert (array_output - array_expected).all() < 1e-7
 
@pytest.fixture
def fragmentation_output(structural_sim):
    return fragmentation_analysis(structural_sim)

def test_fragmentation_output_length(structural_sim, fragmentation_output):
    '''
    Tests that the outputs of the 'connectivity_analysis' have the same length
    
    GIVEN: an istance of the 'ToleranceSimulation' class and the results from
        the 'fragmentation_analysis' function
    WHEN: considering the three function outputs
    THEN: they have the same length
    '''
    freq, S_error, S_attack, s_attack, s_error = fragmentation_output
    len_freq = len(freq)
    len_S_error = len(S_error)
    len_S_attack = len(S_attack)
    len_s_error = len(s_error)
    len_s_attack = len(s_attack)
    assert len_freq == len_S_error == len_S_attack == len_s_error == len_s_attack

def test_fragmentation_check_freq (structural_sim, fragmentation_output):
    '''
    Tests that the first output of 'fragmentation_analysis' are the frequencies 
    that are attributes of the 'ToleranceSimulation' class.
    
    GIVEN: an istance of the 'ToleranceSimulation' class and the results from
        the 'fragmentation_analysis' function
    WHEN: subtracting pairwise the expected frequencies from the first output 
        of the 'fragmentation_analysis' 
    THEN: all the elements are zero
    '''
    expected = structural_sim.frequencies_cleaned
    array_expected = np.array(expected)
    array_output = np.array(fragmentation_output[0])
    assert (array_output - array_expected).all() < 1e-7
   
def test_fragmentation_check_S_error (structural_sim, fragmentation_output):
    '''
    Tests that the second output of 'fragmentation_analysis' are the values of the 
    giant component size (S) of the graph which undergoes errors.
    
    GIVEN: an istance of the 'ToleranceSimulation' class and the results from
        the 'fragmentation_analysis' function
    WHEN: subtracting pairwise the expected S values from the second output 
        of the 'fragmentation_analysis' 
    THEN: all the elements are zero
    '''
    _, expected = structural_sim.graph_property_vs_removals(largest_connected_component_size, error)
    array_expected = np.array(expected)
    array_output = np.array(fragmentation_output[1])
    assert (array_output - array_expected).all() < 1e-7 

def test_fragmentation_check_S_attack (structural_sim, fragmentation_output):
    '''
    Tests that the third output of 'fragmentation_analysis' are the values of the 
    giant component size (S) of the graph which undergoes attacks.
    
    GIVEN: an istance of the 'ToleranceSimulation' class and the results from
        the 'fragmentation_analysis' function
    WHEN: subtracting pairwise the expected S values from the third output 
        of the 'fragmentation_analysis' 
    THEN: all the elements are zero
    '''
    _, expected = structural_sim.graph_property_vs_removals(largest_connected_component_size, attack)
    array_expected = np.array(expected)
    array_output = np.array(fragmentation_output[2])
    assert (array_output - array_expected).all() < 1e-7 
    
def test_fragmentation_check_s_error (structural_sim, fragmentation_output):
    '''
    Tests that the forth output of 'fragmentation_analysis' are the average size
    values of the components excluded the giant one (<s>) of the graph which 
    undergoes errors.
    
    GIVEN: an istance of the 'ToleranceSimulation' class and the results from
        the 'fragmentation_analysis' function
    WHEN: subtracting pairwise the expected <s> values from the forth output 
        of the 'fragmentation_analysis' 
    THEN: all the elements are zero
    '''
    _, expected = structural_sim.graph_property_vs_removals(average_size_connected_components, error)
    array_expected = np.array(expected)
    array_output = np.array(fragmentation_output[3])
    assert (array_output - array_expected).all() < 1e-7 
    
def test_fragmentation_check_s_attack (structural_sim, fragmentation_output):
    '''
    Tests that the fifth output of 'fragmentation_analysis' are the average size
    values of the components excluded the giant one (<s>) of the graph which 
    undergoes attacks.
    
    GIVEN: an istance of the 'ToleranceSimulation' class and the results from
        the 'fragmentation_analysis' function
    WHEN: subtracting pairwise the expected <s> values from the fifth output 
        of the 'fragmentation_analysis' 
    THEN: all the elements are zero
    '''
    _, expected = structural_sim.graph_property_vs_removals(average_size_connected_components, attack)
    array_expected = np.array(expected)
    array_output = np.array(fragmentation_output[4])
    assert (array_output - array_expected).all() < 1e-7

@pytest.fixture
def epidemic_sim(graph):
    sim = EpidemicToleranceSimulation(graph, mu = 0.2, nu = 0.07, duration = 10, infected_t0 = 1)
    return sim 
    
@pytest.fixture
def peak_output(epidemic_sim):
    return epidemic_feature_analysis(epidemic_sim, peak, num_simulations = 1)

def test_peak_check_freq (epidemic_sim, peak_output):
    '''
    Tests that the first output of 'epidemic_feature_analysis' are the frequencies 
    that are attributes of the 'EpidemicToleranceSimulation' class.
    
    GIVEN: an istance of the 'EpidemicToleranceSimulation' class and the results 
        from the 'epidemic_feature_analysis' function
    WHEN: subtracting pairwise the expected frequencies from the first output 
        of the 'epidemic_feature_analysis' 
    THEN: all the elements are zero
    '''
    expected = epidemic_sim.frequencies_cleaned
    array_expected = np.array(expected)
    array_output = np.array(peak_output[0])
    assert (array_output - array_expected).all() < 1e-7
   
def test_epidemic_feature_check_peak_error(epidemic_sim, peak_output, num_simulations = 1):
    '''
    Tests that the second output of 'epidemic_feature_analysis(_, peak, _)'
    are the epidemic peak values for the graph which undergoes errors.
    
    GIVEN: an istance of the 'EpidemicToleranceSimulation' class and the results from
        the 'epidemic_feature_analysis(_, peak, _)' function
    WHEN: subtracting pairwise the expected peak values from the second output 
        of the 'epidemic_feature_analysis(_, peak, _)' 
    THEN: all the elements are zero
    '''
    _, expected =  epidemic_sim.epidemic_property_vs_removals(peak, error, num_simulations)
    array_expected = np.array(expected)
    array_output = np.array(peak_output[1])
    assert (array_output - array_expected).all() < 1e-7

def test_epidemic_feature_check_peak_attack(epidemic_sim, peak_output, num_simulations = 1):
    '''
    Tests that the third output of 'epidemic_feature_analysis(_, peak, _)'
    are the epidemic peak values for the graph which undergoes attacks.
    
    GIVEN: an istance of the 'EpidemicToleranceSimulation' class and the results from
        the 'epidemic_feature_analysis(_, peak, _)' function
    WHEN: subtracting pairwise the expected peak values from the third output 
        of the 'epidemic_feature_analysis(_, peak, _)' 
    THEN: all the elements are zero
    '''
    _, expected =  epidemic_sim.epidemic_property_vs_removals(peak, attack, num_simulations)
    array_expected = np.array(expected)
    array_output = np.array(peak_output[2])
    assert (array_output - array_expected).all() < 1e-7
    
@pytest.fixture
def t_peak_output(epidemic_sim):
    return epidemic_feature_analysis(epidemic_sim, t_peak, num_simulations = 1)

def test_epidemic_feature_check_t_peak_error(epidemic_sim, t_peak_output, num_simulations = 1):
    '''
    Tests that the second output of 'epidemic_feature_analysis(_, t_peak, _)'
    are the epidemic t_peak values for the graph which undergoes errors.
    
    GIVEN: an istance of the 'EpidemicToleranceSimulation' class and the results from
        the 'epidemic_feature_analysis(_, t_peak, _)' function
    WHEN: subtracting pairwise the expected t_peak values from the second output 
        of the 'epidemic_feature_analysis(_, t_peak, _)' 
    THEN: all the elements are zero
    '''
    _, expected =  epidemic_sim.epidemic_property_vs_removals(t_peak, error, num_simulations)
    array_expected = np.array(expected)
    array_output = np.array(t_peak_output[1])
    assert (array_output - array_expected).all() < 1e-7
    
def test_epidemic_feature_check_t_peak_attack(epidemic_sim, t_peak_output, num_simulations = 1):
    '''
    Tests that the third output of 'epidemic_feature_analysis(_, t_peak, _)'
    are the epidemic t_peak values for the graph which undergoes attacks.
    
    GIVEN: an istance of the 'EpidemicToleranceSimulation' class and the results from
        the 'epidemic_feature_analysis(_, t_peak, _)' function
    WHEN: subtracting pairwise the expected t_peak values from the third output 
        of the 'epidemic_feature_analysis(_, t_peak, _)' 
    THEN: all the elements are zero
    '''
    _, expected =  epidemic_sim.epidemic_property_vs_removals(t_peak, attack, num_simulations)
    array_expected = np.array(expected)
    array_output = np.array(t_peak_output[2])
    assert (array_output - array_expected).all() < 1e-7

@pytest.fixture
def duration_output(epidemic_sim):
    return epidemic_feature_analysis(epidemic_sim, epidemic_duration, num_simulations = 1)

def test_epidemic_feature_check_duration_error(epidemic_sim, duration_output, num_simulations = 1):
    '''
    Tests that the second output of 'epidemic_feature_analysis(_, epidemic_duration, _)'
    are the epidemic life values for the graph which undergoes errors.
    
    GIVEN: an istance of the 'EpidemicToleranceSimulation' class and the results from
        the 'epidemic_feature_analysis(_, epidemic_duration, _)' function
    WHEN: subtracting pairwise the expected epidemic_duration values from the 
        second output  of the 'epidemic_feature_analysis(_, epidemic_duration, _)' 
    THEN: all the elements are zero
    '''
    _, expected =  epidemic_sim.epidemic_property_vs_removals(epidemic_duration, error, num_simulations)
    array_expected = np.array(expected)
    array_output = np.array(duration_output[1])
    assert (array_output - array_expected).all() < 1e-7
    
def test_epidemic_feature_check_duration_attack(epidemic_sim, duration_output, num_simulations = 1):
    '''
    Tests that the third output of 'epidemic_feature_analysis(_, epidemic_duration, _)'
    are the epidemic life values for the graph which undergoes attacks.
    
    GIVEN: an istance of the 'EpidemicToleranceSimulation' class and the results from
        the 'epidemic_feature_analysis(_, epidemic_duration, _)' function
    WHEN: subtracting pairwise the expected epidemic_duration values from the 
        third output  of the 'epidemic_feature_analysis(_, epidemic_duration, _)' 
    THEN: all the elements are zero
    '''
    _, expected =  epidemic_sim.epidemic_property_vs_removals(epidemic_duration, attack, num_simulations)
    array_expected = np.array(expected)
    array_output = np.array(duration_output[2])
    assert (array_output - array_expected).all() < 1e-7
    
@pytest.fixture
def infected_output(epidemic_sim):
    return epidemic_feature_analysis(epidemic_sim, total_infected, num_simulations = 1)

def test_epidemic_feature_check_infected_error(epidemic_sim, infected_output, num_simulations = 1):
    '''
    Tests that the second output of 'epidemic_feature_analysis(_, total_infected, _)'
    are the values of total infected cases for the graph which undergoes errors.
    
    GIVEN: an istance of the 'EpidemicToleranceSimulation' class and the results from
        the 'epidemic_feature_analysis(_, total_infected, _)' function
    WHEN: subtracting pairwise the expected total_infected values from the 
        second output  of the 'epidemic_feature_analysis(_, total_infected, _)' 
    THEN: all the elements are zero
    '''
    _, expected =  epidemic_sim.epidemic_property_vs_removals(total_infected, error, num_simulations)
    array_expected = np.array(expected)
    array_output = np.array(infected_output[1])
    assert (array_output - array_expected).all() < 1e-7
    
def test_epidemic_feature_check_infectedk_attack(epidemic_sim, infected_output, num_simulations = 1):
    '''
    Tests that the third output of 'epidemic_feature_analysis(_, total_infected, _)'
    are the values of total infected cases for the graph which undergoes attacks.
    
    GIVEN: an istance of the 'EpidemicToleranceSimulation' class and the results from
        the 'epidemic_feature_analysis(_, total_infected, _)' function
    WHEN: subtracting pairwise the expected total_infected values from the 
        third output  of the 'epidemic_feature_analysis(_, total_infected, _)' 
    THEN: all the elements are zero
    '''
    _, expected =  epidemic_sim.epidemic_property_vs_removals(total_infected, attack, num_simulations)
    array_expected = np.array(expected)
    array_output = np.array(infected_output[2])
    assert (array_output - array_expected).all() < 1e-7
