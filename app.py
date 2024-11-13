# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output




external_stylesheets = [
    'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True, pages_folder="", suppress_callback_exceptions=True)
app.debug = False
from layouts import index_layout, us_map_layout, state_comparison_layout, custom_rate_layout

# Define the back button
back_button = html.Div([
    html.A(html.I(className='fa fa-arrow-left mr-2'), href='/', className='btn btn-link mt-2')  # Back button with arrow icon and btn-link class for minimal styling
], id='back-button')

app.layout = html.Div([
    back_button,  # Render the back button before the page content
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Output('back-button', 'style'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/us-map':
        return us_map_layout, {}
    elif pathname == '/state-comparison':
        return state_comparison_layout, {}
    elif pathname == '/custom-rate':
        return custom_rate_layout, {}
    else:
        return index_layout, {'display': 'none'}

if __name__ == '__main__':
    app.run_server(debug=False)