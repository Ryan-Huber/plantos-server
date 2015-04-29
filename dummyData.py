# Measurements are approximate, 
# and in the unit Meters
#
#
#
#
#Enclosure
enclosure = {
			"url":"/",
			"length":12.0,
			"width":2.0,
	   		"height":4.0,
			"children":[]
			}
#AISLE
main_system = {"url":"/main_system",
			"length":10.0,
			 "width":0.5,
			"height":4.0,
			"x":0,
			"y":1.5,
			"z":0,
			  "children":[]
			   }
#SYSTEM / TRAY
groBot = {"url":"/groBot",
	   "length":1,
		"width":1,
	   "height":1,
		"x":0,
		"y":0,
		"z":0,
		 "children":[]
		  }
#BAY 1 of main system
bay1 = {"url":"/bay/1",
   		"x":0,
		"y":0,
		"z":0,
		"length":2.0,
		"width":0.5,
		"height":4.0,
	  "children":[]
		}
#BAY 2 of main system
bay2 = {"url":"/bay/2",
		"x":2.0,
		"y":0,
		"z":0,
		"length":2.0,
		"width":0.5,
		"height":4.0,
	 	"children":[]
		}
#BAY 3 of main system
bay3 = {"url":"/bay/3",
   		"x":4.0,
		"y":0,
		"z":0,
		"length":2.0,
		"width":0.5,
		"height":4.0,
	  	"children":[]
		}
#BAY 4 of main system
bay4 = {"url":"/bay/4",
		"x":6.0,
		"y":0,
		"z":0,
		"length":2.0,
		"width":0.5,
		"height":4.0,
	  	"children":[]
		}
#BAY 5 of main system
bay5 = {"url":"/bay/5",
		"x":8.0,
		"y":0,
		"z":0,
		"length":2.0,
		"width":0.5,
		"height":4.0,
	  	"children":[]
		}
#TRAY 1 of Bay 1
tray1 = {"url":"/tray/1",
    	"x":0,
		"y":0,
		"z":0.5,
    	"rows":5,
     "columns":11,
      "length":1.8,
       "width":0.5,
      "height":0.15,
	   "sites":[]
		}
#TRAY 1 of Bay 2
tray2 = {"url":"/tray/2",
    	"x":0,
		"y":0,
		"z":0.5,
    	"rows":6,
     "columns":12,
      "length":1.8,
       "width":0.5,
      "height":0.15,
	   "sites":[]
		}
#TRAY 2 of Bay 2
tray3 = {"url":"/tray/3",
    	"x":0,
		"y":0,
		"z":1.75,
    	"rows":6,
     "columns":12,
      "length":1.8,
       "width":0.5,
      "height":0.15,
	   "sites":[]
		}
#TRAY 3 of Bay 2
tray4 = {"url":"/tray/4",
    	"x":0,
		"y":0,
		"z":3,
    	"rows":6,
     "columns":12,
      "length":1.8,
       "width":0.5,
      "height":0.15,
	   "sites":[]
		}
#TRAY 1 of Bay 3
tray5 = {"url":"/tray/5",
    	"x":0,
		"y":0,
		"z":0.5,
    	"rows":5,
     "columns":11,
      "length":1.8,
       "width":0.5,
      "height":0.15,
	   "sites":[]
		}
#TRAY 2 of Bay 3
tray6 = {"url":"/tray/6",
    	"x":0,
		"y":0,
		"z":2,
    	"rows":5,
     "columns":11,
      "length":1.8,
       "width":0.5,
      "height":0.15,
	   "sites":[]
		}
#TRAY 1 of Bay 4
tray7 = {"url":"/tray/7",
    	"x":0,
		"y":0,
		"z":0.5,
    	"rows":5,
     "columns":11,
      "length":1.8,
       "width":0.5,
      "height":0.25,
	   "sites":[]
		}
#TRAY 2 of Bay 4
tray8 = {"url":"/tray/8",
    	"x":0,
		"y":0,
		"z":2,
    	"rows":5,
     "columns":11,
      "length":1.8,
       "width":0.5,
      "height":0.25,
	   "sites":[]
		}
#TRAY 1 of Bay 5
tray9 = {"url":"/tray/9",
    	"x":0,
		"y":0,
		"z":0.5,
    	"rows":5,
     "columns":11,
      "length":1.8,
       "width":0.5,
      "height":0.4,
	   "sites":[]
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
#Now populate children with children
bay1["children"].append(tray1) #Full Tray
bay2["children"].append(tray2) #Full Tray
bay2["children"].append(tray3)
bay2["children"].append(tray4)
bay3["children"].append(tray5)
bay3["children"].append(tray6)
bay4["children"].append(tray7)
bay4["children"].append(tray8)
bay5["children"].append(tray9)
#Now Populate System with children
main_system["children"].append(bay1)
main_system["children"].append(bay2)
main_system["children"].append(bay3)
main_system["children"].append(bay4)
main_system["children"].append(bay5)

from copy import deepcopy

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
