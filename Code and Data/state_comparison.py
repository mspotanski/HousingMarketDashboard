# us_map.py



import plotly.graph_objs as go
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import dash

app = dash.register_page(__name__)

state_to_code = {
    "United States": "USA" ,
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", 
}

def year_quarter_to_id(year, quarter):
    return (year - 2018) * 4 + (quarter - 1)

def id_to_year_quarter(quarter_id):
    year = 2018 + quarter_id // 4
    quarter = 1 + quarter_id % 4
    return year, quarter

def display_state_details(clickData, year, quarter):
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
home_sale_price_path = 'Metro_median_sale_price_uc_sfrcondo_sm_sa_month.csv'
income_data = pd.read_csv(income_data_path)
loan_data = pd.read_csv(loan_data_path)
home_sale_data = pd.read_csv(home_sale_price_path)

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
# Clean Median Home Sale Price Data
home_sale_data.at[0, 'StateName'] = 'USA'
home_sale_data = home_sale_data.drop(['SizeRank', 'RegionType', 'RegionID', 'RegionName'], axis=1)

# Melt home_sale_data on StateName
home_sale_data = pd.melt(home_sale_data, id_vars=['StateName'])

# Rename columns to ['state_name', 'date', 'median_home_price']
home_sale_data.rename(columns={'StateName': 'state', 'variable': 'date', 'value': 'median_home_price'}, inplace=True)

# Group home_sale_data by state and date
# Take median of aggregation on median_home_price
# State is already in Abbreviated Terms
home_sale_data = home_sale_data.groupby(['state', 'date'])
home_sale_data = home_sale_data['median_home_price'].median()
home_sale_data = home_sale_data.reset_index()
home_sale_data['date'] = pd.to_datetime(home_sale_data['date'])
home_sale_data['median_home_price'] = pd.to_numeric(home_sale_data['median_home_price'])


# layout = html.Div([
#     html.H1('US Housing Price Index Map'),
#     dcc.Graph(id='us-map'),
#     dcc.Slider(
#         id='year-slider',
#         min=min(unique_years),
#         max=max(unique_years),
#         value=min(unique_years),
#         marks={str(year): str(year) for year in unique_years},
#         step=None
#     ),
#     html.Div(id='state-details-container'),
# ])
layout = html.Div([
    html.H1('State Comparison', className='mb-4'),
    html.Div([
        html.Label("Select State 1:", className='mr-2'),
        dcc.Dropdown(
            id='state-dropdown-1',
            options=state_options,
            value='AL'
        ),
        html.Label("Select State 2:", className='mr-2'),
        dcc.Dropdown(
            id='state-dropdown-2',
            options=state_options,
            value='AK'
        )
    ], className='form-group'),
    html.Div([
        html.Div([
            dcc.Graph(id='state-comparison-graph'),
        ], className='col-6'),
        html.Div([
            dcc.Graph(id='median_home_chart'),
        ], className='col-6'),
    ], className='row'),
], className='container')
@callback(
    Output('state-comparison-graph', 'figure'),
    [Input('state-dropdown-1', 'value'), Input('state-dropdown-2', 'value')]
)
def update_comparison_graph(state_code_1, state_code_2):

    state_1_income_data = income_data_cleaned[income_data_cleaned['StateCode'] == state_code_1]

    state_2_income_data = income_data_cleaned[income_data_cleaned['StateCode'] == state_code_2]

    comparison_fig = go.Figure()

    comparison_fig.add_trace(go.Scatter(
        x=years,
        y=state_1_income_data[income_columns].values.flatten(),
        mode='lines+markers',
        name=f'Median Income {state_code_1}'
    ))

    comparison_fig.add_trace(go.Scatter(
        x=years,
        y=state_2_income_data[income_columns].values.flatten(),
        mode='lines+markers',
        name=f'Median Income {state_code_2}'
    ))

    comparison_fig.update_layout(
        title_text="Comparison of Median Household Income Over Years",
        xaxis_title="Year",
        yaxis_title="Median Household Income"
    )

    return comparison_fig
@callback(
    Output('median_home_chart', 'figure'),
    [Input('state-dropdown-1', 'value'), Input('state-dropdown-2', 'value')]
)

def update_median_home_graph(state_option_1, state_option_2):
    house_sale_fig = go.Figure()

    if state_option_1 != 'AK':
        state_1_house_sale_data = home_sale_data[home_sale_data['state'] == state_option_1]
        house_sale_fig.add_trace(go.Scatter(
            x=state_1_house_sale_data['date'],
            y=state_1_house_sale_data['median_home_price'],
            mode='lines+markers',
            name=f'Median Sale Price for {state_option_1}'
        ))

    if state_option_2 != 'AK':
        state_2_house_sale_data = home_sale_data[home_sale_data['state'] == state_option_2]
        house_sale_fig.add_trace(go.Scatter(
            x=state_2_house_sale_data['date'],
            y=state_2_house_sale_data['median_home_price'],
            mode='lines+markers',
            name=f'Median Sale Price for {state_option_2}'
        ))

    annotations = []
    if state_option_1 == 'AK' or state_option_2 == 'AK':
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=1, text='Data not available for Alaska', showarrow=False))
   

    house_sale_fig.update_layout(
        title_text="Comparison of Median Home Sale Price Over Time",
        xaxis_title="Date",
        yaxis_title="Median Home Sale Price",
        annotations=annotations,
        # showlegend=True
    )

    return house_sale_fig