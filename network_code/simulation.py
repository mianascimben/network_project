'''

    This script defines the classes implementing the simulation for analyzing
    the changing in the network and epidemic properties when node removals are 
    performed. 

'''

import networkx as nx
import numpy as np
import random as rn
import inspect
import matplotlib.pyplot as plt
from .plot_functions import display_epidemic


class GetRemotionFrequencies: 
    '''
    A class to calculate node remotion frequencies.

    The number of frequencies calculated is set by 'num_points'.
    This is the parent class of ToleranceSimulation and EpidemicToleranceSimulation.
    
    Attributes:
    ----------
    max_removal_rate : float, optional
        Maximum removal rate for the nodes in the network (default is 0.5).
    num_points : int, optional
        Total number of removal frequencies to be generated (default is 15).
    number_of_nodes : int
        Total number of nodes in the network.
    frequencies_cleaned : numpy.ndarray
        Array of unique frequencies after removing repeated values.
    num_removals_cleaned : numpy.ndarray
        Array of unique numbers of removals corresponding to the 
        'frequencies_cleaned'.
    
    Methods:
    -------
    calculate_frequencies():
        Calculates the frequencies and the number of node removals based on the
        maximum removal rate and the number of points.
    '''
    
    def __init__(self, G, max_removal_rate = 0.5, num_points = 15):
        '''Constructs all the necessary attributes for the subclasses.
        
        Parameters:
        ----------
        max_removal_rate : float, optional
            Maximum removal rate for the nodes in the network (default is 0.5).
        num_points : int, optional
            Total number of removal frequencies to be generated (default is 15).
        number_of_nodes : int
            Total number of nodes in the network.
        frequencies_cleaned : numpy.ndarray
            Array of unique frequencies after removing repeated values.
        num_removals_cleaned : numpy.ndarray
            Array of unique numbers of removals corresponding to the 
            'frequencies_cleaned'.
        
        '''
        self.max_removal_rate = max_removal_rate
        self.num_points = num_points
        self.number_of_nodes = nx.number_of_nodes(G)
        self.frequencies_cleaned, self.num_removals_cleaned = self.generate_frequencies()
    
    def generate_frequencies (self):
        '''
        Generate a list of evenly spaced frequency values.

        This function generates a list of frequency values that are evenly spaced 
        between 0 and the specified maximum frequency. The number of values generated
        is specified by the 'num_points' parameter.

        Returns:
        -------
        frequencies_cleaned : numpy.ndarray
            The cleaned array of frequencies.
        num_removals_cleaned : numpy.ndarray
            The cleaned array of the corrisponding number of nodes to be removed.
              
        Examples
        --------
        >>> G = nx.erdos_renyi_graph(100, 0.04)
        >>> GetRemotionFrequencies(G, 0.1, 5).frequencies_cleaned
            array([0.  , 0.02, 0.05, 0.07, 0.1 ])
              
        >>> GetRemotionFrequencies(G, 0.1, 5).num_removals_cleaned
            array([ 0,  2,  5,  7, 10])
        '''
        frequencies = np.linspace(0, self.max_removal_rate, self.num_points)
        num_removals = (frequencies * self.number_of_nodes).astype(int)

        # avoid the repetition of equal numbers in num_errors
        num_removals_cleaned = np.unique(num_removals)
        frequencies_cleaned = (1/self.number_of_nodes)*num_removals_cleaned
        return frequencies_cleaned, num_removals_cleaned

class ToleranceSimulation(GetRemotionFrequencies):
    '''
    A class to study network tolerance to node remotion (error/attack) by 
    analysing the behaviour of a specified 'property_function'.

    Attributes:
    ----------
    G : networkx.Graph
        The input network graph on which running the simulation.
        
    All the attributes included in the 'GetRemotionFrequencies' class 
    
    Methods:
    -------
    graph_property_vs_removals(property_function, removal_function):
        Calculates the specified graph property as a function of node removals.

    Notes
    -----
    This class is connected to 'GetRemotionFrequencies' by inheritance.
    '''
    
    def __init__(self, G, max_removal_rate = 0.5, num_points = 15):
        '''
        Initializes the ToleranceSimulation with a graph, maximum removal rate, and number of points.

        Parameters:
        ----------
        G : networkx.Graph
            The input network graph.
        max_removal_rate : float, optional
            The maximum removal rate for the nodes (default is 0.5).
        num_points : int, optional
            The number of points for calculating the removal frequencies 
            (default is 15).
        
        '''
        super().__init__(G, max_removal_rate, num_points)
        self.G = G
        
    def graph_property_vs_removals(self, property_function, removal_function, random_seed = None):
        '''
        Calculates the specified graph property as a function of node removals.

        This function generates new versions of the input graph 'G', each subjected
        to a different node removal frequency. The removals can be randomly (error) or 
        hierarchically (attack) selected depending on the 'removal_function'. 
        It then calculates the property of the graph, defined by 'property_function',
        for each modified graph and returns the data for further analysis or 
        plotting.

        Parameters
        ----------
        property_function : function
            A function that calculates a property of the graph.
        removal_function : function
            A function that removes nodes from the graph.
        random_seed : int
            For reproducibility

        Returns:
        -------
        frequencies_cleaned : numpy.ndarray
            The cleaned array of frequencies.
        property_values : list
            The list of property values corresponding to each frequency.
        
        Examples
        --------
        >>> G = nx.erdos_renyi_graph(100, 0.05)
        >>> freq, diam = ToleranceSimulation(G, num_points = 5).graph_property_vs_removals(get_diameter, attack)
        >>> freq
        array([0.  , 0.01, 0.02, 0.03, 0.05])
        >>> diam
        [3.3, 3.3, 3.4, 3.5, 3.6]
        
        '''
        if random_seed is not None:
            rn.seed(random_seed)
            np.random.seed(random_seed)
            
        property_values = []
        
        for i in self.num_removals_cleaned:
            G_modified = removal_function(self.G, i)
            property_values.append(property_function(G_modified))
         
        return self.frequencies_cleaned, property_values
    
class SIR_Model():
    '''
    A class to simulate the spread of an epidemic on a network using the SIR model.

    Attributes:
    ----------
    number_of_nodes : int
        The total number of nodes in the network.
    mu : float
        The transmission probability.
    nu : float
        The recovery probability.
    duration : int
        The duration of the epidemic simulation.
    infected_t0 : int
        The initial number of infected nodes.
    
    Methods:
    -------
    first_infection():
        Initializes the infection state by randomly infecting a set number of 
        nodes.

    evolution(G, plot_spread=False):
        Simulates the evolution of the epidemic using the SIR model.

    get_infected(G, state):
        Updates the infection state of the network using a for loop over 
        discordant links.

    get_recovered(starting_state, final_state):
        Updates the state of the network by assigning immunity to infected nodes.

    '''
    def __init__(self, G, mu, nu, duration, infected_t0):
        '''
        Initializes the 'SIR_Model' class with the network and the epidemic
        parameters.

        Parameters:
        ----------
        G : networkx.Graph
            The input network graph.
        mu : float
            The transmission probability.
        nu : float
            The recovery probability.
        duration : int
            The duration of the epidemic simulation.
        infected_t0 : int
            The initial number of infected nodes.
        '''
        self.number_of_nodes = nx.number_of_nodes(G)
        self.mu = mu
        self.nu = nu
        self.duration = duration
        self.infected_t0 = infected_t0
        
    def first_infection(self):
        '''
        Initializes the infection state by randomly infecting a set number of
        nodes.

        Returns:
        -------
        state : numpy.ndarray
            The array representing the initial infection state of the network.
        '''
        state = np.zeros(self.number_of_nodes)
        infected_index = np.random.randint(0, self.number_of_nodes, self.infected_t0)
        state[infected_index] = 1
        return state
    
    def evolution(self, G, plot_spread = False):
        '''
        Simulates the evolution of the epidemic using the SIR model.
        
        This process relies on two assumptions: the infection and immunisation are
        binomial processes and the trasmission of the disease can only happen among 
        nodes that are connected.
        
        Each node can be in two states: 
            0  if the node is susceptible 
            1  if the node is infected
            -1 if the node has recovered
            
        This function lets to visualize the evolution of the states of the nodes
        over time, by setting the 'plot_spread' variable equal to 'True'. 
            red nodes: infected state
            green nodes: recovered state
            blue nodes: susceptible state
        
        Parameters:
        ----------
        G : networkx.Graph
            The input network graph.
            plot_spread : bool, optional
            If True, plots the spread of the epidemic over time (default is False).

       Returns:
       -------
       infection_rate : numpy.ndarray
           The array emboding the fraction of infected cases over time.
       recovered_rate : numpy.ndarray
           The array embodying the fraction of recovered nodes over time.
           
       Notes:
       -----
       
       The recovery process taking place at a certain time step
       cannot recover the nodes that have been infected during the same 
       time step. So it only works on nodes infected at leat from 1 time step. 
       
       The plotting functionality needs a lot of power and time. 
       The plots are thought to provide a visual understanding of the epidemic 
       dynamics and not to analyze it. When you use it, make sure to have small
       networks and a short simulation. 
       '''
        state =  self.first_infection()
        
        # In error/attack simulation relabeling prevent from incongruences between 
        # indexes of the array 'state', that go from 0 to number of nodes of the
        # actual graph, and the nodes labels of the first graph of the simulation.
        # Maybe the index i in 'state' has been erased in the graph: this label
        # would refer to nothing.
        G = nx.convert_node_labels_to_integers(G)
        
        if plot_spread:
            pos = nx.circular_layout(G)  # fixed layout for the graph
            display_epidemic(G, state, pos) 
            
        infection_rate = []
        recovered_rate = []
        
        for time in range(1, self.duration + 1):
            
            infected_state = self.get_infected(G, state)
        
            recovered_state = self.get_recovered(state, infected_state)
            
            infection_rate.append(np.mean(recovered_state == 1))
            recovered_rate.append(np.mean(recovered_state == -1))
            
            state = recovered_state
            
            if plot_spread:
                display_epidemic(G, recovered_state, pos)
                
        return np.array(infection_rate), np.array(recovered_rate)
        
    def get_infected(self, G, starting_state):
        '''
        Updates the infection state of the network.
        
        This function identifies the nodes that are currently susceptible and 
        applies a binomial process to determine which of these nodes become 
        infected. The infection can happen only among nodes that are connected. 
        Infected nodes are then marked in the final state with a value of 1.

        Parameters:
        ----------
        G : networkx.Graph
            The input network graph.
        starting_state : numpy.ndarray
            The current state of the nodes.

        Returns:
        -------
        state : numpy.ndarray
            The updated state of the nodes after infection.
        '''
        state = starting_state
        # find all the pairs of nodes that are connected by an edge and in which
        # one of the two nodes is infected and the other susceptible
        discordant_links = [(u, v) for u, v in G.edges() if state[u] + state[v] == 1]
        transmission = np.random.binomial(1, self.mu, len(discordant_links))
            
        #Update the infection status
        for j, (u, v) in enumerate(discordant_links):
            if transmission[j]:
                state[u] = state[v] = 1 
        
        return state

    def get_recovered(self, starting_state, final_state):
        '''
        Updates the state of the network by assigning immunity to infected nodes.

        This function identifies the nodes infected (before they have
        trasmited the disease) and applies a binomial process to determine which 
        of these nodes become recovered. 
        Recovered nodes are then marked with a value of -1 only after the 
        trasmission of the desease has be performed, that is the final state.
        
        Parameters:
        ----------
        starting_state : numpy.ndarray
            The initial state of the network, where infected nodes are marked.
            It is the array of the states before the infected nodes have 
            trasmitted the disease with a value of 1.
        final_state : numpy.ndarray
            The state of the network to be updated with recovered nodes.
            It is the array of the states after the infected nodes have 
            trasmitted the disease.            

        Returns:
        -------
        final_state : numpy.ndarray
            The updated state of the network, with recovered nodes marked as -1.

        '''
        infected_nodes = np.where(starting_state == 1)
        immunity = np.random.binomial(1, self.nu, len(infected_nodes[0])).astype(bool)
        recovered_nodes = infected_nodes[0][immunity]
        final_state[recovered_nodes] = -1
        return final_state     

class EpidemicToleranceSimulation(GetRemotionFrequencies):
    '''
    A class to simulate the effect of node removals on epidemic spread in a network.

    This class extends the GetRemotionFrequencies class and integrates epidemic 
    simulation using the SIR model to study how the removal of nodes impacts
    the spread of an epidemic.

    Attributes:
    ----------
    G : networkx.Graph
        The input network graph.
    epidemic_data : SIR_Model
        An instance of SIR_Model to simulate the epidemic on the network.
    All the attributes included in the 'GetRemotionFrequencies' class.
    
    Methods:
    -------
    epidemic_property_vs_removals(property_function, removal_function, *args, **kwargs):
        Simulates the effect of node removals on the spread of the epidemic and 
        calculates the specified epidemic property as a function of node removal.
        
    Notes:
    -----
    This class is connected to 'GetRemotionFrequencies' by inheritance and to 
    SIR_Model by composition.
    '''
    
    def __init__(self, G, mu, nu, duration, infected_t0, max_removal_rate = 0.5, num_points = 15):
        '''
        Initializes the EpidemicToleranceSimulation with the network and epidemic parameters.

        Parameters:
        ----------
        G : networkx.Graph
            The input network graph.
        mu : float
            The transmission probability.
        nu : float
            The recovery probability.
        duration : int
            The duration of the epidemic simulation.
        infected_t0 : int
            The initial number of infected nodes.
        max_removal_rate : float, optional
            The maximum removal rate for the nodes (default is 0.5).
        num_points : int, optional
            The number of points for calculating the removal frequencies (default is 15).
        '''
        super().__init__(G, max_removal_rate, num_points)
        self.epidemic_data = SIR_Model(G, mu, nu, duration, infected_t0)
        self.G = G
        
        
    def epidemic_property_vs_removals(self, property_function, removal_function, num_simulations, random_seed = None, *args, **kwargs):
        '''
        Simulates the effect of node removals on an epidemic spreading and 
        records the changing in the value of the property given by 
        'property_function'.

        This method simulates the spread of an epidemic following the SIR model 
        on a network after nodes are removed according to a given 
        'removal_function'. It then evaluates a specified epidemic property at 
        each removal stage. 
        In order to avoid random effects more simulations are runned at each 
        removal frequencies. Then the value of the epidemic property is averaraged
        over all the simulations.

        Parameters:
        ----------
        property_function : function
            A function that calculates a specific property of the epidemic.
        removal_function : function
            A function that removes nodes from the network.
        num_simulations: int
            The number of simulations to run for each removal stage, allowing 
            for the averaging of results 
            to account for the randomness in epidemic spreading.
        random_seed : int
            For reproducibility
        *args : tuple
            Additional arguments to pass to the property function.
        **kwargs : dict
            Additional keyword arguments to pass to the property function.

        Returns:
        -------
        frequencies_cleaned : numpy.ndarray
            The array of frequencies corresponding to the removal rates.
        property_values : list
            The list of the values of the calculated feature of the epidemic
            at each removal frequency.
            
        Notes
        -----
        The 'property_function' has some restrictions about its input: it is 
        expected to handle the infection  evolution over time. However, 
        it can also handle the immunization evolution or other parameters if the
        'property_function' requires them.

        
        Examples
        --------
        >>> G = nx.erdos_renyi_graph(100, 0.05)
        >>> simulation = EpidemicToleranceSimulation(G, mu=0.15, nu=0.05, 
                                                     duration=50, infected_t0=1,
                                                     num_points=5)
        >>> freq, duration = simulation.epidemic_property_vs_removals(epidemic_duration, 
                                                                      attack, 
                                                                      num_simulations=10)
        >>> freq
        array([0.  , 0.01, 0.02, 0.03, 0.05])
        >>> duration
        [45.1, 50.0, 35.8, 50.0, 50.0]
        '''
        
        if random_seed is not None:
            rn.seed(random_seed)
            np.random.seed(random_seed)

        property_values = []
         
        for num_removed_nodes in self.num_removals_cleaned:
            G_modified = removal_function(self.G, num_removed_nodes)
            
            # Each row represents an epidemic simulation
            infected = np.zeros((num_simulations, self.epidemic_data.duration))
            recovered = np.zeros((num_simulations, self.epidemic_data.duration))
            
            for simulation in range(num_simulations): 
                infected[simulation, :], recovered[simulation, :] = self.epidemic_data.evolution(G_modified, plot_spread = False)
            
            # Calculate the epidemic property
            # checking if the property function requires recovery evolution
            if 'recovery_evolution' in inspect.signature(property_function).parameters:
                result = property_function(infected, recovered, *args, **kwargs)
            else:
                result = property_function(infected, *args, **kwargs)
                            
            property_values.append(result)
                            
        
        return self.frequencies_cleaned, property_values
    
