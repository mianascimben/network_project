'''

This script define some useful functions to plot data using a predefined format 

'''

import numpy as np
import matplotlib.pyplot as plt
from simulation_tools.pdf_functions import exp_model, fit_data


def data_exponential_plot(x, y, errors=True, xlabel='x', ylabel='y', title='x v/s y'):
    '''
    Plots the probability density function of the node degrees.

    This function generates a log-log plot of the degree distribution of 
    in a graph. It plots the experimental data and overlays a theoretical 
    exponential model. The fit of the data to the exponential model is achieved 
    through the function 'fit_data()'.
    Optionally, it can also display error bands around the theoretical model 
    (set 3 sigma of confidence).

    Parameters:
    ----------
    x : array-like
        An array containing the degree of the node in a graph.
    y : array-like
        An array containing the frequency of each node degree in a graph.
    errors : bool, optional
        Whether to plot error bands around the theoretical model. The default is True.
    xlabel : str, optional
        The label for the x-axis. The default is 'x'.
    ylabel : str, optional
        The label for the y-axis. The default is 'y'.
    title : str, optional
        The title of the plot. The default is 'x v/s y'.

    Returns:
    -------
    fig : matplotlib.figure.Figure
        The matplotlib figure object containing the plot.
    ax : matplotlib.axes._axes.Axes
        The matplotlib Axes object containing the plot.

    '''
    parameters, pcov = fit_data(exp_model, x, y)
    alpha, beta = parameters
    
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = exp_model(x_fit, alpha, beta)  # Unpacks parameters as alpha and beta
    
    fig, ax = plt.subplots()
    ax.loglog(x, y, label='Experimental data', linestyle='none', marker='o')
    ax.loglog(x_fit, y_fit, color='red', label='Model')
    d_alpha, d_beta = np.sqrt(np.diag(pcov))
    
    if errors:        
        y_fit_up = exp_model(x_fit, alpha + 3*d_alpha, beta + 3*d_beta)
        y_fit_down = exp_model(x_fit, alpha - 3*d_alpha, beta - 3*d_beta)
        
        ax.fill_between(x_fit, y_fit_up, y_fit_down, alpha=0.5, label='Errors')
    
    ax.set_ylabel(ylabel, size=13)
    ax.set_xlabel(xlabel, size=13)
    ax.set_title(title, size=18)
    ax.legend()
    ax.grid(True)
    return fig, ax


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

def make_plot(freq, data_error, data_attack, ylabel, title):
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

