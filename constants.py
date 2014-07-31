#!/usr/bin/env python

from collections import OrderedDict

DATABASE_NAMES = OrderedDict([("main_system", "Main System"),
                            ("germinator", "Germinator")])
COLLECTION_NAMES = {
    "main_system": OrderedDict([("water_sensors", "Water Sensors"),
        ("air_sensors", "Air Sensors")]),
    "germinator": OrderedDict()
}
COLLECTION_INFO = {
    "main_system": {
        "water_sensors": OrderedDict([
            # Temperature sensor
            ("Temperature", {
                "range": [15, 30],
                "ticks": [15, 20, 25, 30],
                "green": [20, 25],
                "yellow": [18, 27]
            }),
            # pH sensor
            ("PH", {
                "range": [5, 7],
                "ticks": [5, 5.5, 6, 6.5, 7],
                "green": [5.7, 6.3],
                "yellow": [5.5, 6.5]
            }),
            # DO sensor
            ("DO", {
                "range": [0, 20],
                "ticks": ["0", 5, 10, 15, 20],
                "green": [7, 13],
                "yellow": [5, 15]
            }),
            # ORP sensor
            ("ORP", {
                "range": [-500, 500],
                "ticks": [-500, -250, "0", 250, 500],
                "green": [250, 400],
                "yellow": [200, 450]
            }),
            # EC sensor
            ("EC", {
                "range": [0, 2000],
                "ticks": ["0", 500, 1000, 1500, 2000],
                "green": [700, 1300],
                "yellow": [500, 1500]
            })
            # Flow meter
            # ("Volume", {
            #     "range": [0, 10],
            #     "ticks": [0, 0],
            #     "green": [0, 0]
            # }),
            # ("LPM", {
            #     "range": [0, 10],
            #     "ticks": [0, 0],
            #     "green": [0, 0]
            # }),
            # ("LPH", {
            #     "range": [0, 10],
            #     "ticks": [0, 0],
            #     "green": [0, 0]
            # })
        ]),
        "air_sensors": OrderedDict([
            ("Temperature", {
                "range": [15, 30],
                "ticks": [15, 20, 25, 30],
                "green": [20, 25],
                "yellow": [18, 27]
            }),
            ("Humidity", {
                "range": [0, 100],
                "ticks": ["0", 25, 50, 75, 100],
                "green": [40, 60],
                "yellow": [30, 70]
            }),
            # These values are arbitrary
            ("CO2", {
                "range": [0, 1000],
                "ticks": ["0", 250, 500, 750, 1000],
                "green": [400, 600],
                "yellow": [300, 700]
            })
        ])
    },
    "germinator": {
    },
}
