'''
Created on 21.05.2014

@author: ionitadaniel19
'''
from config.utilities import setup_logging,get_data_driven_scenario_values,get_simple_hybrid_driven_scenario_values,get_keywords_driven_scenario_values
import unittest
from utests import FrameworkTests

def test_recording(desired_test,desired_browser,test_data=None):
    desired_url='http://localhost:81/autframeworks/'
    testtorun=FrameworkTests(desired_test, desired_browser, desired_url,test_data)
    suite = unittest.TestSuite()
    suite.addTest(testtorun)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    setup_logging()
    #testrecordplayback
    test_recording('test_recordplayback','firefox')
    
    #testrmodularframework
    test_recording('test_modularframework','ie')
    
    #testdataframework
    test_recording('test_dataframework','chrome')
    
    #testkeywordframework
    test_recording('test_keywordframework','firefox')
    
    #test_hybridframework
    test_recording('test_hybridframework','chrome',1)