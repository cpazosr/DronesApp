### Project Description

 A Pilot needs to register his drone at the system (Drone model, Serial number, etc.). He has to choose between the available drone models (All DJI Drone models compatible with DJI MSDKv5) and then add his drone (1:n) with the serial number, age, pilot name (or extra pilot relation), ...
After registering he can fly and acquire data. To do so he needs to create a flight in the system, that is related to the drone. When he finished the flight he set the flight to state finished (with date time) and can describe if anything happened during the flight.

---

This web application allows pilots to register to the platform. Once registered the pilot can access to the drones for flights. New drones can be added based on the available on the database. For each drone it can make multiple flights and register each flight details.

--- 

The structure is:
- Pilot: login / register
- Drones: register new drone / fly drone
- Flights: plan new flight / fly the mission

--- 

Development: 
- Backend: Flask
- DB: PostgreSQL
- Frontend: Vue / Typescript