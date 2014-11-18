'''
Created on 24.05.2014

@author: ionitadaniel19
'''
import logging.config
import os 
import json
from xlsmanager import easyExcel
from constants import *
import traceback
import copy

def setup_logging(default_path='logging.json', default_level=logging.INFO,env_key='LOG_CFG'):
    """Setup logging configuration"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),default_path)

    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'r') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def load_browser_driver(browser_driver_path):
    """Setup browser driver configuration"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),browser_driver_path)

def get_webdriver_selector_element(element_name):
    element=None
    selector=None
    
    if element_name.startswith("css="):
        element = element_name.split('=', 1)[-1]
        selector= SELECTOR_CSS    
    elif element_name.startswith("xpath=") or element_name.startswith("//"):
        element = element_name.split('=', 1)[-1]
        selector= SELECTOR_XPATH 
    elif element_name.startswith("id="):
        element = element_name.split('=', 1)[-1]
        selector= SELECTOR_ID
    elif element_name.startswith("link="):
        element = element_name.split('=', 1)[-1]
        selector= SELECTOR_LINK
    elif element_name.startswith("name=") or element_name.find("=") == -1:
        element = element_name.split('=', 1)[-1]
        selector= SELECTOR_NAME
    elif element_name.startswith("class="):
        element = element_name.split('=', 1)[-1]
        selector= SELECTOR_CLASS
    elif element_name.startswith("tag="):
        element = element_name.split('=', 1)[-1]
        selector= SELECTOR_TAG
    else:
        raise Exception("Incorrect element %s.It should be one of type:css,xpath,id,link,name,class,tag." %element_name)
    
    return (selector,element)

def get_data_driven_scenario_values(scenario_id=1,xls_file=DEF_DATA_PATH,sheet_name="Data"):
    data_xls_keys_cols={'scenario':1,'login':2,'select':4}
    data_driven_data={CELL_USER:'',CELL_PWD:'',CELL_ANSWER:'',CELL_EXPECTED:''}
    try:
        xls_sheet=easyExcel(xls_file,sheet_name)
        last_row=xls_sheet.get_sheet_last_row(sheet_name)
        found=False
        scenario_row=0
        for row in range(1,last_row):
            if xls_sheet.getCell(row,data_xls_keys_cols['scenario'])==scenario_id:
                found=True
                scenario_row=row
                break
        if found is False:
            raise Exception('Scenarion %s not found in xls file %s sheet %s' %(scenario_id,xls_file,sheet_name))
            
        #stop at finding blank value or exit at index 5
        for index_row in range(scenario_row,scenario_row+5):
            if xls_sheet.getCell(index_row,data_xls_keys_cols['login'])==None:
                break
            
            if xls_sheet.getCell(index_row,data_xls_keys_cols['login'])==CELL_USER:
                #actual values is one column to the right
                data_driven_data[CELL_USER]=xls_sheet.getCell(index_row,data_xls_keys_cols['login']+1)
            if xls_sheet.getCell(index_row,data_xls_keys_cols['login'])==CELL_PWD:
                data_driven_data[CELL_PWD]=xls_sheet.getCell(index_row,data_xls_keys_cols['login']+1)
            if xls_sheet.getCell(index_row,data_xls_keys_cols['select'])==CELL_ANSWER:
                data_driven_data[CELL_ANSWER]=xls_sheet.getCell(index_row,data_xls_keys_cols['select']+1)
            if xls_sheet.getCell(index_row,data_xls_keys_cols['select'])==CELL_EXPECTED:
                data_driven_data[CELL_EXPECTED]=xls_sheet.getCell(index_row,data_xls_keys_cols['select']+1)
            index_row=index_row+1
              
        return data_driven_data
   
    except Exception,ex:
        print ex
        return None
    finally:
        xls_sheet.close()
    

def get_simple_hybrid_driven_scenario_values(scenario_id=1,xls_file=DEF_DATA_PATH,sheet_name="HybridSimple"):
    data_xls_keys_cols={'scenario':1,'function':2,'parameters':3}
    hybrid_driven_dict={FRAMEWORK_FUNCTIONS:'',PARAMETERS:[]}
    hybrid_driven_data=[] #list of dictionaries of hybrid_driven_dict type
    try:
        xls_sheet=easyExcel(xls_file,sheet_name)
        last_row=xls_sheet.get_sheet_last_row(sheet_name)
        found=False
        scenario_row=0
        for row in range(1,last_row):
            if xls_sheet.getCell(row,data_xls_keys_cols['scenario'])==scenario_id:
                found=True
                scenario_row=row
                break
        if found is False:
            raise Exception('Scenarion %s not found in xls file %s sheet %s' %(scenario_id,xls_file,sheet_name))
            
        #stop at finding blank value or exit at index 5
        for index_row in range(scenario_row,scenario_row+5):
            if xls_sheet.getCell(index_row,data_xls_keys_cols['function'])==None:
                break
            
            temp_hybrid_dict=copy.deepcopy(hybrid_driven_dict)
            if xls_sheet.getCell(index_row,data_xls_keys_cols['function'])==CELL_F_REMEMBER_ME:
                temp_hybrid_dict[FRAMEWORK_FUNCTIONS]=CELL_F_REMEMBER_ME
                if xls_sheet.getCell(index_row,data_xls_keys_cols['parameters'])!=None:
                    temp_hybrid_dict[PARAMETERS]=xls_sheet.getCell(index_row,data_xls_keys_cols['parameters']).split("&&")
            if xls_sheet.getCell(index_row,data_xls_keys_cols['function'])==CELL_F_LOGIN:
                temp_hybrid_dict[FRAMEWORK_FUNCTIONS]=CELL_F_LOGIN
                if xls_sheet.getCell(index_row,data_xls_keys_cols['parameters'])!=None:
                    temp_hybrid_dict[PARAMETERS]=xls_sheet.getCell(index_row,data_xls_keys_cols['parameters']).split("&&")
            if xls_sheet.getCell(index_row,data_xls_keys_cols['function'])==CELL_F_SELECT_ANSWER:
                temp_hybrid_dict[FRAMEWORK_FUNCTIONS]=CELL_F_SELECT_ANSWER
                if xls_sheet.getCell(index_row,data_xls_keys_cols['parameters'])!=None:
                    temp_hybrid_dict[PARAMETERS]=xls_sheet.getCell(index_row,data_xls_keys_cols['parameters']).split("&&")
            if xls_sheet.getCell(index_row,data_xls_keys_cols['function'])==CELL_F_SHOW_ANSWER:
                temp_hybrid_dict[FRAMEWORK_FUNCTIONS]=CELL_F_SHOW_ANSWER
                if xls_sheet.getCell(index_row,data_xls_keys_cols['parameters'])!=None:
                    temp_hybrid_dict[PARAMETERS]=xls_sheet.getCell(index_row,data_xls_keys_cols['parameters']).split("&&")
            hybrid_driven_data.append(temp_hybrid_dict)
            index_row=index_row+1
              
        return hybrid_driven_data
   
    except Exception,ex:
        print ex
        return None
    finally:
        xls_sheet.close()

def get_keywords_driven_scenario_values(scenario_id=1,xls_file=DEF_DATA_PATH,sheet_name="Keyword"):
    data_xls_keys_cols={'scenario':1,'action':2,'window':3,'locator':4,'parameters':5}
    keyword_driven_dict={FRAMEWORK_FUNCTIONS:'',PARAMETERS:[],PAGE_WINDOW:'',LOCATOR:''}
    keyword_driven_data=[] #list of dictionaries of keyword_driven_dict type
    try:
        xls_sheet=easyExcel(xls_file,sheet_name)
        last_row=xls_sheet.get_sheet_last_row(sheet_name)
        found=False
        scenario_row=0
        for row in range(1,last_row):
            if xls_sheet.getCell(row,data_xls_keys_cols['scenario'])==scenario_id:
                found=True
                scenario_row=row
                break
        if found is False:
            raise Exception('Scenarion %s not found in xls file %s sheet %s' %(scenario_id,xls_file,sheet_name))
        
        #get next scenario
        for next_row in range(scenario_row,last_row):
            if xls_sheet.getCell(row,data_xls_keys_cols['scenario'])!=None:
                next_scenario_row=next_row
                
                
        #stop at finding blank value or next scenario value
        for index_row in range(scenario_row,next_scenario_row):
            if xls_sheet.getCell(index_row,data_xls_keys_cols['action'])==None:
                break
            
            temp_keyword_dict=copy.deepcopy(keyword_driven_dict)
            temp_keyword_dict[FRAMEWORK_FUNCTIONS]=xls_sheet.getCell(index_row,data_xls_keys_cols['action'])
            if xls_sheet.getCell(index_row,data_xls_keys_cols['window'])!=None:
                temp_keyword_dict[PAGE_WINDOW]=xls_sheet.getCell(index_row,data_xls_keys_cols['window'])
            if xls_sheet.getCell(index_row,data_xls_keys_cols['locator'])!=None:
                temp_keyword_dict[LOCATOR]=xls_sheet.getCell(index_row,data_xls_keys_cols['locator'])  
            if xls_sheet.getCell(index_row,data_xls_keys_cols['parameters'])!=None:
                temp_keyword_dict[PARAMETERS]=xls_sheet.getCell(index_row,data_xls_keys_cols['parameters']).split("&&")
                    
            keyword_driven_data.append(temp_keyword_dict)
            index_row=index_row+1
              
        return keyword_driven_data
   
    except Exception,ex:
        print ex
        return None
    finally:
        xls_sheet.close()
