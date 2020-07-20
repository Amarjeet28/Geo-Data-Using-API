# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:06:31 2020

@author: amarjeet


Pulls distances from Google API - Make sure the key is preserved.
"""

#Google APIs distance matrix code
#-------------------------------
import pandas as pd
import googlemaps as gm
#import time as tm


class local_activities:
    
    def __init__(self):
        pass
        
    def read_data(self):
        InputDf = pd.read_csv('<<file path>>/filname.csv')
        return InputDf
        
class web_based_activities(object):
    
    def __init__(self,local_activities):
        self.InputDf = local_activities.read_data()
    
    def calculate_distances(self):
        
        origin = self.InputDf['OC'].tolist()
        destination= self.InputDf['DC'].tolist()  
        
        for i in range(len(origin)):
                gmaps = gm.Client(key='<<Insert Key Here>>',timeout=None,retry_timeout=380,queries_per_second=9000)
                distance_results = gmaps.distance_matrix(origin[i], destination[i],'driving', region='in')
                distance_results = pd.DataFrame(distance_results)
                distance_results.to_csv('D:/2_Business Dev\Rivigo/DataFromRivigoTeam/Distance Matrix From Google/Distances.csv', mode ='a', header = False)

def main():
    la = local_activities()
    la.read_data()
    
    wba = web_based_activities(la)
    wba.calculate_distances()

if __name__== "__main__":
    main()
    
