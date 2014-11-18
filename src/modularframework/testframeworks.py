'''
Created on 01.06.2014

@author: ionitadaniel19
'''
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import traceback
import time

class TestFrameworksPage():
    def __init__(self,driver,url=None):
        try:
            self.driver=driver
            if url is not None:
                self.driver.get(url)
        except:
            print traceback.format_exc()

    def select_answer(self,answer):
        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID,"q1a")),'Element not found framework question')
            if answer=='Modular':
                self.driver.find_element_by_id("q1a").click()
            elif answer=='Data-Driven':
                self.driver.find_element_by_id("q1b").click()
            elif answer=='Keyword-Driven':
                self.driver.find_element_by_id("q1c").click()
            else:
                error='Answer % does not exist in the list :Modular,Data-Driven,Keyword-Driven' %answer
                raise Exception(error)
        except:
            print traceback.format_exc()
    
    def show_answer(self):
        actual_answer=None
        try:
            self.driver.find_element_by_name("showanswer").click()
            actual_answer=self.driver.find_element_by_css_selector("#answer > p").text
            time.sleep(2)
        except:
            print traceback.format_exc()
        finally:
            return actual_answer
    
    