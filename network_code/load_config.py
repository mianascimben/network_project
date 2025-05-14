'''
    Import of the global variables from 'constants.txt' and declare new global variables
'''

import configparser
from graph_property_functions import total_infected, epidemic_duration, peak, t_peak

def load_config(path="constants.txt"):
    config = configparser.ConfigParser()
    config.read(path)

    return {
        "N": int(config["network"]["N"]),
        "P": float(config["network"]["P"]),
        "MAX_REMOVAL_RATE": float(config["network"],["MAX_REMOVAL_RATE"]),
        "SEED": int(config["random"]["SEED"]),
        "MU": float(config["epidemic"]["MU"]),
        "NU": float(config["epidemic"]["NU"]),
        "DURATION": int(config["epidemic"]["DURATION"]),
        "INFECTED_T0": int(config["epidemic"]["INFECTED_T0"]),
        "NUM_POINTS": int(config["epidemic"]["NUM_POINTS"]),
        "NUM_SIMULATIONS": int(config["epidemic"]["NUM_SIMULATIONS"])
    }

EPIDEMIC_FUNCS = {
    'total_infected': [total_infected, 'Fraction of total infected cases'],
    'duration': [epidemic_duration, 'Epidemic Duration'],
    't_peak': [t_peak, 't_peak'],
    'peak': [peak, 'Infection Peak']
}