# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays(
    songplay_id SERIAL PRIMARY KEY,
    start_time BIGINT NOT NULL,
    user_id INT NOT NULL, 
    level text, 
    song_id text,
    artist_id text, 
    session_id text, 
    location text,
    user_agent text, 
    CONSTRAINT fk_user FOREIGN KEY(user_id) 
        REFERENCES users(user_id), 
    CONSTRAINT fk_song FOREIGN KEY(song_id)
        REFERENCES songs(song_id),
    CONSTRAINT fk_artist FOREIGN KEY(artist_id)
        REFERENCES artists(artist_id))      
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users(
    user_id INT PRIMARY KEY, 
    first_name text, 
    last_name text, 
    gender text, 
    level text)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs(
    song_id text PRIMARY KEY, 
    title text,
    artist_id text NOT NULL,
    year INT,
    duration FLOAT)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists(
    artist_id text PRIMARY KEY, 
    name text, 
    location text, 
    latitude NUMERIC(6,2), 
    longitude NUMERIC(6,2))
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time(
    start_time BIGINT PRIMARY KEY, 
    hour INT, 
    day text, 
    week INT, 
    month text, 
    year INT, 
    weekday text)
""")


# INSERT RECORDS

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
    VALUES (%s, %s, %s, %s,%s)
    ON CONFLICT DO NOTHING
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s,%s) 
ON CONFLICT DO NOTHING
""")

time_table_insert = 'INSERT INTO time VALUES %s ON CONFLICT DO NOTHING'

user_table_insert = 'INSERT INTO users (user_id , first_name, last_name, gender, level) VALUES (%s, %s, %s, %s, %s)  ON CONFLICT(user_id) DO UPDATE SET level=EXCLUDED.level'

songplay_table_insert = 'INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) VALUES %s'

# FIND SONGS

song_select = ("""
SELECT s.song_id, s.artist_id
FROM(
    songs AS s
    JOIN artists AS a
    ON s.artist_id = a.artist_id)
WHERE s.title = %s AND a.name = %s AND s.duration = %s""")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]