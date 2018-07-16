# Protopaja
## IoT web app
Internet of Things -like web-application for monitoring construction site air quality. Server hosting by DigitalOcean.

## Techniques used:
Arduino Web Client: Send data to server.

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

2. 