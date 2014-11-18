'''
Created on 01.06.2014

@author: ionitadaniel19
'''

def show_answer_datadriven(driver,scenario=1):
    from modularframework.login import LoginPage
    from modularframework.testframeworks import TestFrameworksPage
    from config.utilities import get_data_driven_scenario_values
    from config.constants import *
    data_test=get_data_driven_scenario_values(scenario)
    login_page=LoginPage(driver)
    login_page.login(data_test[CELL_USER], data_test[CELL_PWD])
    test_framework_page=TestFrameworksPage(driver)
    test_framework_page.select_answer(data_test[CELL_ANSWER])
    actual_answer=test_framework_page.show_answer()
    expected_answer=data_test[CELL_EXPECTED]
    return actual_answer,expected_answer