from ..BaseActions import BaseAction
from ..GUtils.CLog import CLog

from time import sleep
import os 
import pandas as pd

class Symbol(BaseAction):
    def __init__(self,driver):
        super().__init__(self)
        self.driver = driver

    def ShowSector(self):
        self.Click('/html/body/div[6]/section/div[11]/div[5]/table/thead/tr/th[81]/div/span')
        sleep(2)
        self.Wait('/html/body/div[6]/section/div[11]/div[5]/table/thead/tr/th[81]/form/div/div[2]/div[1]/ul/li[4]/label')
        self.Click('/html/body/div[6]/section/div[11]/div[5]/table/thead/tr/th[81]/form/div/div[2]/div[1]/ul/li[4]/label')
        self.Click('/html/body/div[6]/section/div[11]/div[5]/table/thead/tr/th[81]/form/div/div[3]/a')

    def ClosePopup(self):
        try:
            self.Click('/html/body/div[6]/div[2]/i', LogErr=False)
        except:
            pass

    def NextPage(self):
        buttonXpath = '/html/body/div[5]/section/div[11]/div[5]/div[2]/div[3]/a'
        if self.CheckExists(buttonXpath):
            self.Click(buttonXpath)
            sleep(2)
            return {"Success":True}
        return {"Success":False}

    @staticmethod
    def AppendifValue(array,value):
        if value:
            array.append(value)
        else:
            array.append('')
            CLog('[!] Missing Value')
        return array

    
    def Extract(self):
        try:
            NameList = []
            SymbolList = []
            # SectorList = []
            cont = True

            while (cont):               
                for i in range (1,51):
                    self.ClosePopup()
                    Name =  self.GetValue(xpath='/html/body/div[5]/section/div[11]/div[5]/table/tbody/tr[%d]/td[2]/a'%i)
                    Symbol = self.GetValue(xpath='/html/body/div[5]/section/div[11]/div[5]/table/tbody/tr[%d]/td[3]'%i)
                    
                    if i == 1:
                        print('[-] First item in page:' + Name + Symbol)

                    self.AppendifValue(NameList,Name)
                    self.AppendifValue(SymbolList,Symbol)

                msg = ' '.join(['[-]', str(len(NameList)), str(len(SymbolList))]) 
                CLog(msg)      

                if(self.CheckExists('/html/body/div[5]/section/div[11]/div[5]/div[2]/div[3]/a')):
                    self.NextPage()
                else:
                    cont = False

            res = {'NameList':NameList,'SymbolList':SymbolList}
            return res

        except Exception as e:
            print(e)








