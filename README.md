# Protopaja
## IoT web app
Internet of Things -like web-application for monitoring construction site air quality. Server hosting by DigitalOcean.

## Techniques used:
Arduino WifiClient: Send data to server.

Apache: Run server.

Django: Framework for application.

Django channels: Make Django asynchronous.

SQLite: Database for managing devices and data.

Chart.js: Draw charts from data.

## Devicedata application
1. Get JSON-data from device
	- Device ID
		- Time
		- Pollution
		- Temp
		- Humidity

2. Make two models out of JSON-data
	- Device
		- Device ID : Specific ID number. Generated.
		- Device info : Device name, location etc. Given by user.

	- Data
		- ForeignKey to Device : Links many Data-models to one Device.
		- Date : Date of data received by Arduino master device. 
		- Pollution : Pollution data. _(numbers/labels)?_
		- Temp : Temperature as float.
		- Humidity : Humidity as int.