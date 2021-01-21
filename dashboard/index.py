import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# see https://community.plot.ly/t/nolayoutexception-on-deployment-of-multi-page-dash-app-example-code/12463/2?u=dcomfort
from app import server
from app import app
from layouts import *
#from components import Header, print_button

import pandas as pd
import io
import xlsxwriter
from flask import send_file
from data_fetcher import *

data_fetcher = DataFetcher()

# see https://dash.plot.ly/external-resources to alter header, footer and favicon
app.index_string = ''' 
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Sparkify Report</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div>Sparkify Report</div>
    </body>
</html>
'''

app.layout = html.Div(style={'background': '#111111'},children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Update page
# # # # # # # # #
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/sparkify-report/':
        return layout_sparkify_report
    else:
        return noPage

@app.callback(
    Output('plays_over_the_time', 'figure'),
    Input('unit-time', 'value'))
def update_time_figure(selected_time):

    times_df = data_fetcher.time_most_used(selected_time)
    
    fig = px.line(times_df, x=selected_time, y="times_played", line_shape="spline", render_mode="svg")

    fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )

    return fig


@app.callback(
    Output('locations-graph', 'figure'),
    Input('n-locations', 'value'))
def update_n_location_graph(n_ranking):

    main_locations = data_fetcher.main_locations(n_ranking)
    
    fig = px.bar(data_frame=main_locations, x="location", y="times_played", color='times_played')

    fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )

    return fig


@app.callback(
    Output('top_users', 'figure'),
    Input('n-users', 'value'))
def update_n_users_graph(n_ranking):

    main_users = data_fetcher.main_users(n_ranking)
    
    fig = px.bar(data_frame=main_users, x="last_name", y="times_played", color='times_played')

    fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
