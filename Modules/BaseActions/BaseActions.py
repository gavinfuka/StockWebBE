from time import sleep
import os 

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ..GUtils.CLog import CLog


class BaseAction():
    def __init__(self,driver):
        self.image = os.getcwd()+"/image.png"
        self.driver = driver

    def Select(self,xpath=None,name=None,id=None, className=None, cssSelector=None, linkText=None):
        for i in range(3): #retry
            try:
                if (xpath):
                    select =  self.driver.find_element_by_xpath(xpath)
                elif(name):
                    select = self.driver.find_element_by_name(name)
                elif(id):
                    select = self.driver.find_element_by_id(id)
                elif(className):
                    select = self.driver.find_element_by_class_name(className)
                elif(cssSelector):
                    select = self.driver.find_element_by_css_selector(cssSelector)
                elif(linkText):
                    select = self.driver.find_element_by_link_text(linkText)
                return(select) if select else None
            except:
                pass
        CLog('[X] Cannot find Element')
        return None

    def Click(self,xpath=None,name=None,id=None, className=None, cssSelector=None, linkText=None, LogErr=True):
        try:
            select = self.Select(xpath,name,id, className, cssSelector, linkText)
            if select:
                select.click()
                return {"Success":True}
        except Exception as e:
            if (LogErr):
                CLog('[X] Click Button Failed')
            return {"Success":False}


           

    def Send(self, xpath, value=""):
        try:
            select =  self.driver.find_element_by_xpath(xpath)
            select.send_keys(value)
        except:
            try:
                select = self.driver.find_element_by_name(xpath)
                select.send_keys(value)
            except:
                print('[X] cannot find item by xpath or name')

    def GetValue(self,xpath=None,name=None,id=None, className=None, cssSelector=None, linkText=None):
        select = self.Select(xpath,name,id, className, cssSelector, linkText)
        if select:
            return select.text
        return ''

    def CheckExists(self, xpath=None,name=None,id=None, className=None, cssSelector=None, linkText=None):
        res = self.Select(xpath,name,id, className, cssSelector, linkText)
        if (res!=None):
            return True
        else:
            return False


    def Wait(self, xpath):
        try:
            locator= ('xpath', xpath)
            WebDriverWait(self.driver, 20, 0.5).until(EC.presence_of_element_located(locator))
        finally:
            return