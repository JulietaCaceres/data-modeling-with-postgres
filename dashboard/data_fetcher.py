DEFAULT_CONN_STR = "host=127.0.0.1 dbname=sparkifydb user=postgres password=postgres"
import psycopg2
import pandas as pd

class DataFetcher:
    """
    - Connects to the sparkifydb
    - Gets data to use in graphics
    """ 
    def __init__(self, connstr=DEFAULT_CONN_STR):
         # connect to default database
        self.conn = psycopg2.connect(connstr)
        self.conn.set_session(autocommit=True)

    def songs_played(self, n_top=5 ):
        """
        Execute a query to songplays table to obtain the n_top rancking of songs that were played.
    
        Parameters
        ---------
        n_top: int, limit of the rancking to be desplayed.

        Returns
        -------
        DataFrame[times_played, title]: return a data frame with all the titles of the songs played and the times were played.

        """
        cur = self.conn.cursor()
        query = f"SELECT times_played, title " \
                f"FROM (( " \
                    f"SELECT COUNT(*) AS times_played, song_id " \
                    f"FROM songplays " \
                    f"GROUP BY song_id) AS t1 " \
                    f"LEFT JOIN songs " \
                    f"USING(song_id))" \
                f"ORDER BY times_played DESC " \
                f"LIMIT {n_top};"
        cur.execute(query)
        return pd.DataFrame(cur.fetchall(), columns=['times_played', 'title'])

    
    def songs_played_by_location(self, location=None):
        """
        Execute a query to sonplays table to obtain the time songs were played by location.
        
        Parameters
        ----------
        location: str, default value None.
            None: if location is not specified then the funtion returns songs played in all the locations
            str: location that is used to returns the songs played in the specific location.
        
        Returns
        -------
        DataFrame[times_played, title, artist, location]: 
            return a data frame with the times that a song is played, the title and artist of the song,
            and the location where was played
        """
        cur = self.conn.cursor()
        if not location:
            query="""
            SELECT t1.times_played, s.title, a.name AS artist, t1.location
            FROM(
                (SELECT COUNT(*) AS times_played, song_id, location
                FROM songplays
                GROUP BY song_id, location) AS t1
                JOIN songs AS s
                ON t1.song_id = s.song_id
                JOIN artists AS a
                ON s.artist_id = a.artist_id
            )
            """
        else:
            query=f"SELECT COUNT(*) AS times_played, title, artist, location"\
                  f"FROM songplays" \
                  f"JOIN songs" \
                  f"USING(song_id)" \
                  f"JOIN artists AS a" \
                  f"ON songplays.artist_id = artists.artist_id" \
                  f"WHERE songplays.location = {location}"
                  
        cur.execute(query)
        return pd.DataFrame(cur.fetchall(), columns=['times_played', 'title', 'artist', 'location'])


    def main_locations(self, n_top=5):
        """
        Execute a query to sonplays table to obtain the locations most frequently use the plataform.
        
        Parameters
        ---------
        n_top: int, limit of the rancking to be desplayed.
       
        Returns
        -------
        DataFrame[times_played, location]: 
            return a data frame with the times that a song is played and the location where was played
        """
        cur = self.conn.cursor()
        query= f"SELECT COUNT(*) AS times_played, location " \
               f"FROM songplays " \
               f"GROUP BY location " \
               f"ORDER BY times_played DESC " \
               f"LIMIT {n_top}"
                  
        cur.execute(query)
        return pd.DataFrame(cur.fetchall(), columns=['times_played', 'location'])

    def main_locations_by_year(self, n_top=5, year=2018):
        """
        Execute a query to sonplays table to obtain the locations most frequently use the plataform.
        
        Parameters
        ---------
        n_top: int, limit of the rancking to be desplayed.
       
        Returns
        -------
        DataFrame[times_played, location]: 
            return a data frame with the times that a song is played and the location where was played
        """
        cur = self.conn.cursor()
        query = f"WITH data_by_year AS (SELECT start_time " \
                        f"FROM time " \
                        f"WHERE year = {year}) " \
                f"SELECT COUNT(*) AS times_played, location " \
                f"FROM songplays " \
                f"JOIN data_by_year " \
                f"USING(start_time) " \
               f"GROUP BY location " \
               f"ORDER BY times_played DESC " \
               f"LIMIT {n_top}"
                                  
        cur.execute(query)
        return pd.DataFrame(cur.fetchall(), columns=['times_played', 'location'])

    def main_users(self, n_top=5):
        """
        Execute a query to sonplays table to obtain the users who most frequently use the plataform.
        
        Parameters
        ---------
        n_top: int, limit of the rancking to be desplayed.
       
        Returns
        -------
        DataFrame[times_played, user]: 
            return a data frame with the times that the users use the plataform
        """
        cur = self.conn.cursor()
        query= f"SELECT times_played, user_id, first_name, last_name " \
               f"FROM ((( " \
                    f"SELECT COUNT(*) AS times_played, user_id " \
                    f"FROM songplays " \
                    f"GROUP BY user_id) AS t1" \
                    f"LEFT JOIN users " \
                    f"USING(user_id))) AS t2 " \
               f"ORDER BY times_played DESC " \
               f"LIMIT {n_top}"
                  
        cur.execute(query)
        return pd.DataFrame(cur.fetchall(), columns=['times_played', 'user_id', 'first_name', 'last_name'])

    def main_users_by_year(self, n_top=5, year=2018):
        """
        Execute a query to sonplays table to obtain the users who most frequently use the plataform.
        
        Parameters
        ---------
        n_top: int, limit of the rancking to be desplayed.
       
        Returns
        -------
        DataFrame[times_played, user]: 
            return a data frame with the times that the users use the plataform
        """
        cur = self.conn.cursor()
        query= f"SELECT times_played, user_id, first_name, last_name " \
               f"FROM ((( " \
                    f"SELECT COUNT(*) AS times_played, user_id " \
                    f"FROM songplays " \
                    f"WHERE year = {year} " \
                    f"GROUP BY user_id) AS t1" \
                    f"LEFT JOIN users " \
                    f"USING(user_id))) AS t2 " \
               f"ORDER BY times_played DESC " \
               f"LIMIT {n_top}"
                  
        cur.execute(query)
        return pd.DataFrame(cur.fetchall(), columns=['times_played', 'user_id', 'first_name', 'last_name'])

    def hour_most_used(self):
        """
        Execute a query to sonplays table to obtain the hours with more traffic of users.
       
        Returns
        -------
        DataFrame[times_played, hour]: 
            return a data frame with the times that the users use the plataform
        """
        cur = self.conn.cursor()
        query= f"SELECT COUNT(*) AS times_played, hour " \
                f"FROM( " \
                    f"SELECT songplay_id, hour " \
                    f"FROM songplays " \
                    f"LEFT JOIN time " \
                    f"USING(start_time)) AS t1 " \
                f"GROUP BY t1.hour " \
                f"ORDER BY hour"
                  
        cur.execute(query)
        return pd.DataFrame(cur.fetchall(), columns=['times_played', 'hour'])
        
    def time_most_used(self, time_selected):
        """
        Execute a query to sonplays table to obtain the hours with more traffic of users.
       
        Returns
        -------
        DataFrame[times_played, hour]: 
            return a data frame with the times that the users use the plataform
        """
        cur = self.conn.cursor()
        query= f"SELECT COUNT(*) AS times_played, {time_selected} " \
                f"FROM( " \
                    f"SELECT songplay_id, t.{time_selected} " \
                    f"FROM songplays " \
                    f"LEFT JOIN time as t " \
                    f"USING(start_time)) AS t1 " \
                f"GROUP BY t1.{time_selected} " \
                f"ORDER BY {time_selected}"
                  
        cur.execute(query)
        return pd.DataFrame(cur.fetchall(), columns=['times_played', time_selected])
        
