
"""
Created on Thu Jun 20 09:13:43 2024

@author: mima

This code comprehends the plots of the analysis.
"""
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from functions import exp_model
from functions import fit_data

#this has to be fixed, I m not sure we need it. 
# def network_plot(G, draw_edges = True):
#     '''
#     Visualization of the network passed as input.
    
#     The figure represents a scatter plot of the network nodes
#     with the optional addiction of edges.
    
#     Prameters 
#     ---------
#     G : networkx.classes.graph.Graph
#         Input graph to be visualized
#     draw_edges : boolean, optional.
#         Whether to draw network edges. The default is True. 
#     Returns
#     -------
#     fig: plot of the network in input in a scatter plot.
#     '''
    
#     fig = plt.scatter('Longitude', 'Latitude', data = airports_clean, s=8,)
    
#     if draw_edges:
#         nx.draw(G, air_pos, node_color='blue', edge_color='gray', node_size=10)
    

def data_fitting_plot(x, y, model, errors=True, ylabel='y', xlabel='x', title='x v/s y'):
    '''
    Plots the probability density function (frequency) of the node degrees.

    This function generates a log-log plot of the degree distribution of nodes in a graph. 
    It plots the experimental data and overlays a theoretical model based on the provided parameters.
    Optionally, it can also display error bands around the theoretical model (3 sigma confidence).

    Parameters
    ----------
    x : array-like
        Indipendent variable.
    y : array-like
        Dependent variable.
    model: callable
        The model function to fit.
    errors : bool, optional
        Whether to plot error bands around the theoretical model. The default is True.
    ylabel : str, optional
        The label for the y-axis. The default is 'y'.
    xlabel : str, optional
        The label for the x-axis. The default is 'x'.
    title : str, optional
        The title of the plot. The default is 'x v/s y'.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The matplotlib figure object containing the plot.

    Examples
    --------
    >>> G = nx.scale_free_graph(N,seed = 10)
    >>> degree, frequency = frequency_degree(G)
    >>> fig = pdf_degree_plot(degree, frequency)
    >>> plt.show()
    '''
    parameters, pcov = fit_data(exp_model, x, y)
    alpha, beta = parameters
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = exp_model(x_fit, alpha, beta)  # Unpacks parameters as alpha and beta

    fig, ax = plt.subplots()
    ax.loglog(x, y, label='Experimental data', linestyle='none', marker='o')
    ax.loglog(x_fit, y_fit, color='red', label='Model')
    
    if errors:        
        y_fit_up = exp_model(x_fit, alpha + 3*np.sqrt(pcov[0][0]), beta + 3*np.sqrt(pcov[1][1]))
        y_fit_down = exp_model(x_fit, alpha - 3*np.sqrt(pcov[0][0]), beta - 3*np.sqrt(pcov[1][1]))
        
        ax.fill_between(x_fit, y_fit_up, y_fit_down, alpha=0.5, label='Errors')
    
    ax.set_ylabel(ylabel, size=13)
    ax.set_xlabel(xlabel, size=13)
    ax.set_title(title, size=18)
    ax.legend()
    ax.grid(True)
    return fig

import matplotlib.pyplot as plt

def diameter_error_attack_plot(x1, y1, label1 = 'data1', data2=False, x2=[], y2=[], label2 ='data2', ylabel='y', xlabel='x', title='x v/s y'):
    '''
    Plots the primary data '(x1, y1)' and, optionally, secondary data '(x2, y2)' if provided.

    This function generates a plot comparing the diameters for networks that have benn 
    subjected to errors or attacks. The x and y axis are the outputs of the functions 
    'diameter_vs_error()' and 'diameter_vs_attack()'.
    

    Parameters
    ----------
    x1 : array-like
        The x-coordinates of the primary data points. The first output of 'diameter_vs_error/attack()'
    y1 : array-like
        The y-coordinates of the primary data points. The second output of 'diameter_vs_error/attack()'
    label1 : str, optional
        The label for the primary data data points. The default is 'data1'.
    data2 : bool, optional
        If True, plots the secondary data. The default is False.
    x2 : array-like, optional
        The x-coordinates of the secondary data points. The default is an empty list.
    y2 : array-like, optional
        The y-coordinates of the secondary data points. The default is an empty list.
    label2 : str, optional
        The label for the secondary data data points. The default is 'data2'.
    ylabel : str, optional
        The label for the y-axis. The default is 'y'.
    xlabel : str, optional
        The label for the x-axis. The default is 'x'.
    title : str, optional
        The title of the plot. The default is 'x v/s y'.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The matplotlib figure object containing the plot.

    Examples
    --------
    >>> x1 = [1, 2, 3, 4]
    >>> y1 = [10, 20, 25, 30]
    >>> x2 = [1, 2, 3, 4]
    >>> y2 = [12, 22, 27, 35]
    >>> fig = diameter_error_attack_plot(x1, y1, data2=True, x2=x2, y2=y2, ylabel='Diameter', xlabel='Errors', title='Diameter Error vs Attack')
    >>> plt.show()
    '''
    fig, ax = plt.subplots()
    
    ax.plot(x1, y1, label = label1, color='blue', marker='o')
    
    if data2:
        ax.plot(x2, y2, label = label2, color='red', marker='o')
    
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(True)
    
    return fig
