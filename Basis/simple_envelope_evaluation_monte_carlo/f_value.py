import numpy as np
import pandas as pd
from  scipy.interpolate  import  interp1d
import itertools


class f1f2Value:

    # obtain the list from csv data
    def __init__(self):
        self.f_list = pd.read_csv('f_value.csv', skiprows = 1)
        self.f_list['ガラス仕様の区分'] = self.f_list['ガラス仕様の区分'].fillna(method='ffill')
        self.f_list['期間']             = self.f_list['期間']            .fillna(method='ffill')
        self.f_list.columns=['Glass Spec',
                             'Season',
                             'l_value',
                             '1N','1NE','1E','1SE','1S','1SW','1W','1NW',
                             '2N','2NE','2E','2SE','2S','2SW','2W','2NW',
                             '3N','3NE','3E','3SE','3S','3SW','3W','3NW',
                             '4N','4NE','4E','4SE','4S','4SW','4W','4NW',
                             '5N','5NE','5E','5SE','5S','5SW','5W','5NW',
                             '6N','6NE','6E','6SE','6S','6SW','6W','6NW',
                             '7N','7NE','7E','7SE','7S','7SW','7W','7NW',
                             '8N','8NE','8E','8SE','8S','8SW','8W','8NW']
        self.f_list['Season'] = self.f_list['Season'].replace( { '冷房':'Cooling', '暖房':'Heating' } )
        self.f_list['Glass Spec'] = self.f_list['Glass Spec'].replace( { 1:'Type1', 2:'Type2', 3:'Type3', 4:'Type4', 5:'Type5', 6:'Type6', 7:'Type7' } )

    # get l and nu list in table
    def getTableValue(self, glassType, season, region, direction):
        r = str({ 'region1':1, 'region2':2, 'region3':3, 'region4':4, 'region5':5, 'region6':6, 'region7':7, 'region8':8 }[region])
        d = { 'N':'N', 'NE':'NE', 'E':'E', 'SE':'SE', 'S':'S', 'SW':'SW', 'W':'W', 'NW':'NW' }[direction]
        return self.f_list[ (self.f_list['Season']==season) & (self.f_list['Glass Spec']==glassType) ].loc[:,['l_value',r+d]]

    # get f1 or f2 value
    def getValue(self, glassType, season, region, direction, lValue):
        if lValue > 20.0:
            lValue = 20.0
        dat = self.getTableValue(glassType, season, region, direction)
        return float( interp1d(dat.iloc[:,0],dat.iloc[:,1])(lValue) )

