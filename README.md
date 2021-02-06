# Data Modeling with Postgres
Project for Data Engineering Nanodegree program at Udacity.


## Objective
This project is an ETL pipeline which takes information from json files, process the data and populate them into a database schema.

The json files are:
**log_data:** Contain information about users and their interactions on the web site "Sparkify". 
The structure of the json is as follow:
![alt text](https://github.com/JulietaCaceres/data-modeling-with-postgres/blob/main/img/log-data.png?raw=true)  

Sparkify is a simulated web of music.

**song_data:** Contain information about songs and artist.
![alt text](https://github.com/JulietaCaceres/data-modeling-with-postgres/blob/main/img/song-data.png?raw=true) 

This data is processed and stored in the database in a star schema for a particular analytic focus.

## Data base schema

- Fact Table
    - songplays: Records in log data associated with song plays i.e. records with page NextSong
      (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
- Dimension Tables
    - users: users in the app
        (user_id, first_name, last_name, gender, level)
    - songs: songs in music database
        (song_id, title, artist_id, year, duration)
    - artists:  artists in music database
        (artist_id, name, location, latitude, longitude)
    - time: timestamps of records in songplays broken down into specific units
        (start_time, hour, day, week, month, year, weekday)

![alt text](https://github.com/JulietaCaceres/data-modeling-with-postgres/blob/main/img/tables.png?raw=true)      
        
## Project structure
- /Data : Contains the json files whit the data to be populated
- /databaseUtils: Contains the following python scripts:
    - sql_queries.py: Contains the queries to create a drop tables, and the insert queries to store the data from jsons.
    - create_tables.py: Contains the logic to drop and create the tables used.
- /notebooks: Contian the notebooks with the test:
    - test.ipynb: Contains queries to validate the creation of the tables.
    - etl.ipynb: Contains the first approach to insert data. It iterates over the data frame and insert the data once by time .
    - etl-with-execute-values: Contains the final approach to insert data using the function 'execute_values' in order to reduce the number of round trips to the database server
- /dashboard: Contains the scripts used to generate a dashboard:
    - app.py: Initialize the Dash application.
    - data_fetcher.py: Contain the queries used to extract the data from the database to use it in the dashboard.
    - index.py: Contains the logic to update the graph because of interaction.
    - layouts.py: Contains the components to show in the dashboard.
- etl.py: Contains the transformationes needed to populate the information and insert the data in the database.

## Dashboard

Running the dashboard is possible take some insights from the data.
You can view the top 5 of locations which have more interaction with the application. The n top can change as you prefer.
![alt text](https://github.com/JulietaCaceres/data-modeling-with-postgres/blob/main/img/top-5-locations.png?raw=true)      
        
Also, you can view the traffic on the page over the time, you are able to select the unit of yime (hour, month, year)
![alt text](https://github.com/JulietaCaceres/data-modeling-with-postgres/blob/main/img/trafic_over_the_time.png?raw=true)      
        
Finally you can view the top 5 users who most use the app.
![alt text](https://github.com/JulietaCaceres/data-modeling-with-postgres/blob/main/img/top-5-users.png?raw=true)      
        

## Run

### Requirements

The following libraries should be installed:
- psycopg2
- pandas
- Dash


### Running

1- Create the tables in sparkify databasse, for that run the script create_table.py:
```console
XXX@XXX:~$ python databaseUtils/create_table.py
```
2- Insert the data:
```console
XXX@XXX:~$ python etl.py
```
To verify the results you can run the test.ipynb


3- Run the dashboard:
```console
XXX@XXX:~$ python dashboard/index.py
```



