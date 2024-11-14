# us_map.py
# import dash_core_components as dcc
from dash import dcc, html, Input, Output, callback

import plotly.graph_objs as go
import pandas as pd
import dash
app = dash.register_page(__name__)

state_to_code = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "United States": "USA" 
}

def year_quarter_to_id(year, quarter):
    return (year - 2018) * 4 + (quarter - 1)

def id_to_year_quarter(quarter_id):
    year = 2018 + quarter_id // 4
    quarter = 1 + quarter_id % 4
    return year, quarter

def display_state_details(clickData, year, quarter, bola):
    if bola == False:
        return None
    if clickData is None:
        return html.Div("Click on a state to see more details.", style={'color': 'gray', 'font-size': '16px'})

    state_code = clickData['points'][0]['location']
    state_data = loan_data[
        (loan_data['State'] == state_code) & 
        ((loan_data['Year'] == year) & (loan_data['Quarter'] == quarter))
    ].iloc[0]

    return html.Div([
        html.H4("State Details", style={'textAlign': 'center', 'margin-bottom': '20px'}),
        html.Table([
            html.Tr([html.Td("State:", style={'padding': '8px', 'background': '#f2f2f2'}),
                     html.Td(state_data['State'], style={'padding': '8px'})]),
            html.Tr([html.Td("Year:", style={'padding': '8px', 'background': '#f2f2f2'}),
                     html.Td(state_data['Year'], style={'padding': '8px'})]),
            html.Tr([html.Td("Quarter:", style={'padding': '8px', 'background': '#f2f2f2'}),
                     html.Td(f"Q{state_data['Quarter']}", style={'padding': '8px'})]),
            html.Tr([html.Td("Median Home Price:", style={'padding': '8px', 'background': '#f2f2f2'}),
                     html.Td(f"${state_data['Median_Home_Price']:,.2f}", style={'padding': '8px'})]),
            html.Tr([html.Td("Mortgage Rate:", style={'padding': '8px', 'background': '#f2f2f2'}),
                     html.Td(f"{state_data['Mortgage_rate']}%", style={'padding': '8px'})]),
            html.Tr([html.Td("Monthly Loan Payment:", style={'padding': '8px', 'background': '#f2f2f2'}),
                     html.Td(f"${state_data['Monthly_loan_payment']:,.2f}", style={'padding': '8px'})]),
            html.Tr([html.Td("Min. Income Needed (Monthly):", style={'padding': '8px', 'background': '#f2f2f2'}),
                     html.Td(f"${state_data['Minimum_income_needed_monthly']:,.2f}", style={'padding': '8px'})]),
            html.Tr([html.Td("Min. Income Needed (Yearly):", style={'padding': '8px', 'background': '#f2f2f2'}),
                     html.Td(f"${state_data['Minimum_income_needed_yearly']:,.2f}", style={'padding': '8px'})])
        ], style={
            'border-collapse': 'collapse',
            'width': '100%',
            'border': '1px solid #ddd',
            'box-shadow': '0 2px 4px rgba(0,0,0,0.1)',
            'border-radius': '5px',
            'background': '#fff',
            'margin-top': '20px'
        })
    ], style={
        'padding': '20px',
        'border': '1px solid #ddd',
        'box-shadow': '0 4px 8px rgba(0,0,0,0.1)',
        'border-radius': '5px',
        'background': '#fff',
        'margin-top': '20px'
    })




start_id = year_quarter_to_id(2018, 3)
end_id = year_quarter_to_id(2024, 1)

income_data_path = 'h08.csv'
loan_data_path = 'merged_data_with_loan_payment_and_income.csv'
income_data = pd.read_csv(income_data_path)
loan_data = pd.read_csv(loan_data_path)

income_data_cleaned = income_data[income_data['State'].notna()].copy()
income_columns = [col for col in income_data.columns if col.isdigit()]
years = [int(year) for year in income_columns]

for col in income_columns:
    income_data_cleaned.loc[:, col] = pd.to_numeric(income_data_cleaned[col].astype(str).str.replace(',', ''), errors='coerce')

income_data_cleaned['StateCode'] = income_data_cleaned['State'].map(state_to_code)

hpi_data_path = 'HPI_EXP_state.txt'
hpi_data = pd.read_csv(hpi_data_path, delimiter='\t')
hpi_data['StateCode'] = hpi_data['state']

unique_years = hpi_data['yr'].unique()
unique_years.sort()
state_options = [{'label': state, 'value': code} for state, code in state_to_code.items()]

layout = html.Div([
    html.H1('US Housing Maps', className='mb-4'),
    dcc.Dropdown(
        id='map-dropdown',
        options=[
            {'label': 'Minimum Monthly Income Needed', 'value': 'income'},
            {'label': 'Housing Price Index', 'value': 'hpi'}
        ],
        value='income'
    ),
    dcc.Graph(id='us-map'),
    html.Div(id='slider-container'),
    html.Div(id='state-details-container'),
], className='container')

@callback(
    Output('slider-container', 'children'),
    [Input('map-dropdown', 'value')]
)
def update_slider(selected_map):
    if selected_map == 'income':
        return dcc.Slider(
            id='slider',
            min=start_id,
            max=end_id,
            value=start_id,
            marks={year_quarter_to_id(y, q): f'{y} Q{q}' for y in range(2018, 2025) for q in range(1, 5) if (y > 2018 or q >= 3) and (y < 2024 or q <= 1)},
            step=1
        )
    else:
        return dcc.Slider(
            id='slider',
            min=min(unique_years),
            max=max(unique_years),
            value=min(unique_years),
            marks={str(year): str(year) for year in unique_years},
            step=None
        )

@callback(
    Output('us-map', 'figure'),
    [Input('map-dropdown', 'value'),
     Input('slider', 'value')]
)
def update_map(selected_map, slider_value):
    if selected_map == 'income':
        year, quarter = id_to_year_quarter(slider_value)
        selected_quarter_str = f"{year} Q{quarter}"
        quarterly_data = loan_data[(loan_data['Year'] == year) & (loan_data['Quarter'] == quarter)]
        
        fig = go.Figure(data=go.Choropleth(
            locations=quarterly_data['State'],
            z=quarterly_data['Minimum_income_needed_monthly'].astype(float),
            text=quarterly_data['State'],
            locationmode='USA-states',
            colorscale='Greens',
            marker_line_color='white',
            colorbar_title="Minimum Income Needed Monthly"
        ))
        
        fig.update_layout(
            title_text=f'US Minimum Monthly Income Needed by State for {selected_quarter_str}',
            geo=dict(
                scope='usa',
                projection=go.layout.geo.Projection(type='albers usa'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'),
            margin=dict(l=0, r=0, t=40, b=0)
        )
    else:
        selected_year = slider_value
        filtered_hpi_data = hpi_data[hpi_data['yr'] == selected_year]
        
        if selected_year == 1991 and filtered_hpi_data['index_nsa'].unique()[0] == 100:
            colorscale = [[0, 'rgb(200, 0, 0)'], [1, 'rgb(200, 0, 0)']]
            zmin = zmax = 100
        else:
            colorscale = 'Reds'
            zmin = filtered_hpi_data['index_nsa'].min()
            zmax = filtered_hpi_data['index_nsa'].max()
        
        fig = go.Figure(data=go.Choropleth(
            locations=filtered_hpi_data['StateCode'],
            z=filtered_hpi_data['index_nsa'].astype(float),
            locationmode='USA-states',
            colorscale=colorscale,
            zmin=zmin,
            zmax=zmax,
            marker_line_color='white',
            colorbar_title="Housing Price Index"
        ))
        
        fig.update_layout(
            title_text=f'US Housing Price Index by State for {selected_year}',
            geo=dict(
                scope='usa',
                projection=go.layout.geo.Projection(type='albers usa'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'),
            margin=dict(l=0, r=0, t=40, b=0)
        )
    
    return fig

@callback(
    Output('state-details-container', 'children'),
    [Input('us-map', 'clickData'),
    Input('slider', 'value'),
    Input('map-dropdown', 'value')]
)
def update_state_details(clickData, slider_value, selected_map):
    if selected_map == 'income':
        year, quarter = id_to_year_quarter(slider_value)
        bola = True
    else:
        year, quarter = slider_value, 1, 
        bola = False
    
    return display_state_details(clickData, year, quarter, bola)