# -*- coding: utf-8 -*-
"""
@author: Amarjeet
@date: 14.05.2020

-- Pulls distance and time from TomTom API 

--Sample URL
  https://api.tomtom.com/routing/1/calculateRoute/52.50931%2C13.42936%3A52.50274%2C13.43872/json?maxAlternatives=0&routeRepresentation=summaryOnly&computeTravelTimeFor=all&routeType=shortest&avoid=unpavedRoads&travelMode=truck&vehicleLoadType=USHazmatClass9&vehicleEngineType=combustion&key=*****
"""
#-------------------------------
import pandas as pd
import urllib.request
import json
  
        
class TomTomAPI_Access():
    
    def __init__(self):
        pass 
    
    def read_input_data(self,inputFilePath):
        self.inputData = pd.read_csv(inputFilePath)
        
  
    def fetch_and_dump_distance_time_info(self, outputFilePath):
    
        #Initialize Static Parameters    
        apiURL          = "https://api.tomtom.com/routing/1/calculateRoute/"
        apiKey          = "<<insert API Key here>>"
        travelMode      = "truck"
        avoid           = "unpavedRoads"
        routeType       = "shortest"
        vehicleEngineType = "combustion"
        vehicleMaxSpeed = "60"     #in km/hr
        vehicleWeight   = "30000"       #in kgs
        vehicleLength   = "15"       #in meters
        vehicleWidth    = "3"        #in meters
        vehicleHeight   = "4"       #in meters
        vehicleCommercial = "true"
        vehicleLoadType = "otherHazmatGeneral"
        traffic = "false"
        
        
        #Input Parameters
        sourceLat   = self.InputData['<<SourceLatitudeColumn>>'].tolist()
        sourceLon   = self.InputData['<<SourceLongitudeColumn>>'].tolist()
        destLat     = self.InputData['<<DestinationLatitudeColumn>>'].tolist()
        destLon     = self.InputData['<<DestinationLongitudeColumn>>'].tolist()
        departAt    = self.InputData['<<DepartAtTimeColumn>>'].tolist()
        #departAt has to be in this format: 2020-05-14T21:32:51+05:30
        #can only be future times
        
        
        for iterator in range(len(sourceLat)+1):
           #Create URL and pull times/distances
           tomtomURL = "%s/%s,%s:%s,%s/json?departAt=%s&\
                        routeType=%s&\
                        traffic=%s&\
                        avoid=%s&\
                        travelMode=%s&\
                        vehicleMaxSpeed=%s&\
                        vehicleWeight=%s&\
                        vehicleLength=%s&\
                        vehicleWidth=%s&\
                        vehicleHeight=%s&\
                        vehicleCommercial=%s&\
                        vehicleLoadType=%s&\
                        vehicleEngineType=%s&\
                        key=%s" % (apiURL,sourceLat,sourceLon,destLat,destLon,
                        departAt,routeType,traffic,avoid,travelMode,
                        vehicleMaxSpeed,vehicleWeight,vehicleLength,vehicleWidth,
                        vehicleCommercial,vehicleLoadType,vehicleHeight,
                        vehicleEngineType,apiKey)
                
           getData = urllib.request.urlopen(tomtomURL).read()
           jsonTomTomString = json.loads(getData)
           totalTimeInSeconds = jsonTomTomString['routes'][0]['summary']['totalTimeSeconds']
           totalDistanceInMeters = jsonTomTomString['routes'][0]['summary']['lengthInMeters']
           
           #If there are more columns needed in the output add here
           apiResponse = pd.dataframe([sourceLat,sourceLon,totalTimeInSeconds,
                                       totalDistanceInMeters], 
                                       columns=['SourceLat','SourceLon',
                                                'DestinationLat','DestinationLong',
                                                'TravelTime','Distance'])
           apiResponse.to_csv(outputFilePath, mode ='a', header = False)

def main():

    inputFilePath = "./../Input Files/Missing_Links_Input_4.csv"
    outputFilePath = "./../Output Files/TomTomDistanceTimeData_Trucking.csv"
    
    #Instantiate Object
    tomTomAPIAccess = TomTomAPI_Access()
    tomTomAPIAccess.read_input_data(inputFilePath)
    tomTomAPIAccess.fetch_and_dump_distance_time_info(outputFilePath)
    
    print("Data Fetched Successfully!!")

if __name__== "__main__":
    main()
    