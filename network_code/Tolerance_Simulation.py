# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
import inspect
import matplotlib.pyplot as plt

#from epidemy_functions import evolution_epidemy_SIR

class GetRemotionFrequencies: 
    '''
    A class to calculate remotion frequencies of network nodes

    The number of frequencies calculated is set by 'num_points' and they are
    evenly distant in the range [0, max_removal_rate]
    
    Attributes:
    ----------
    max_removal_rate : float
        Maximum removal rate for the nodes in the network.
    num_points : int
        Total number of removal frequencies to be generated.
    number_of_nodes : int
        Total number of nodes in the network.
    frequencies_cleaned : numpy.ndarray
        Array of unique cleaned frequencies after removing repeated values.
    num_removals_cleaned : numpy.ndarray
        Array of unique cleaned numbers of removals corresponding to the cleaned frequencies.
    
    Methods:
    -------
    calculate_frequencies():
        Calculates the frequencies and the number of node removals based on the maximum removal 
        rate and the number of points.
    '''
    
    def __init__(self,G, max_removal_rate = 0.05, num_points = 20):
        '''Constructs all the necessary attributes for the person object
        
        Parameters:
        ----------
        max_removal_rate : float
            Maximum removal rate for the nodes in the network.
        num_points : int
            Total number of removal frequencies to be generated.
        number_of_nodes : int
            Total number of nodes in the network.
        frequencies_cleaned : numpy.ndarray
            Array of unique cleaned frequencies after removing repeated values.
        num_removals_cleaned : numpy.ndarray
            Array of unique cleaned numbers of removals corresponding to the cleaned frequencies.
        
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
    A class to analyse network tolerance by removing nodes and observing changes in a specified graph property.

    Attributes:
    ----------
    G : networkx.Graph
        The input network graph on which makin the simulation.
        
    Methods:
    -------
    graph_property_vs_removals(property_function, removal_function):
        Calculates the specified graph property as a function of node removals.

    Notes
    -----
    This class is connected to 'GetRemotionFrequencies' by inheritance.
    '''
    def __init__(self, G, max_removal_rate = 0.05, num_points = 20):
        '''
        Initializes the ToleranceSimulation with a graph, maximum removal rate, and number of points.

        Parameters:
        ----------
        G : networkx.Graph
            The input network graph.
        max_removal_rate : float, optional
            The maximum removal rate for the nodes (default is 0.05).
        num_points : int, optional
            The number of points for calculating the removal frequencies (default is 20).
        
        '''
        super().__init__(G, max_removal_rate, num_points)
        self.G = G
        
    def graph_property_vs_removals(self, property_function, removal_function):
        '''
        Calculates the specified graph property as a function of node removals.

        This function generates new versions of the input graph 'G', each subjected
        to a different node removal rates. The removals can be randomly (error) or 
        hierarchically (attack) selected depending on the 'removal_function'. 
        It then calculates the property of the graph, defined by 'property_function', for each modified 
        graph and returns the data for further analysis or plotting.

        Parameters
        ----------
        property_function : function
            A function that calculates a property of the graph.
        removal_function : function
            A function that removes nodes from the graph.

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
        property_values = []
        
        for i in self.num_removals_cleaned:
            G_modified = removal_function(self.G, i)
            property_values.append(property_function(G_modified))
         
        return self.frequencies_cleaned, property_values
    
class EpidemicData():
    '''
    A class to simulate the spread of an epidemic on a network using the SIR model.

    Attributes:
    ----------
    number_of_nodes : int
        The total number of nodes in the network.
    p_t : float
        The transmission probability.
    p_i : float
        The immunization probability.
    duration : int
        The duration of the epidemic simulation.
    infected_t0 : int
        The initial number of infected nodes.
    starting_state : numpy.ndarray
        The initial state of the nodes (infected or not).
    
    Methods:
    -------
    first_infection():
        Initializes the infection state by randomly infecting a set number of nodes.

    evolution_epidemy_SIR(G, plot_spread=False):
        Simulates the evolution of the epidemic using the SIR model.

    infection_with_for(G, state):
        Updates the infection state of the network using a for loop over discordant links.

    infection_without_for(G, state):
        Updates the infection state of the network using vectorized operations without a for loop.

    immunity(starting_state, final_state):
        Updates the state of the network by assigning immunity to infected nodes.

    '''
    def __init__(self, G, p_t, p_i, duration, infected_t0):
        '''
        Initializes the EpidemicData with the network and epidemic parameters.

        Parameters:
        ----------
        G : networkx.Graph
            The input network graph.
        p_t : float
            The transmission probability.
        p_i : float
            The immunization probability.
        duration : int
            The duration of the epidemic simulation.
        infected_t0 : int
            The initial number of infected nodes.
        '''
        self.number_of_nodes = nx.number_of_nodes(G)
        self.p_t = p_t
        self.p_i = p_i
        self.duration = duration
        self.infected_t0 = infected_t0
        self.starting_state = self.first_infection()
        
    def first_infection(self):
        '''
        Initializes the infection state by randomly infecting a set number of nodes.

        Returns:
        -------
        state : numpy.ndarray
            The array representing the initial infection state of the network.
        '''
        state = np.zeros(self.number_of_nodes)
        infected_index = np.random.randint(0, self.number_of_nodes, self.infected_t0)
        state[infected_index] = 1
        return state
    
    def evolution_epidemy_SIR(self, G, plot_spread = False):
        '''
        Simulates the evolution of the epidemic using the SIR model.
        
        This process relies on two assumptions: the infection and immunisation are
        binomial processes and the trasmission of the disease can only happen among 
        nodes that are connected. 

        Parameters:
        ----------
        G : networkx.Graph
            The input network graph.
            plot_spread : bool, optional
            If True, plots the spread of the epidemic over time (default is False).

       Returns:
       -------
       infection_rate : numpy.ndarray
           The array of infection rates over time.
       immunized_rate : numpy.ndarray
           The array of immunization rates over time.
        
       '''
        state = np.copy(self.starting_state) # to not work on the original starting state, but on its copy
        
        if plot_spread:
            pos = nx.kamada_kawai_layout(G)  # fixed layout for the graph
            node_colors = ['red' if self.starting_state[node] == 1 else 'green' if self.starting_state[node] == -1 else 'skyblue' for node in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_color=node_colors)
            plt.title("Time = 0, SIR model")
            plt.show() 
            
        infection_rate = []
        immunized_rate = []
        for i in range(1, self.duration + 1):
            
            infected_state = self.infection_with_for(G, state)
        
            immunized_state = self.immunity(state, infected_state)
            
            infection_rate.append(np.mean(immunized_state == 1))
            immunized_rate.append(np.mean(immunized_state == -1))
            
            state = immunized_state
            if plot_spread:
                node_colors = ['red' if immunized_state[node] == 1 else 'green' if immunized_state[node] == -1 else 'skyblue' for node in G.nodes()]
                nx.draw(G, pos, with_labels=True, node_color=node_colors)
                plt.title(f"Time = {i}")
                plt.show()
                
        return np.array(infection_rate), np.array(immunized_rate)
    
    # def recovery(self, starting_state, final_state):
        
    #     infected_nodes = np.where(starting_state == 1)
    #     recovery = np.random.binomial(1, self.p_r, len(infected_nodes[0])).astype(bool)
    #     recovered_nodes = infected_nodes[0][recovery]
    #     final_state[recovered_nodes] = 0
    #     return final_state
        
    def infection_with_for(self, G, state):
        '''
        Updates the infection state of the network.
        
        This function identifies the nodes that are currently susceptible and applies a binomial process
        to determine which of these nodes become infected. The infection can happen only among nodes that 
        are connected. Immunized nodes are then marked in the final state with a value of 1.

        Parameters:
        ----------
        G : networkx.Graph
            The input network graph.
        state : numpy.ndarray
            The current state of the nodes.

        Returns:
        -------
        state : numpy.ndarray
            The updated state of the nodes after infection.
        '''
        discordant_links = [(u, v) for u, v in G.edges() if state[u] + state[v] == 1]
        transmit = np.random.binomial(1, self.p_t, len(discordant_links))
            
        #Update the infection status
        for j, (u, v) in enumerate(discordant_links):
            if transmit[j]:
                state[u] = state[v] = 1 
        
        return state

    def infection_without_for(self, G, state):
        
         u, v = np.array(G.edges()).T
         discordant_mask = state[u] != state[v]
         discordant_edges = np.where(discordant_mask)[0]
            
         transmissions = np.random.binomial(1, self.p_t, len(discordant_edges))
         edges_to_update = discordant_edges[transmissions == 1]

         state[u[edges_to_update]] = 1
         state[v[edges_to_update]] = 1
         
         return state

    def immunity(self, starting_state, final_state):
        '''
        Updates the state of the network by assigning immunity to infected nodes.

        This function identifies the nodes that are currently infected and applies a binomial process
        to determine which of these nodes become immunized. Immunized nodes are then marked in the 
        final state with a value of -1.
        
        Parameters:
        ----------
        starting_state : numpy.ndarray
            The initial state of the network, where infected nodes are marked with a value of 1.
        final_state : numpy.ndarray
            The state of the network to be updated with immunized nodes.

        Returns:
        -------
        final_state : numpy.ndarray
            The updated state of the network, with immunized nodes marked as -1.

        '''
        
        infected_nodes = np.where(starting_state == 1)
        immunity = np.random.binomial(1, self.p_i, len(infected_nodes[0])).astype(bool)
        immunized_nodes = infected_nodes[0][immunity]
        final_state[immunized_nodes] = -1
        return final_state     

    
class EpidemicToleranceSimulation(GetRemotionFrequencies):
    '''
    A class to simulate the effect of node removals on epidemic spread in a network.

    This class extends the GetRemotionFrequencies class and integrates epidemic simulation 
    using the SIR model to study how the removal of nodes impacts the spread of an epidemic.

    Attributes:
    ----------
    G : networkx.Graph
        The input network graph.
    epidemic_data : EpidemicData
        An instance of EpidemicData to simulate the epidemic on the network.

    Methods:
    -------
    epidemic_property_vs_removals(property_function, removal_function, *args, **kwargs):
        Simulates the effect of node removals on the spread of the epidemic and calculates the 
        specified epidemic property as a function of node removal.
        
    Notes:
    -----
    This class is connected to 'GetRemotionFrequencies' by inheritance and to EpidemicData by 
    composition.
    '''
    def __init__(self, G, p_t, p_i, duration, infected_t0, max_removal_rate = 0.05, num_points = 20):
        '''
        Initializes the EpidemicToleranceSimulation with the network and epidemic parameters.

        Parameters:
        ----------
        G : networkx.Graph
            The input network graph.
        p_t : float
            The transmission probability.
        p_i : float
            The immunization probability.
        duration : int
            The duration of the epidemic simulation.
        infected_t0 : int
            The initial number of infected nodes.
        max_removal_rate : float, optional
            The maximum removal rate for the nodes (default is 0.05).
        num_points : int, optional
            The number of points for calculating the removal frequencies (default is 20).
        '''
        super().__init__(G, max_removal_rate, num_points)
        self.epidemic_data = EpidemicData(G, p_t, p_i, duration, infected_t0)
        self.G = G
        
        
    def epidemic_property_vs_removals(self, property_function, removal_function, *args, **kwargs):
        '''
        Simulates the effect of node removals on an epidemic and calculates the specified property.

        This method simulates the spread of an epidemic following the SIR model on a network after nodes are removed according 
        to a given 'removal_function'. It then evaluates a specified epidemic property at each removal stage.

        Parameters:
        ----------
        property_function : function
            A function that calculates a specific property of the epidemic (e.g., infection rate).
        removal_function : function
            A function that removes nodes from the network.
        *args : tuple
            Additional arguments to pass to the property function.
        **kwargs : dict
            Additional keyword arguments to pass to the property function.

        Returns:
        -------
        frequencies_cleaned : numpy.ndarray
            The cleaned array of frequencies corresponding to the removal rates.
        property_values : list
            The list of property values corresponding to each removal stage.
            
        Notes
        -----
        The property_function has some restrictions about its input: the code has been
        created for property functions that always work on the function of infection.
        Anyway, they can work even with the function of immunisation, without expliciting it,
        and/or others parameters which must be specified. 
        
        Examples
        --------
        >>> G = nx.erdos_renyi_graph(100, 0.05)
        >>> freq, duration = EpidemicToleranceSimulation(G, num_points = 5).epidemic_property_vs_removals(duration_epidemic, attack)
        >>> freq
        array([0.  , 0.01, 0.02, 0.03, 0.05])
        >>> duration
        ['Epidemic never started', 9, 9, 9, 9]
        '''
        # Ottieni la firma della property_function
        sig = inspect.signature(property_function)
        param_names = sig.parameters.keys()
        
        property_values = []
         
        for i in self.num_removals_cleaned:
            G_modified = removal_function(self.G, i)
            infected, immunized = self.epidemic_data.evolution_epidemy_SIR(G_modified)
            #property_values.append(property_function(infected))#check
            # Prepariamo gli argomenti da passare
            infected  # Sempre passiamo "infected"
            # Aggiungi immunized se richiesto dalla funzione
            if 'recovery_function' in param_names:
                result = property_function(infected, immunized, *args, **kwargs)
            else:
                result = property_function(infected, *args, **kwargs)
            
            property_values.append(result)
            
        return self.frequencies_cleaned, property_values
    
        
        

