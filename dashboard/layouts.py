import dash_core_components as dcc
import dash_html_components as html
import dash_table
from datetime import datetime as dt
from datetime import date, timedelta
import pandas as pd
from data_fetcher import *
import plotly.express as px

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

data_fetcher = DataFetcher()

#data frame with songs played by location
main_locations = data_fetcher.main_locations(10)

#Ranking songs most played
main_locations_bar = px.bar(data_frame=main_locations, x="location", y="times_played", color='times_played')

#data frame with songs played
main_users = data_fetcher.main_users()

#Top 5 songs most played
main_users_bar = px.bar(data_frame=main_users, x="last_name", y="times_played", color='user_id')

#Data frame with hours and times played
hour_most_used = data_fetcher.hour_most_used()

hour_most_used_line = px.line(hour_most_used, x="hour", y="times_played", line_shape="spline", render_mode="svg")

#Change the background of the plot.
main_locations_bar.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

hour_most_used_line.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

main_users_bar.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

introduction_message = """
## Introduction

This is a basic dashboard of the data recolected form sparkify web page.   
The principal goal is show a quick review over the data and behivor of the users.
"""
ranking_locations_message = """
## Ranking Locations in which the platafrom is used most frequently.

Bellow we can find the 5 locations which have more interaction with the application.  
You can change the amount of location displayed.
"""


traffic_message = """
## Traffic on the page over time.

The following graph shows the evolution through the time of the traffic in the web site.  
You can select the period of time (hour, mounth, year).
"""

users_message = """
## Ranking users who most frequently use the app
Bellow you can find the top 5 users who most use the app.  
Placing the mouse over the graph you can find the corresponding user id for each 
"""

######################## START Sparkify Report Layout ########################

layout_sparkify_report = html.Div(style={'backgroundColor': colors['background']}, children=[

    html.H1(children='Sparkify Report',
            style={
            'textAlign': 'center',
            'color': colors['text'],
        }),

    dcc.Markdown(children=introduction_message,
    style={
        'color': colors['text']
    }),

    dcc.Markdown(children=ranking_locations_message,
    style={
        'color':  colors['text']
    }),

    html.Label(children='n ranking',
    style={
        'color' : colors['text']
    }),
    dcc.Input(id='n-locations', value=5, type='number'),

    dcc.Graph(
        id='locations-graph',
        figure=main_locations_bar
    ),
    
    dcc.Markdown(children=traffic_message,
    style={
        'color':  colors['text']
    }),
    html.Label(children='Select unit of time',
    style={
        'color': colors['text']
    }),
    dcc.Dropdown(
        id='unit-time',
        options=[
            {'label': 'Hour', 'value': 'hour'},
            {'label': 'Month', 'value': 'month'},
            {'label': 'Year', 'value': 'year'},
        ],
        value='hour'
    ),    

    dcc.Graph(
        id='plays_over_the_time',
        figure=hour_most_used_line
    ),
    dcc.Markdown(children=users_message,
    style={
        'color': colors['text']
    }),
    
    html.Label(children='n ranking',
    style={
        'color' : colors['text']
    }),
    dcc.Input(id='n-users', value='5', type='number'),

    dcc.Graph(
        id='top_users',
        figure=main_users_bar
    )    
])

######################## END Sparkify Report Layout ########################

######################## START No Page Layout ########################

noPage = html.Div(style={'backgroundColor': colors['background']}, children=[

    html.H1(children='No page',
            style={
            'textAlign': 'center',
            'color': colors['text'],
        })])