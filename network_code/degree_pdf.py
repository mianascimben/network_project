'''

This script aims to display degree distribution for the global air traffic graph.

''' 

import pickle
import numpy as np
from simulation_tools.pdf_functions import exp_model, fit_data, degree_pdf
from simulation_tools.plot_functions import data_exponential_plot

with open('flight.gpickle', 'rb') as f:
    flight_net = pickle.load(f)

degree, pdf = degree_pdf(flight_net)

# Not consider the first term when performing the fit,
# because it doesn't follow the exponential model
degree_1 = degree[1:]
pdf_1 = pdf[1:]

# Use non-linear least squares to fit the exponential function to the data
fit = fit_data(exp_model, degree_1, pdf_1)
# and get the errors of the parameters
std_dev = np.sqrt(np.diag(fit[1]))

fig, ax = data_exponential_plot(degree_1, pdf_1, errors=True ,ylabel='Pdf', xlabel='Degree (k)', title='Degree distribution')
ax.plot(degree[0], pdf[0], linestyle = 'none', marker = 'o', color = 'royalblue')

