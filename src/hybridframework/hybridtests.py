'''
Created on 01.06.2014

@author: ionitadaniel19
'''
def show_answer_hybrid_simple(driver,scenario):
    from modularframework.login import LoginPage
    from modularframework.testframeworks import TestFrameworksPage
    from config.utilities import get_simple_hybrid_driven_scenario_values
    from config.constants import *
    data_test=get_simple_hybrid_driven_scenario_values(scenario)
    login_page=None
    test_framework_page=None
    actual_answer=None
    for data_function in data_test:
        if data_function[FRAMEWORK_FUNCTIONS]==CELL_F_REMEMBER_ME:
            if login_page is None:
                login_page=LoginPage(driver)
            login_page.remember_me()   
        if data_function[FRAMEWORK_FUNCTIONS]==CELL_F_LOGIN:
            if login_page is None:
                login_page=LoginPage(driver)
            if len(data_function[PARAMETERS])==2:
                username=data_function[PARAMETERS][0]
                pwd=data_function[PARAMETERS][1]
                login_page.login(username, pwd)
            else:
                raise Exception('For function %s there were not enough parameters specified %s.Expected 2.' %(data_function[FRAMEWORK_FUNCTIONS],data_function[PARAMETERS]))     
        if data_function[FRAMEWORK_FUNCTIONS]==CELL_F_SELECT_ANSWER:
            if test_framework_page is None:
                test_framework_page=TestFrameworksPage(driver)
            if len(data_function[PARAMETERS])==1:
                answer=data_function[PARAMETERS][0]
                test_framework_page.select_answer(answer)
            else:
                raise Exception('For function %s there were not enough parameters specified %s.Expected 1.' %(data_function[FRAMEWORK_FUNCTIONS],data_function[PARAMETERS]))
        if data_function[FRAMEWORK_FUNCTIONS]==CELL_F_SHOW_ANSWER:
            if test_framework_page is None:
                test_framework_page=TestFrameworksPage(driver)
            actual_answer=test_framework_page.show_answer()
    return actual_answer