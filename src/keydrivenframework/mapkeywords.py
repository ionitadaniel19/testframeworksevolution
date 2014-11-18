'''
Created on 07.06.2014

@author: ionitadaniel19
'''

from config.constants import *
from config.constants import PARAMETERS
import keywords
from objectlibrary import map_selenium_objects

map_selenium_keywords={
                       "OPEN":"open_page",
                       "CLICK":"click_wait",
                       "GET_TEXT":"get_text",
                       "WAIT":"wait_element",
                       "TYPE":"type_text",
                       "VALIDATE":"validate_answer"
                       }

def call_function_args(module,function_name,*args):
    keywords_functions=getattr(__import__(module), function_name)
    return  keywords_functions(*args)

#arguments in a list form
def call_function_args_list(module,function_name,args):
    #keywords_functions=getattr(__import__(module), function_name)
    keywords_functions=getattr(module, function_name)
    return  keywords_functions(*args)

def call_keyword_function(function_name,args):
    if function_name in map_selenium_keywords:
        return call_function_args_list(keywords,map_selenium_keywords[function_name],args)
    
def call_map_keyword(data_function,*args):
    #map the keywords for locators to selenium locators
    if data_function[LOCATOR] in map_selenium_objects:
        data_function[LOCATOR]=map_selenium_objects[data_function[LOCATOR]]
        
    if data_function[FRAMEWORK_FUNCTIONS]==CLICK:
        data_function[PARAMETERS]=[data_function[LOCATOR]]+data_function[PARAMETERS]
    elif data_function[FRAMEWORK_FUNCTIONS]==GET_TEXT:
        data_function[PARAMETERS]=[data_function[LOCATOR]]+data_function[PARAMETERS]
    elif data_function[FRAMEWORK_FUNCTIONS]==WAIT:
        data_function[PARAMETERS]=[data_function[LOCATOR]]+data_function[PARAMETERS]
    elif data_function[FRAMEWORK_FUNCTIONS]==TYPE:
        data_function[PARAMETERS]=[data_function[LOCATOR]]+data_function[PARAMETERS]
    elif data_function[FRAMEWORK_FUNCTIONS]==OPEN:
        #no changes here
        pass
    elif data_function[FRAMEWORK_FUNCTIONS]==VALIDATE:
        #no changes here
        pass
    else:
        raise Exception('Function name %s not found in the mapping of functions %s' %(data_function[FRAMEWORK_FUNCTIONS],map_selenium_keywords))
    
    #add the optional arguments at the beginning of the argument list
    for arg in args:
        if isinstance(arg, list):
            arg_list=arg
        else:
            arg_list=[arg] 
        data_function[PARAMETERS]=arg_list+data_function[PARAMETERS]
    
    return call_keyword_function(data_function[FRAMEWORK_FUNCTIONS],data_function[PARAMETERS])
    