# Data Modeling with Postgres
Project for Data Engineering Nanodegree program at Udacity.


## Objective
This project is an ETL pipeline which takes information from json files about users and their interactions on the web page "Sparkify". 
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
- sql_queries.py: Contains the queries to create a drop tables, and the insert queries to store the data from jsons.
- create_tables.py: Contain the login to drop and create the tables used.
- etl.py: Contains the transformationes needed to populate the information.
- test.ipynb: Contains queries to validate the creation of the tables.


## Run

### Requirements

The following libraries should be installed:
- psycopg2
- pandas

### Running

In order to run the project you should:
- Run the script create_tables.py
- Run the script etl.py

To verify the results you can run the test.ipynb


