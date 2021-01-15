"""Etl for database 

This script takes the json files with songs and user interaction data and populates this information into a 
database using a star schema.

This script requires that `pandas` be installed within the Python
environment you are running this script in.

The sttar schema created using this script will be:
    Fact Table
    ==========
    
    * songplays : Records in log data associated with song plays
        (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)

    Dimension Tables
    ================
    
    * users : Users in the app
        (user_id, first_name, last_name, gender, level)
    * songs - Songs in music database
        (song_id, title, artist_id, year, duration)
    * artists: Artists in music database
        (artist_id, name, location, latitude, longitude)
    * time: Timestamps of records in songplays broken down into specific units
        (start_time, hour, day, week, month, year, weekday)
"""

import os
import glob
import psycopg2
import psycopg2.extras
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Insert data from a json file into song and aritist tables.

    Parameters
    ----------
    cur : str
        Cursor of the database connection.
    filepath : str
        Path of the song json file to process
    """
    

    # read song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)

    
def select_song_and_artist_id(cur, song, artist, length):
    """
    Extract song_id and artist_id from song and artist tables.
    
    Parameters
    ----------
    cur : str
        Cursor of the database connection.
    song: str
        Name of the song in songs table
    artist: str
        Name of the artist in artists table
    length:
        Duration of the song
    
    Returns
    -------
    song_id, artist_id
        song and artis id from tables. None in case of not marching results.
    """
    # get songid and artistid from song and artist tables
    cur.execute(song_select, (song, artist, length))
    results = cur.fetchone()
    if results:
        return results[0], results[1]
    else:
        return None, None

def process_log_file(cur, filepath):
    """
    Insert data from a json file into time, user and songplay tables.

    Parameters
    ----------
    cur : str
        Cursor of the database connection.
    filepath : str
        Path of the song json file to process
    """    

    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'],unit='ms')

    
    # insert time data records
    time_data = [t, t.dt.hour, t.dt.day,  t.dt.week,  t.dt.month,  t.dt.year,  t.dt.weekday]
    column_labels = ['timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    psycopg2.extras.execute_values(cur, time_table_insert, ((
            time['timestamp'],
            time['hour'],
            time['day'],
            time['week'],
            time['month'],
            time['year'],
            time['weekday']
            ) for index, time in time_df.iterrows()), page_size=100 )
        
    # load user table
    user_df = df[["userId", 'firstName', 'lastName', 'gender', 'level']]


    # insert user records        
    psycopg2.extras.execute_values(cur, user_table_insert, ((
        user["userId"],
        user['firstName'],
        user['lastName'],
        user['gender'],
        user['level']
    ) for index, user in user_df.iterrows()), page_size=100)

    # insert songplay records 
    psycopg2.extras.execute_values(cur,songplay_table_insert, ((
        row['ts'],
        row['userId'],
        row['level'],
        select_song_and_artist_id(cur, row.song, row.artist, row.length)[0],
        select_song_and_artist_id(cur, row.song, row.artist, row.length)[1],
        row['sessionId'],
        row['location'],
        row['userAgent']
    )for index, row in df.iterrows()), page_size=100 )

def process_data(cur, conn, filepath, func):
    """
    Iterate over the files and process the data to insert them into tables.
    
    Parameters
    ----------
    cur : str
        Cursor of the database connection.
    conn: str
        Connection to the database
    filepath : str
        Path of the song json file to process
    func:
        Function used to process the json file according to the information.
    """ 
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres password=postgres")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()