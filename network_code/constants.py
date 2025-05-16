from simulation_tools.graph_property_functions import peak, t_peak, epidemic_duration, total_infected

EPIDEMICS_FUNCS = {
    'peak': [peak, 'Infection peak'],
    't_peak': [t_peak, 't_peak'],
    'duration': [epidemic_duration, 'Epidemic duration'],
    'infected': [total_infected, 'Fraction of total infected cases']
    }
