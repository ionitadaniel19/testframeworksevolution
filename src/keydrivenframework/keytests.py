'''
Created on 01.06.2014

@author: ionitadaniel19
'''
from mapkeywords import *
from config.utilities import *
from config.constants import *

#keyword_driven_dict={FRAMEWORK_FUNCTIONS:'',PARAMETERS:[],PAGE_WINDOW:'',LOCATOR:''}

def show_answer_keydriven(driver,scenario):
    actual_answer=None
    validate=False
    data_keywords=get_keywords_driven_scenario_values(scenario)
    for data_keys in data_keywords:
        if data_keys[FRAMEWORK_FUNCTIONS]==GET_TEXT:
            actual_answer=call_map_keyword(data_keys,driver)
        elif data_keys[FRAMEWORK_FUNCTIONS]==VALIDATE:
            validate=call_map_keyword(data_keys,actual_answer)
        else:
            call_map_keyword(data_keys,driver)
    return validate,actual_answer