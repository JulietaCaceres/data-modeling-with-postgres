# Data Modeling with Postgres
Project for Data Engineering Nanodegree program at Udacity.


## Objective
This project is an ETL pipeline which takes information from json files about users and their interactions on the web site "Sparkify". 
Sparkify is a simulated web of music, and the json files contain information about songs, interactions user-page, and artists.
The goal is to take information from files and populate this data into fact and dimension tables for a star schema for a particular analytic focus.

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



## Run

### Requirements

The following libraries should be installed:
- psycopg2
- pandas
- dash
- dash-core-components
- plotly-express 


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



