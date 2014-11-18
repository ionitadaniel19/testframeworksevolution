'''
Created on 01.06.2014

@author: ionitadaniel19
'''
import unittest
import traceback
import os
from config.utilities import load_browser_driver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver import Firefox
from selenium.webdriver import Chrome
from selenium.webdriver import Ie
from config.constants import EXPECTED_ANSWER
import logging,time

class FrameworkTests(unittest.TestCase):
    def __init__(self,test,browser_name,url,test_data=None):
        super(FrameworkTests,self).__init__(test)
        self.test=test
        self.browser_name=browser_name
        self.url=url
        self.driver=None
        if self.browser_name=='firefox':
            ffp = FirefoxProfile()
            ffp.update_preferences()
            self.driver = Firefox(firefox_profile=ffp)
        elif self.browser_name=='chrome':
            chromedriver = load_browser_driver("chromedriver")
            os.environ["webdriver.chrome.driver"] = chromedriver
            self.driver=Chrome(chromedriver)
        elif self.browser_name=='ie':
            iedriver = load_browser_driver("IEDriverServer")
            os.environ["webdriver.ie.driver"] = iedriver
            self.driver=Ie(iedriver)
        self.verification = []
        self.verification.append("Test %s on browser %s" %(self.test,self.browser_name))
        self.test_data=test_data
        self.errors=[]
        
    def setUp(self):
        """
            set up data used in the tests.
            setUp is called before each test function execution.
        """
        self.driver.get(self.url)
        time.sleep(5)
    
    def tearDown(self):
        """
            tearDown is called after all other test methods have been invoked.
        """
        if self.driver:
            try:
                time.sleep(2)
                self.driver.quit()
            except:
                print traceback.format_exc()
        for item in self.verification:
            logging.info(item)
        for err in self.errors:
            self.fail(err)
            logging.error(item)
            
    def test_recordplayback(self):
        try:
            self.verification.append('Test record and playback')
            from linearframework.recordtests import show_answer_record
            actual_answer=show_answer_record(self.driver)
            self.assertEqual(actual_answer, EXPECTED_ANSWER, 'Actual answer incorrect:%s.Expected answer is:%s' %(actual_answer,EXPECTED_ANSWER))
        except Exception,ex:
            raise Exception('Test record playback failed with Exception:%s' %ex)
            
    def test_modularframework(self):
        try:
            self.verification.append('Test modular driven framework')
            from modularframework.modulartests import show_answer_modular
            actual_answer=show_answer_modular(self.driver)
            self.assertEqual(actual_answer, EXPECTED_ANSWER, 'Actual answer incorrect:%s.Expected answer is:%s' %(actual_answer,EXPECTED_ANSWER))
        except Exception,ex:
            raise Exception('Test modular failed with Exception:%s' %ex)
        
    def test_dataframework(self):
        try:
            self.verification.append('Test data driven framework')
            from datadrivenframework.datatests import show_answer_datadriven
            actual_answer,expected_answer=show_answer_datadriven(self.driver,2)
            self.assertEqual(actual_answer, expected_answer, 'Actual answer incorrect:%s.Expected answer is:%s' %(actual_answer,expected_answer))
        except Exception,ex:
            raise Exception('Test data driven failed with Exception:%s' %ex)
    
    def test_keywordframework(self):
        try:
            self.verification.append('Test keyword driven framework')
            from keydrivenframework.keytests import show_answer_keydriven
            validate,actual_answer=show_answer_keydriven(self.driver,1)
            if validate is False:
                self.assertTrue(validate,  'Actual answer incorrect:%s'%actual_answer)
        except Exception,ex:
            raise Exception('Test keyword failed with Exception:%s.Traceback is %s' %(ex,traceback.format_exc()))
        
    def test_hybridframework(self):
        try:
            self.verification.append('Test hybrid framework')
            from hybridframework.hybridtests import show_answer_hybrid_simple
            actual_answer=show_answer_hybrid_simple(self.driver,self.test_data)
            self.assertEqual(actual_answer, EXPECTED_ANSWER, 'Actual answer incorrect:%s.Expected answer is:%s' %(actual_answer,EXPECTED_ANSWER))
        except Exception,ex:
            raise Exception('Test hybrid failed with Exception:%s' %ex)
    