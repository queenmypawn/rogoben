import dash
import dash_core_components as dcc
import dash_html_components as html
import rogobencharts as rc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1('HHCAHPS Survey Data'),
        html.Div('''
            A graphical, visual illustration of the HHCAHPS data contained in a .csv.
        '''),
        html.Div([
            html.H3('Average Star Ratings'),
            dcc.Graph(id='Chart 1', figure = rc.c1)
        ], className='nine columns'),

        html.Div([
            html.H3('Services Offered'),
            dcc.Graph(id='Chart 2', figure = rc.c2)
        ], className='nine columns'),

        html.Div([
            html.H3('Type of Ownership'),
            dcc.Graph(id='Chart 3', figure = rc.c3)
        ], className='nine columns'),
    ], className='column')
])

if __name__ == '__main__':
    app.run_server(debug=True)