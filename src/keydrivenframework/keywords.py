'''
Created on 07.06.2014

@author: ionitadaniel19
'''

from config.constants import *
from config.utilities import get_webdriver_selector_element
import selenium.webdriver.support.expected_conditions as Conditions
from selenium.webdriver.support.ui import *
import traceback
from selenium.webdriver.support import expected_conditions as EC

#functions keywords_selenium

def click(driver,locator):
    element = driver.find_element(*get_webdriver_selector_element(locator))
    element.click()

def get_text(driver,locator):
    return driver.find_element(*get_webdriver_selector_element(locator)).text.strip()

def wait_element(driver,locator,timeout=60):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(get_webdriver_selector_element(locator)),'Element not found %s' %locator)
    except:
        raise Exception("%s second time out reached while waiting for element to be present, %s\n%s" % ((timeout), locator, traceback.format_exc()))
    
def click_wait(driver,locator,timeout=60):
    wait_element(driver,locator, timeout)
    click(driver,locator)

def type_text(driver,locator,text):
    text_element =  driver.find_element(*get_webdriver_selector_element(locator))
    text_element.clear()
    text_element.send_keys(text)
    
def open_page(driver,url):
    driver.get(url)

def validate_answer(answer,expected_answer):
    if answer==expected_answer:
        return True
    else:
        return False
                