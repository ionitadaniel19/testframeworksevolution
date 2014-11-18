'''
Created on 06.06.2014

@author: ionitadaniel19
'''
import os

EXPECTED_ANSWER="The correct answer is none of the above! The most recommended test framework is a hybrid test framework." 
DEF_DATA_PATH=  os.path.join(os.getcwd().split('src')[0],'data','frameworks.xlsx')
FRAMEWORK_FUNCTIONS='FUNCTION'
PARAMETERS='PARAMETERS'
LOCATOR='LOCATOR'
PAGE_WINDOW='WINDOW'

#xls values
CELL_USER='USER'
CELL_PWD='PWD'
CELL_ANSWER='ANSWER'
CELL_EXPECTED='EXPECTED_ANSWER'
CELL_F_REMEMBER_ME='REMEMBER_ME'
CELL_F_LOGIN='LOGIN'
CELL_F_SELECT_ANSWER='SELECT_ANSWER'
CELL_F_SHOW_ANSWER='SHOW_ANSWER'

#SELENIUM IDENTIFICATION
SELECTOR_ID = "id"
SELECTOR_XPATH = "xpath"
SELECTOR_NAME = "name"
SELECTOR_LINK = "link text"
SELECTOR_PARTIAL_LINK= "partial link text"
SELECTOR_TAG = "tag name"
SELECTOR_CLASS = "class name"
SELECTOR_CSS = "css selector"

#FUNCTIONS KEYWORDS SELENIUM
OPEN="OPEN"
CLICK="CLICK"
GET_TEXT="GET_TEXT"
WAIT="WAIT"
TYPE="TYPE"
VALIDATE="VALIDATE"

