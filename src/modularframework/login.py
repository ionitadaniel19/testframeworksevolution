'''
Created on 01.06.2014

@author: ionitadaniel19
'''
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class LoginPage():
    def __init__(self,driver,url="http://localhost/autframeworks/index.html"):
        self.driver=driver
        self.driver.get(url)

    def login(self,username,pwd):
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.login")),'Element not found login form')
        self.driver.find_element_by_name("login").clear()
        self.driver.find_element_by_name("login").send_keys(username)
        self.driver.find_element_by_name("password").clear()
        self.driver.find_element_by_name("password").send_keys(pwd)
        self.driver.find_element_by_name("commit").click()
        
    def remember_me(self):
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.ID,"remember_me")),'Element not found remember me option')
        self.driver.find_element_by_id("remember_me").click()
            