import dash_core_components as dcc
import dash_html_components as html
import dash_table
from components import Header, print_button
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

#Top 10 songs most played
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

######################## START Sparkify Report Layout ########################

layout_sparkify_report = html.Div(style={'backgroundColor': colors['background']}, children=[

    html.H1(children='Sparkify Report',
            style={
            'textAlign': 'center',
            'color': colors['text'],
        }),

    html.H2(children='Metrics',
    style={
            'color': colors['text'],
        }),
    html.H3(children='Top 10 Locations most frequently use the plataform.',
    style={
        'color':  colors['text']
    }),

    dcc.Graph(
        id='songs-played',
        figure=main_locations_bar
    ),
    html.H3(children='Times played over the time',
    style={
        'color':  colors['text']
    }),
    dcc.Graph(
        id='times_vs_hour',
        figure=hour_most_used_line
    ),
    html.H4(children='Top 5 users most frequently use the app',
    style={
        'color': colors['text']
    }),
    dcc.Graph(
        id='top_users',
        figure=main_users_bar
    )    
])

######################## 404 Page ########################
noPage = html.Div([ 
    # CC Header
    Header(),
    html.P(["404 Page not found"])
    ], className="no-page")




