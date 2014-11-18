'''
Created on 01.06.2014

@author: ionitadaniel19
'''
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import traceback

def show_answer_record(driver):
    actual_answer=None
    try:
        print 'Test Show answer for record and playback'
        driver.get("http://localhost/autframeworks/index.html")
        driver.find_element_by_name("login").clear()
        driver.find_element_by_name("login").send_keys("test")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("test")
        driver.find_element_by_id("remember_me").click()
        driver.find_element_by_name("commit").click()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID,"q1c")),'Element not found q1c')
        driver.find_element_by_id("q1c").click()
        driver.find_element_by_name("showanswer").click()
        actual_answer=driver.find_element_by_css_selector("#answer > p").text
        
    except:
        print traceback.format_exc()
    finally:
        return actual_answer
    

    
    