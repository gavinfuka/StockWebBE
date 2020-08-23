from time import sleep
from .schema import schema
import os 
class _example():
    def __init__(self,driver):
        self.driver = driver
        self.image = os.getcwd()+"/image.png"

    def Click(self,xpath):
        try:
            select =  self.driver.find_element_by_xpath(xpath)
            select.click()
        except:
            try:
                select = self.driver.find_element_by_name(xpath)
                select.click()
            except:
                print('[X] cannot find item by xpath or name')

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

    def Create(self, NewMember = False):
        pass






