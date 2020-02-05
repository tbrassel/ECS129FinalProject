#Class for Energy calculation
'''Energy'''

import pandas as pd

class Energy_calc:
    def __init__(self, df1,df2):
        #pull down entire column
        self.epsilon1 = df1['Epsilon']
        self.epsilon2 = df2['Epsilon']
        self.sigma1 = df1['Sigma']
        self.sigma2 = df2['Sigma']
        self.x1 = df1['X']
        self.x2 = df2['X']
        self.y1 = df1['Y']
        self.y2 = df2['Y']
        self.q1 = df1['Charge']
        self.q2 = df2['Charge']
        self.constant = 83 #constant, can change
        self.asp1 = df1['ASP']
        self.asp2 = df2['ASP']

    #order same as Tyler's demonstration on board
    def Epsilon(self):
        pass
        #return epsilon matrix

    def Sigma(self):
        pass
        #return

    def Distance(self):
        pass
        #return

    def Charge(self):
        pass
        #return

    def Area(self):
        pass
        #return

    def Van(self):
        #calculate van der waals
        #call other funtions inside this class
        pass

    def Area(self):
        pass

    def Energy_diff(self):
        pass
        #return
