#!/usr/bin/env python

from collections import OrderedDict

DATABASE_NAMES = OrderedDict([("main_system", "Main System")])
                            # ("germinator", "Germinator"),
                            # ("aero_1", "Mini-Aero System")])
COLLECTION_NAMES = {
    "main_system": OrderedDict([("water_sensors_1", "Water Sensors 1"),
        ("water_sensors_2", "Water Sensors 2"),
        ("water_sensors_3", "Water Sensors 3"),
        ("water_sensors_4", "Water Sensors 4"),
        ("water_sensors_5", "Water Sensors 5"),
        ("water_sensors_6", "Water Sensors 6"),
        ("air_sensors_2_2", "Atmospheric Sensors 2 2"),
        ("air_sensors_3", "Atmospheric Sensors 3")])
    # "germinator": OrderedDict([("water_sensors",
    #     ("air_sensors", "Air Sensors")]),
    # "aero_1": OrderedDict([("water_sensors", "Water Sensors"),
    #     ("air_sensors", "Air Sensors")])
}
__temperature_info = ("Temperature", {
    "range": [15, 30],
    "ticks": [15, 20, 25, 30],
    "green": [20, 25],
    "yellow": [18, 27]
})
__water_temperature_info = ("Water_Temperature", __temperature_info[1])
__ph_info = ("PH", {
    "range": [5, 7],
    "ticks": [5, 5.5, 6, 6.5, 7],
    "green": [5.7, 6.3],
    "yellow": [5.5, 6.5]
})
__do_info = ("DO", {
    "range": [0, 20],
    "ticks": ["0", 5, 10, 15, 20],
    "green": [7, 13],
    "yellow": [5, 15]
})
__orp_info = ("ORP", {
    "range": [-500, 500],
    "ticks": [-500, -250, "0", 250, 500],
    "green": [250, 400],
    "yellow": [200, 450]
})
__ec_info = ("EC", {
    "range": [0, 2000],
    "ticks": ["0", 500, 1000, 1500, 2000],
    "green": [700, 1300],
    "yellow": [500, 1500]
})
__sal_info = ("SAL", {
    "range": [0, 3],
    "ticks": ["0",1, 2, 3],
    "green": [0.2, 2],
    "yellow": [0.1, 2.1]
})
__tds_info = ("TDS", {
    "range": [0, 2000],
    "ticks": ["0", 500, 1000, 1500, 2000],
    "green": [500, 1000],
    "yellow": [0, 1500]
})
__sg_info = ("SG", {
    "range": [0.6, 1.4],
    "ticks": [0.6, 0.8, 1, 1.2, 1.4],
    "green": [0.8, 1.2],
    "yellow": [0.7, 1.3]
})
_water_sensors_info = OrderedDict([
    __temperature_info,
    __ph_info,
    __do_info,
    __orp_info,
    __ec_info,
    __sal_info,
    __tds_info,
    __sg_info
])
__CO2_info = ("CO2", {
    "range": [0, 1000],
    "ticks": ["0", 250, 500, 750, 1000],
    "green": [400, 600],
    "yellow": [200, 800]
})

__CO2_temp_info = ("CO2_Temperature", __temperature_info[1])

__CO_info = ("CO", {
    "range": [0, 2000],
    "ticks": ["0", 500, 1000, 1500, 2000],
    "green": [800, 1200],
    "yellow": [600, 1400]
})
__light_info = ("Light", {
    "range": [0, 5],
    "ticks": ["0", 1, 2, 3, 4, 5],
    "green": [3,4],
    "yellow": [2, 5]
})
__altitude_info = ("Altitude", {
    "range": [-50, 50],
    "ticks": [-50, -25, "0", 25, 50],
    "green": [-25, 25],
    "yellow": [-35, 35]
})
__uv_info = ("UV", {
    "range": [0, 500],
    "ticks": ["0", 100, 200, 300, 400, 500],
    "green": [200, 300],
    "yellow": [100, 400]
})
__ir_info = ("IR", {
    "range": [0, 1000],
    "ticks": ["0", 250, 500, 750, 1000],
    "green": [600, 750],
    "yellow": [500, 850]
})
__humidity_info = ("Humidity", {
    "range": [0, 100],
    "ticks": ["0", 25, 50, 75, 100],
    "green": [40, 60],
    "yellow": [30, 70]
})
__pressure_info = ("Pressure", {
    "range": [0, 2],
    "ticks": ["0", 1, 2],
    "green": [0.8, 1.2],
    "yellow": [0.7, 1.3]
})
__CO2_humidity_info = ("CO2_Humidity", __humidity_info[1])
__barometer_info = ("Barometer_Temperature", {
    "range": [0, 50],
    "ticks": ["0", 10, 20, 30, 40, 50],
    "green": [20, 30],
    "yellow": [10, 40]
})
__dust_info = ("Dust", {
    "range": [0, 10000],
    "ticks": ["0", 2500, 5000, 7500],
    "green": [4000, 6000],
    "yellow": [3000, 7000]
})
__O2_info = ("O2", {
    "range": [0, 100],
    "ticks": ["0", 25, 50, 75, 100],
    "green": [40, 60],
    "yellow": [30, 70]
})
__NO2_info = ("NO2", {
    "range": [0, 50],
    "ticks": ["0", 25, 50, 75, 100],
    "green": [30, 50],
    "yellow": [20, 60]
})
_air_sensors_info = OrderedDict([
    __CO2_info,
    __CO_info,
    __temperature_info,
    __light_info,
    __altitude_info,
    __uv_info,
    __humidity_info,
    __pressure_info,
    __barometer_info,
    __dust_info,
    __O2_info,
    __NO2_info
])

_air_sensors_2_info = OrderedDict([
    __CO2_info,
    __CO2_temp_info,
    __CO2_humidity_info,
    __temperature_info,
    __light_info,
    __uv_info,
    __ir_info,
    __humidity_info,
    __dust_info,
    __O2_info,
    __water_temperature_info
])

COLLECTION_INFO = {
    "main_system": {
        "water_sensors_1": _water_sensors_info,
        "water_sensors_2": _water_sensors_info,
        "water_sensors_3": _water_sensors_info,
        "water_sensors_4": _water_sensors_info,
        "water_sensors_5": _water_sensors_info,
        "water_sensors_6": _water_sensors_info,
        "air_sensors_2_2": _air_sensors_2_info,
        "air_sensors_3": _air_sensors_info,
    }
 #    "germinator": {
	# "water_sensors": _water_sensors_info,
 #        "air_sensors": _air_sensors_info
 #    },
 #    "aero_1": {
	# "water_sensors": _water_sensors_info,
 #        "air_sensors": _air_sensors_info
 #    }
}
