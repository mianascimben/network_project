# -*- coding: utf-8 -*-
"""

    Tests for the constant.py script
    
"""

import pytest 
from network_code.constants import EPIDEMICS_FUNCS
from network_code.analysis_functions import  peak, t_peak, epidemic_duration, total_infected

def test_EPIDEMICS_FUNCS_is_dictionary():
    assert isinstance(EPIDEMICS_FUNCS, dict)
    
def test_epidemics_funcs_keys():
    expected_keys = {'peak', 't_peak', 'duration', 'total_infected'}
    assert set(EPIDEMICS_FUNCS.keys()) == expected_keys
    
def test_epidemics_funcs_peak_function_mapping():
    assert EPIDEMICS_FUNCS['peak'][0] is peak
    
def test_epidemics_funcs_tpeak_function_mapping():
    assert EPIDEMICS_FUNCS['t_peak'][0] is t_peak
    
def test_epidemics_funcs_duration_function_mapping():
    assert EPIDEMICS_FUNCS['duration'][0] is epidemic_duration
    
def test_epidemics_funcs_infected_function_mapping():
    assert EPIDEMICS_FUNCS['total_infected'][0] is total_infected