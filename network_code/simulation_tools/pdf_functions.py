'''

This script contains some useful functions for calculating the degree pdf of networks

'''
import numpy as np
from scipy.optimize import curve_fit

def degree_pdf(G):
    '''
    This function calculate the degree pdf of the input graph 'G'.

    Parameters
    ----------
    G : networkx.classes.graph.Graph
        The input graph.

    Returns
    -------
    degree_unique : numpy.ndarray
        An array with the values of the degree of the nodes of 'G' 
        in ascending oreder. The are no repeated values.
             
    pdf_n : numpy.ndarray
        An array representing the pdf of the degree. 
    '''
    
    # Get the degrees from the graph
    degree_G = G.degree()
    degree_dict = dict(degree_G)
    degree_list = sorted(degree_dict.items())
    
    # Get the degree frequencies
    _,degree = zip(*degree_list)
    degree_unique, pdf =np.unique(degree, return_counts=True)
    
    # Normalization of the frequencies of the degrees to get the pdf
    n = sum(pdf)
    pdf_n = 1/n * pdf
    
    return degree_unique, pdf_n


def fit_data(f, x, y):
    '''
    Use non-linear least squares to fit a function, f, to data.

    This function utilizes the `curve_fit` function from the `scipy.optimize`
    module to fit the provided model function `f` to the data points `x` and `y`.
    It returns the optimal parameters and the estimated covariance of the 
    parameters.

    Parameters
    ----------
    f : function
        The model function, f(x,...) to fit. It should take the independent 
        variable as the first argument and the parameters to fit as separate 
        remaining arguments.
    x : array-like
        The independent variable.
    y : array-like
        The dependent data.

    Returns
    -------
    popt : array
        Optimal values for the parameters such that the sum of the squared 
        residuals is minimized.
    pcov : 2-D array
        The estimated covariance of popt. The diagonals provide the variance 
        of the parameter estimate. 
        
    Notes:
    -----
    To compute one standard deviation errors of the parameters, use 
    `np.sqrt(np.diag(pcov))`.

    Examples
    --------
    >>> def model(x, a, b):
    ...     return a * np.exp(b * x)
    >>> x = np.array([1, 2, 3, 4])
    >>> y = np.array([2.7, 7.4, 20.1, 55.6])
    >>> popt, pcov = fit_data(model, x, y)
    >>> print(popt)
    [1. 2.]
    '''
    popt, pcov = curve_fit(f, x, y)
    return popt, pcov


def exp_model(data, alpha, beta):
    '''
    Return the exponential of the input data.

    This function computes the value of the expression `alpha * data ^ (beta)`,
    where `alpha` and `beta` are parameters of the model.

    Parameters
    ----------
    data : numeric or array-like
        The input data to which the exponential model is applied. This can be a 
        single numeric value or an array-like structure 
        (such as a list or numpy array) containing multiple numeric values.
    alpha : numeric
        The coefficient parameter of the exponential model. It scales the 
        result of the power transformation.
    beta : numeric
        The exponent parameter of the exponential model. It determines the 
        power to which each element in `data` is raised.

    Returns
    -------
    numeric or array-like
        The output of the exponential function, computed as `alpha * data ** beta`.
        If `data` is a single numeric value, the return will be a single numeric 
        value. If `data` is array-like, the return will be an array-like structure
        of the same shape containing the computed values.
    '''
    return alpha * data ** beta
