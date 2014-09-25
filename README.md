PlantosServer
=============
A Web Server used to manage an instance of a CityFARM. PlantosServer provides
tools for data collection, data visualization, and plant monitoring through an
easy-to-use web interface

Installation
------------
PlantosServer expects to be running alongside an instance of MongoDB for data
storage. To install MongoDB, just run
        sudo apt-get install mongodb

Operation
---------
To start the server, just run
        python main.py
This will start a local instance of the web server on your computer. To navigate
the site, visit http://(your-ip-address):5000.
