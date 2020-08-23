# from ._example import _example
from .InvestCom import InvestCom
from .BaseActions import BaseActions
#config
from ..config import config

from selenium import webdriver


class ChromeBot:
    def __init__(self, URL=None):
        self.ENV = config['ENV']
        self.system = config['System']
        self.Version = config[self.ENV]['Driver']['Version']
        driverLoc = config[self.ENV]['Driver'][self.system].replace('${Version}', self.Version)
        
        #ignore https error
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        
        try:
            #browse url
            if not URL:
                URL = config[self.ENV]['URL']
            if "${Criteria}" in URL:
                URL = URL.replace('${Criteria}', "|".join(config['Criteria']))  +"%3EviewData.symbol;1"
        except Exception as e:
            print(e)

        self.driver = webdriver.Chrome(driverLoc, options=options)
        self.driver.get(URL) 

        ##self.Modules
        # self._example = _example(self.driver)
        self.BaseActions = BaseActions(self.driver)
        self.InvestCom = InvestCom(self.driver)



    def Quit(self):
        self.driver.quit()