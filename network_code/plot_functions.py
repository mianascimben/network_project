'''

This script define some useful functions to plot data using a predefined format 

'''

import matplotlib.pyplot as plt
import networkx as nx
import time

def plot_multiple_data(x_data, y_data, labels, colors=None, markers=None, linestyles=None,
                       ylabel='y', xlabel='x', title='x v/s y'):
    '''
    Plots multiple data series on the same figure.

    Parameters:
    ----------
    x_data : list of array-like
        A list containing the x-coordinates of each data series.
    y_data : list of array-like
        A list containing the y-coordinates of each data series.
    labels : list of str
        A list of labels for the data series.
    colors : list of str, optional
        A list of colors for the data series. Defaults to None (automatic color selection).
    markers : list of str, optional
        A list of markers for the data series. Defaults to None (no markers).
    linestyles : list of str, optional
        A list of linestyles for the data series. Defaults to None (solid lines).
    ylabel : str, optional
        The label for the y-axis. Default is 'y'.
    xlabel : str, optional
        The label for the x-axis. Default is 'x'.
    title : str, optional
        The title of the plot. Default is 'x v/s y'.

    Returns:
    -------
    fig : matplotlib.figure.Figure
        The matplotlib figure object containing the plot.
    ax : matplotlib.axes._axes.Axes
        The matplotlib Axes object containing the plot.

    '''
    fig, ax = plt.subplots()
    
    # Iterate over each data series and plot
    for i, (x, y) in enumerate(zip(x_data, y_data)):
        color = colors[i] if colors else None
        marker = markers[i] if markers else None
        linestyle = linestyles[i] if linestyles else None
        ax.plot(x, y, label=labels[i], color=color, marker=marker, linestyle=linestyle)
    
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(True)
    
    return fig, ax

def make_plot(freq, data_error, data_attack, ylabel, title, **kwargs):
    """
    Generates a 2-line plot comparing the effect of random errors and targeted 
    attacks on a given network metric across node removal frequencies.

    Parameters
    ----------
    freq : array-like
        Array of node removal frequencies.

    data_error : array-like
        Metric values under random errors.

    data_attack : array-like
        Metric values under targeted attacks.

    ylabel : str
        Label for the y-axis (e.g., "Diameter", "Total Infected").

    title : str
        Title of the plot.
    
    **kwargs : dict
        Parameters used in the creation of the network and/or the epidedemic 
        simulation 
    
    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure object containing the plot.

    ax : matplotlib.axes.Axes
        The axes object for further customization or saving.
    """
    fig, ax = plot_multiple_data(
        x_data = [freq, freq],
        y_data = [data_error, data_attack],
        labels = ['error','attack'],
        colors = ['blue', 'red'],
        markers = ['o','o'],
        linestyles = ['-','-'],
        ylabel = ylabel, xlabel='Frequency',
        title = title
        )
    return fig, ax


def make_plot_fragmentation(freq, S_error, S_attack, s_error, s_attack,  ylabel, title):
    """
    Generates a 4-line plot showing the structural fragmentation of a network under
    random errors and targeted attacks. Plots both:
    - S: Size of the largest connected component
    - <s>: Average size of the remaining connected components
    
    Parameters
    ----------
    freq : array-like
        Array of node removal frequencies.
    
    S_error : array-like
        Size of the largest component under random errors.
    
    S_attack : array-like
        Size of the largest component under targeted attacks.
    
    s_error : array-like
        Average size of smaller components under random errors.
    
    s_attack : array-like
        Average size of smaller components under targeted attacks.
    
    ylabel : str
        Label for the y-axis (e.g., "S, <s>").
    
    title : str
        Title of the plot.
    
    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure object containing the plot.
    
    ax : matplotlib.axes.Axes
        The axes object for further customization or saving.
    """
    fig, ax = plot_multiple_data(
            x_data = [freq, freq, freq, freq], 
            y_data = [S_error, S_attack, s_error, s_attack],  
            labels = ['S vs error', 'S vs attack', '<s> vs error', '<s> vs attack'],
            colors = ['blue', 'red', 'blue', 'red'],
            markers = ['o', 'o', 's', 's'],
            linestyles = ['--', '--', '-', '-'],
            ylabel = ylabel, xlabel = 'Frequency',
            title = title
            )
    return fig, ax

def make_plot_2networks(freq, data_error_ER, data_attack_ER, data_error_SF, data_attack_SF, 
                        ylabel, title):
    """
    Generates a 4-line plot to comparethe impact of errors and attacks on two networks
    (typically ER and SF). Plots:
    - Error and attack effects on ER network
    - Error and attack effects on SF network

    Parameters
    ----------
    freq : array-like
        Array of node removal frequencies.

    data_error_ER : array-like
        Metric values for ER network under random errors.

    data_attack_ER : array-like
        Metric values for ER network under targeted attacks.

    data_error_SF : array-like
        Metric values for SF network under random errors.

    data_attack_SF : array-like
        Metric values for SF network under targeted attacks.

    ylabel : str
        Label for the y-axis (e.g., "Diameter", "Total Infected").

    title : str
        Title of the plot.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure object containing the plot.

    ax : matplotlib.axes.Axes
        The axes object for further customization or saving.
    """
    
    fig, ax = plot_multiple_data(x_data = [freq, freq, freq, freq], 
                    y_data = [data_error_ER, data_attack_ER, data_error_SF, data_attack_SF],  
                    labels = ['error on ER', 'attack on ER', 'error on SF', 'attack on SF'],
                    colors = ['blue', 'red', 'blue', 'red'],
                    markers = ['o', 'o', 's', 's'],
                    linestyles = ['--', '--', '-', '-'],
                    ylabel = ylabel, xlabel = 'Frequency',
                    title = title
                    )
    return fig, ax

def display_epidemic(graph, states, layout):
    '''
    Displays the graph structure with the nodes colors representing their state
    at each time step:
        red nodes: infected state
        green nodes: recovered state
        blue nodes: susceptible state

    Parameters
    ----------
    graph : networkx.classes.graph.Graph
        The graph on which the epidemic is run.
    
    states : np.array or list
         Each element of the `states` can be (-1,0,1). It stores the states of 
         the network nodes.
         That means: if the first element is `0`, then the node labeled as 'zero'
         is healthy.
         
    layout : dict
        Fixes the layout/disposition of the graph
         
    Returns
    -------
    None.
    
    Note: 
    -----
    The plot is not returned as a figure but directly shown up.

    '''
    node_colors = ['red' if states[node] == 1 else 'green' if states[node] == -1 else 'skyblue' for node in graph.nodes()]
    nx.draw(graph, layout, with_labels=True, node_color=node_colors)
    plt.title(f"Time = {time}, SIR model")
    plt.show() 
    
    

