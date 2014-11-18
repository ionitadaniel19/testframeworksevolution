'''
Created on 01.06.2014

@author: ionitadaniel19
'''
import traceback

def show_answer_modular(driver):
    actual_answer=None
    try:
        print 'Test Show answer for modular framework'
        from modularframework.login import LoginPage
        from modularframework.testframeworks import TestFrameworksPage
        login_page=LoginPage(driver)
        login_page.login("test", "test")
        test_framework_page=TestFrameworksPage(driver)
        test_framework_page.select_answer('Data-Driven')
        actual_answer=test_framework_page.show_answer()
    except:
        print traceback.format_exc()
    finally:
        return actual_answer