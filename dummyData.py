# Measurements are approximate, 
# and in the unit Meters
#
#length = x
#height = y
#width = z
#

# BASE VALUES
encWidth = 1.91
encHeight = 2.49
encLength = 8.53

aWidth = 0.65
aHeight = 2.2
aLength = 6.01
aOffx = 0.038
aOffz = 0.25
aOffy = 0.034

bayWidth = 0.65
bayHeight = 2.2
bayLength = 1.142 #1.172, 1.142
bayOffx = 0.0767
extraOff = 0.0

trayWidth = 0.65
trayHeight = 0.14
trayLength = 1.12

encModelDims = [8.53, 2.49, 1.91]
encModel3D = "/static/img/Models/enclosure.dae"
aModelDims = [6.01, 2.2, 0.92]
aModel3D = "/static/img/Models/aisle.dae"
bayModelDims = [1.1378, 2.2, 0.92]
bayModel3D = "/static/img/Models/bay.dae"
trayModelDims = [1.8, 0.15, 0.5]
trayModel3D = "/static/img/Models/tray.dae"

#Enclosure
enclosure = {
			"url":"/CityFarm",
			"length":encLength,
			 "width":encWidth,
			"height":encHeight,
	   		"x":0,
			"y":0,
			"z":0,
			"children":[],
			"model3d":encModel3D,
			"objectDims":encModelDims,
			}
#AISLE
main_system = {"url":"/main_system",
			"length":aLength,
			 "width":aWidth,
			"height":aHeight,
			"x":aOffx,
			"y":aOffy,
			"z":aOffz,
			  "children":[],
			  "model3d":aModel3D, 
			  "objectDims":aModelDims,
			   }
#SYSTEM / TRAY
groBot = {"url":"/groBot",
	   "length":1,
		"width":1,
	   "height":1,
		"x":0,
		"y":0,
		"z":0,
		 "children":[],
		  }
#BAY 1 of main system
bay1 = {"url":"/bay/1",
   		"x":0,
		"y":0,
		"z":0,
		"length":bayLength,
		"width":bayWidth,
		"height":bayHeight,
	  "children":[],
	  "model3d":bayModel3D, 
	  "objectDims":bayModelDims,
		}
#BAY 2 of main system
bay2 = {"url":"/bay/2",
		"x":bayOffx+bayLength+extraOff,
		"y":0,
		"z":0,
		"length":bayLength,
		"width":bayWidth,
		"height":bayHeight,
	 	"children":[],
	 	"model3d":bayModel3D, 
	 	"objectDims":bayModelDims,
		}
#BAY 3 of main system
bay3 = {"url":"/bay/3",
   		"x":2*bayOffx+2*bayLength+extraOff,
		"y":0,
		"z":0,
		"length":bayLength,
		"width":bayWidth,
		"height":bayHeight,
	  	"children":[],
	  	"model3d":bayModel3D, 
	  	"objectDims":bayModelDims,
		}
#BAY 4 of main system
bay4 = {"url":"/bay/4",
		"x":3*bayOffx+3*bayLength+extraOff,
		"y":0,
		"z":0,
		"length":bayLength,
		"width":bayWidth,
		"height":bayHeight,
	  	"children":[],
	  	"model3d":bayModel3D, 
	  	"objectDims":bayModelDims,
		}
#BAY 5 of main system
bay5 = {"url":"/bay/5",
		"x":4*bayOffx+4*bayLength+extraOff,
		"y":0,
		"z":0,
		"length":bayLength,
		"width":bayWidth,
		"height":bayHeight,
	  	"children":[],
	  	"model3d":bayModel3D, 
	  	"objectDims":bayModelDims,
		}
#TRAY 1 of Bay 1
tray1 = {"url":"/tray/1",
    	"x":0,
		"y":0,
		"z":0,
    	"rows":5,
     "columns":11,
      "length":trayLength,
       "width":trayWidth,
      "height":trayHeight,
	   "sites":[],
	   "model3d":trayModel3D, 
	   "objectDims":trayModelDims,
		}
#TRAY 1 of Bay 2
tray2 = {"url":"/tray/2",
    	"x":0,
		"y":0,
		"z":0,
    	"rows":6,
     "columns":12,
      "length":trayLength,
       "width":trayWidth,
      "height":trayHeight,
	   "sites":[],
	   "model3d":trayModel3D, 
	   "objectDims":trayModelDims,
		}
#TRAY 2 of Bay 2
tray3 = {"url":"/tray/3",
    	"x":0,
		"y":0,
		"z":0.72,
    	"rows":6,
     "columns":12,
      "length":trayLength,
       "width":trayWidth,
      "height":trayHeight,
	   "sites":[],
	   "model3d":trayModel3D, 
	   "objectDims":trayModelDims,
		}
#TRAY 3 of Bay 2
tray4 = {"url":"/tray/4",
    	"x":0,
		"y":0,
		"z":1.44,
    	"rows":6,
     "columns":12,
      "length":trayLength,
       "width":trayWidth,
      "height":trayHeight,
	   "sites":[],
	   "model3d":trayModel3D, 
	   "objectDims":trayModelDims,
		}
#TRAY 1 of Bay 3
tray5 = {"url":"/tray/5",
    	"x":0,
		"y":0,
		"z":0,
    	"rows":5,
     "columns":11,
      "length":trayLength,
       "width":trayWidth,
      "height":trayHeight,
	   "sites":[],
	   "model3d":trayModel3D, 
	   "objectDims":trayModelDims,
		}
#TRAY 2 of Bay 3
tray6 = {"url":"/tray/6",
    	"x":0,
		"y":0,
		"z":1.1,
    	"rows":5,
     "columns":11,
      "length":trayLength,
       "width":trayWidth,
      "height":trayHeight,
	   "sites":[],
	   "model3d":trayModel3D, 
	   "objectDims":trayModelDims,
		}
#TRAY 1 of Bay 4
tray7 = {"url":"/tray/7",
    	"x":0,
		"y":0,
		"z":0,
    	"rows":5,
     "columns":11,
      "length":trayLength,
       "width":trayWidth,
      "height":trayHeight*2,
	   "sites":[],
	   "model3d":trayModel3D, 
	   "objectDims":trayModelDims,
		}
#TRAY 2 of Bay 4
tray8 = {"url":"/tray/8",
    	"x":0,
		"y":0,
		"z":1.1,
    	"rows":5,
     "columns":11,
      "length":trayLength,
       "width":trayWidth,
      "height":trayHeight*2,
	   "sites":[],
	   "model3d":trayModel3D, 
	   "objectDims":trayModelDims,
		}
#TRAY 1 of Bay 5
tray9 = {"url":"/tray/9",
    	"x":0,
		"y":0,
		"z":0,
    	"rows":5,
     "columns":11,
      "length":trayLength,
       "width":trayWidth,
      "height":trayHeight*3,
	   "sites":[],
	   "model3d":trayModel3D, 
	   "objectDims":trayModelDims,
		}
#SITES for Tray1
sites1 = []
i = 1
for column in range(11):
	for row in range (5):
		if row % 2 == column % 2:
			sitex = {"url":"/site/1" + str(i),
					 "row":row,
				  "column":column,
				   "plant":{}
					}
			sites1.append(sitex)
			i+=1
#SITES for Tray2
sites2 = []
i = 1
for column in range(12):
	for row in range (6):
		if row % 2 != column % 2:
			sitex = {"url":"/site/2" + str(i),
					 "row":row,
				  "column":column,
				   "plant":{}
					}
			sites2.append(sitex)
			i+=1
#PLANT TYPES
plantTypes = []
tomato = {"url":"",
		  "common_name":"Tomato",
		  "latin_name":"",
		  "estimated_time_until_harvest":""
		  }
lettuce = {"url":"",
		   "common_name":"Lettuce",
		   "latin_name":"",
		   "estimated_time_until_harvest":""
		   }
kale = {"url":"",
		"common_name":"Kale",
		"latin_name":"",
		"estimated_time_until_harvest":""
		}
plantTypes.append(tomato)
plantTypes.append(lettuce)
plantTypes.append(kale)

#MAKE TREE FOR TRAY SELECT
# Don't need to add plants to site yet
# Main System has 5 children
# children 3-5 currently have empty children 
# Bay 1 and 2 currently have only 1 Tray full each

#Already populated sites1 and 2
#Now populate tray1 and 2 with sites1 and 2
tray1["sites"] = sites1 
tray2["sites"] = sites2
#Now populate bays with trays
bay1["children"].append(tray1) #Full Tray
bay2["children"].append(tray2) #Full Tray
bay2["children"].append(tray3)
bay2["children"].append(tray4)
bay3["children"].append(tray5)
bay3["children"].append(tray6)
bay4["children"].append(tray7)
bay4["children"].append(tray8)
bay5["children"].append(tray9)
#Now Populate Main System (aisle) with bays
main_system["children"].append(bay1)
main_system["children"].append(bay2)
main_system["children"].append(bay3)
main_system["children"].append(bay4)
main_system["children"].append(bay5)

from copy import deepcopy
#put aisle in the enclosure
enclosure["children"].append(main_system)
traySelectQuery = deepcopy(enclosure)


#See system query (urls only)
'''
print main_system["url"]
for bay in main_system["children"]:
	print "\t" + bay["url"]
	for tray in bay["children"]:
		print "\t\t" + tray["url"]
		for site in tray["sites"]:
			print "\t\t\t" + site["url"]
'''

#PLANTS
from random import randint
#sites1
i=1
x=1
for site in main_system["children"][0]["children"][0]["sites"]:
	if i%2==1:
		typeIndex = (x+len(plantTypes)-1)%len(plantTypes)
		plantXType = plantTypes[typeIndex]
		url = "/plant/1"+str(x)
		sownDate = ""
		plantX = {"url":url,
				  "plant_type":plantXType,
				  "sown_date":sownDate}
		site["plant"] = plantX
		x+=1
	i+=1
#Sites2
i=1
x=1
for site in main_system["children"][1]["children"][0]["sites"]:
	if i%2==1:
		typeIndex = (x+len(plantTypes)-1)%len(plantTypes)
		plantXType = plantTypes[typeIndex]
		url = "/plant/2"+str(x)
		sownDate = ""
		plantX = {"url":url,
				  "plant_type":plantXType,
				  "sown_date":sownDate}
		site["plant"] = plantX
		x+=1
	i+=1

trayListQuery = [tray1, tray2]


#See system tree down to plant (URL only)
'''
print main_system["url"]
for bay in main_system["children"]:
	print "\t" + bay["url"]
	for tray in bay["children"]:
		print "\t\t" + tray["url"]
		for site in tray["sites"]:
			print "\t\t\t" + site["url"]
			print "\t\t\t\t" + str(site["plant"])

'''

'''
print childrenelectQuery["url"]
for bay in childrenelectQuery["children"]:
	print "\t" + bay["url"]
	for tray in bay["children"]:
		print "\t\t" + tray["url"]
		for site in tray["sites"]:
			print "\t\t\t" + site["url"]
			print "\t\t\t\t" + str(site["plant"])

'''
checkThis = tray9
for x,y in checkThis.items():
	if x != "children":
		#print x,y
		pass



