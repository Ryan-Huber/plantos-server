PlantosServer
=============
A Web Server used to manage an instance of a CityFARM. PlantosServer provides
tools for data collection, data visualization, and plant monitoring through an
easy-to-use web interface

Installation
------------
Note: Installation instructions may vary by operating system. These instructions
are for a machine running Ubuntu Server.

PlantosServer expects to be running alongside an instance of MongoDB for data
storage. To install MongoDB, just run

    sudo apt-get install mongodb

Now, clone this repository with the following command:

    git clone https://github.com/MIT-CityFARM/plantos-server.git

Navigate to the plantos-server folder and install the dependencies by running

    sudo pip install -r requirements.txt

The web server can be run by running the main.py file.

PlantosServer requires a configuration file with information about the database
it is using in order to operate correctly. The first time it is run, it will
copy the provided example configuration file (application.cfg.example) into the
instance directory, where the flask app reads it from. To get the program to run,
you will need to edit the application.cfg file in the instance directory to
reflect the actual settings for your specific system.

Operation
---------
To start the server, just run

    python main.py -d

This will start it in debug mode. To navigate to the site, visit http://\<your-ip
-address\>:5000 in your favorite web browser. You can also start the server in
release mode by running

    python main.py

If you do this, it will run on port 80, but will not provide as much output to
the console, making it harder to debug.
