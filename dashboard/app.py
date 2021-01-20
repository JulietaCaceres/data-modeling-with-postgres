import dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
               "https://codepen.io/bcd/pen/YaXojL.js"]
app = dash.Dash(__name__,external_scripts=external_js, external_stylesheets=external_stylesheets, url_base_pathname='/sparkify-report/')
server = app.server
app.config.suppress_callback_exceptions = True

