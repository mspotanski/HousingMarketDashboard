# index.py
from dash import dcc, html
import dash
app = dash.register_page(__name__)
layout = html.Div([
    html.H1('Welcome to the US Housing Dashboard!', className='mb-4'),
    html.Div([
        dcc.Link('US Map Data', href='/us-map', className='list-group-item list-group-item-action'),
        dcc.Link('State Comparison', href='/state-comparison', className='list-group-item list-group-item-action'),
        dcc.Link('Custom Rate Comparison', href='/custom-rate', className='list-group-item list-group-item-action'),
    ], className='list-group')
], className='container')