'''
    This scripts contains the tests for the functions in 'epidemic_functions'
'''
import pytest
import numpy as np

from network_code.analysis_functions import peak, t_peak, epidemic_duration, total_infected


@pytest.fixture
def array_1D():
    return np.array([10, 12, 25, 46, 67])

@pytest.fixture
def array_2D():
    return np.array([[10, 34, 2, 25], [30, 5, 1, 3]])

class TestPeak:
    
    def test_peak_1D(self, array_1D):
        ''' This functions test that the 'peak' function works in 1D'''
        expected = np.max(array_1D)
        assert peak(array_1D) == expected
    
    def test_peak_2D(self, array_2D):
        ''' This functions test that the 'peak' function works in 2D'''
        expected = np.mean(np.max(array_2D, axis = 1)) 
        assert peak(array_2D) == expected
        
    def test_peak_valid_output_1D(self, array_1D):
        ''' This function check that the output of peak is a number
        
        GIVEN: a valid 1D array
        WHEN: I apply to it the 'peak' function
        THEN: the resulting state is a single number (int or float)
        '''
        output = peak(array_1D)
        assert isinstance(output, (int, float, np.integer, np.floating))
        
    def test_peak_valid_output_2D(self, array_2D):
        ''' This function check that the output of peak is a number
        
        GIVEN: a valid 2D array
        WHEN: I apply to it the 'peak' function
        THEN: the resulting state is a single number (int or float)
        '''
        output = peak(array_2D)
        assert isinstance(output, (int, float, np.integer, np.floating))

class TestTPeak:
    
    def test_tpeak_1D(self, array_1D):
        ''' This functions test that the 't_peak' function works in 1D'''
        expected = np.argmax(array_1D)
        assert t_peak(array_1D) == expected
        
    def test_tpeak_2D(self, array_2D):
        ''' This functions test that the 't_peak' function works in 2D'''
        
        expected = np.mean(np.argmax(array_2D, axis=1))
        assert t_peak(array_2D) == expected
        
    def test_tpeak_valid_output_1D(self, array_1D):
        ''' This function check that the output of 't_peak' is a number
        
        GIVEN: a valid 1D array
        WHEN: I apply to it the 't_peak' function
        THEN: the resulting state is a single number (int or float)
        '''
        output = t_peak(array_1D)
        assert isinstance(output, (int, float, np.integer, np.floating))
        
    def test_tpeak_valid_output_2D(self, array_2D):
        ''' This function check that the output of 't_peak' is a number
        
        GIVEN: a valid 2D array
        WHEN: I apply to it the 't_peak' function
        THEN: the resulting state is a single number (int or float)
        '''
        output = t_peak(array_2D)
        assert isinstance(output, (int, float, np.integer, np.floating))

class TestDuration:
    
    def test_duration_1D(self, array_1D):
        ''' This functions test that the 'epidemic_duration' function works in 1D'''
        
        expected = np.count_nonzero(array_1D)
        assert epidemic_duration(array_1D) == expected
        
    def test_duration_2D(self, array_2D):
        ''' This functions test that the 'epidemic_duration' function works in 2D'''
        expected = np.mean(np.count_nonzero(array_2D, axis=1))
        assert epidemic_duration(array_2D) == expected
        
    def test_duration_valid_output_1D(self, array_1D):
        ''' This function check that the output of 'epidemic_duration' is a number
        
        GIVEN: a valid 1D array
        WHEN: I apply to it the 'epidemic_duration' function
        THEN: the resulting state is a single number (int or float)
        '''
        output = epidemic_duration(array_1D)
        assert isinstance(output, (int, float, np.integer, np.floating))
        
    def test_duration_valid_output_2D(self, array_2D):
        ''' This function check that the output of 'epidemic_duration' is a number
        
        GIVEN: a valid 2D array
        WHEN: I apply to it the 'epidemic_duration' function
        THEN: the resulting state is a single number (int or float)
        '''
        output = epidemic_duration(array_2D)
        assert isinstance(output, (int, float, np.integer, np.floating))
class TestTotalInfected:
    def test_total_infected_1D(self):
        ''' This functions test that the 'total_infected' function works in 1D'''
        array1 = np.array([2,4,7,9,3])
        array2 = np.array([0,1,4,7,12])
        expected = array1[-1] + array2[-1]
        assert total_infected(array1, array2) == expected
        
    def test_total_infected_2D(self):
        ''' This functions test that the 'total_infected' function works in 2D'''
        array1 = np.array([[2,4,7,9,3], [2,7,3,2,0]])
        array2 = np.array([[0,1,4,7,12], [0,3,4,10,10]])
        expected = np.mean(array1[:,-1] + array2[:,-1])
        assert total_infected(array1, array2) == expected
    
    def test_tot_infected_valid_output_1D(self, array_1D):
        ''' This function check that the output of 'total_infected' is a number
        
        GIVEN: a valid 1D array
        WHEN: I apply to it the 'total_infected' function
        THEN: the resulting state is a single number (int or float)
        '''
        array1 = np.array([[2,4,7,9,3], [2,7,3,2,0]])
        array2 = np.array([[0,1,4,7,12], [0,3,4,10,10]])
        output = total_infected(array1, array2)
        assert isinstance(output, (int, float, np.integer, np.floating))
        
    def test_tot_infected_valid_output_2D(self, array_2D):
        ''' This function check that the output of 'total_infected' is a number
        
        GIVEN: a valid 2D array
        WHEN: I apply to it the 'total_infected' function
        THEN: the resulting state is a single number (int or float)
        '''
        array1 = np.array([[2,4,7,9,3], [2,7,3,2,0]])
        array2 = np.array([[0,1,4,7,12], [0,3,4,10,10]])
        output = total_infected(array1, array2)
        assert isinstance(output, (int, float, np.integer, np.floating))
    
