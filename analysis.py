<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 12:14:24 2024

@author: mima
"""

# network analysis

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import random
#upload data
adj = pd.read_csv('flight_graph.csv')

G = nx.from_pandas_edgelist(adj)

# get the degree from max to min and its frequence
G_deg = sorted((d for n,d in G.degree()),reverse=True)
G_deg_unique, freq = np.unique(G_deg, return_counts = True)
pdf = freq/(freq.sum())
# theorical model
def exp_model(data, alpha, beta):
    '''
    

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    alpha : TYPE
        DESCRIPTION.
    beta : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    return alpha*data**beta 

parameters, pcov = curve_fit(exp_model,G_deg_unique,pdf)
alpha, beta = parameters

x_fit = np.linspace(min(G_deg_unique), max(G_deg_unique), 100)
y_fit = exp_model(x_fit, alpha, beta)
#Errorbar addition (CHECK)
y_fit_up =  exp_model(x_fit, alpha+pcov[0][0], beta+pcov[1][1] )
y_fit_down = exp_model(x_fit, alpha-pcov[0][0], beta-pcov[1][1] )

# Visualization
plt.loglog(G_deg_unique, pdf, label='Sperimental data', linestyle='none', marker='o')
plt.loglog(x_fit, y_fit, color='red', label='Model')
plt.fill_between(x_fit, y_fit_up, y_fit_down, alpha=0.2, label = 'Errors')# (1/2 SIGMA?)
plt.ylabel('Pdf', size=13)
plt.xlabel('Degree', size=13)
plt.title('Flight degree pdf', size=18)
plt.legend()
plt.show()

diameter = nx.average_shortest_path_length(G) # the distances are kept all =1 otherwise weights

def error(G, n):
    '''
    

    Parameters
    ----------
    G : TYPE
        DESCRIPTION.
        
    n : TYPE
        DESCRIPTION.
        
    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    edges = list(G.edges())
    random_edges = random.sample(edges, n)
    G.remove_edges_from(random_edges)
    return G

def attack(G, n):
    '''
    

    Parameters
    ----------
    G : TYPE
        DESCRIPTION.
    
    n : TYPE
        DESCRIPTION.
        
    Returns
    -------
    None.

    '''

    degrees = dict(G.degree())
    top_n_nodes = sorted(degrees, key=degrees.get, reverse=True)[:n]
    return G.remove_node(top_n_nodes)






=======
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 12:14:24 2024

@author: mima
"""

# network analysis

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
#upload data
adj = pd.read_csv('flight_graph.csv')

G = nx.from_pandas_edgelist(adj)

# get the degree from max to min and its frequence
G_deg = sorted((d for n,d in G.degree()),reverse=True)
G_deg_unique, freq = np.unique(G_deg, return_counts = True)

# theorical model
def exp_model(data, alpha, beta):
    return alpha*data**beta 

parameters, pcov = curve_fit(exp_model,G_deg_unique,freq)
alpha, beta = parameters

x_fit = np.linspace(min(G_deg_unique), max(G_deg_unique), 100)
y_fit = exp_model(x_fit, alpha, beta)
#Errorbar addition
y_fit_up =  exp_model(x_fit, alpha+pcov[0][0], beta+pcov[1][1] )
y_fit_down = exp_model(x_fit, alpha-pcov[0][0], beta-pcov[1][1] )

# Visualization
plt.loglog(G_deg_unique, freq, label='Sperimental data', linestyle='none', marker='o')
plt.loglog(x_fit, y_fit, color='red', label='Model')
plt.fill_between(x_fit, y_fit_up, y_fit_down, alpha=0.2, label = 'Errors')#errors 
plt.ylabel('Pdf', size=13)
plt.xlabel('Degree', size=13)
plt.title('Flight degree pdf', size=18)
plt.legend()
plt.show()


