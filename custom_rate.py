import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objs as go
import plotly.express as px
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
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
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

# layout = html.Div([
#     html.H1("US States Housing Index and Median Income Interactive Map"),
#     dcc.Graph(id='us-map'),
#     dcc.Slider(
#         id='year-slider',
#         min=min(unique_years),
#         max=max(unique_years),
#         value=min(unique_years),
#         marks={str(year): str(year) for year in unique_years},
#         step=None
#     ),
#     html.Div([
#         html.Label("Select State 1:"),
#         dcc.Dropdown(
#             id='state-dropdown-1',
#             options=state_options,
#             value='AL'  
#         ),
#         html.Label("Select State 2:"),
#         dcc.Dropdown(
#             id='state-dropdown-2',
#             options=state_options,
#             value='AK'  
#         )
#     ]),
#     dcc.Graph(id='state-comparison-graph'),
#     dcc.Graph(id='quarterly-us-map'),
#     dcc.Slider(
#         id='quarter-slider',
#         min=start_id,
#         max=end_id,
#         value=start_id,
#         marks={year_quarter_to_id(y, q): f'{y} Q{q}' for y in range(2018, 2025) for q in range(1, 5) if (y > 2018 or q >= 3) and (y < 2024 or q <= 1)},
#         step=1
#     ),
#     html.Div(id='state-details-container'),
#     html.Div([
#         html.Label("Select State for Custom Rate Comparison:"),
#         dcc.Dropdown(
#             id='custom-rate-state-dropdown',
#             options=[{'label': state, 'value': code} for state, code in state_to_code.items()],
#             value='AL'
#         ),
#         html.Label("Enter Custom Interest Rate (%):"),
#         dcc.Input(id='custom-rate-input', type='number', value=4.5),  
#         html.Button('Submit', id='submit-rate')
#     ]),
#     dcc.Graph(id='custom-rate-graph')

# ])

layout = html.Div([
    html.H1('Custom Rate Comparison', className='mb-4'),
    html.Div([
        html.Label("Select State for Custom Rate Comparison:", className='mr-2'),
        dcc.Dropdown(
            id='custom-rate-state-dropdown',
            options=[{'label': state, 'value': code} for state, code in state_to_code.items()],
            value='AL'
        ),
        html.Label("Enter Custom Interest Rate (%):", className='mr-2'),
        dcc.Input(id='custom-rate-input', type='number', value=4.5, className='form-control'),
        html.Button('Submit', id='submit-rate', className='btn btn-primary')
    ], className='form-group'),
    dcc.Graph(id='custom-rate-graph')
], className='container')
@callback(
    Output('custom-rate-graph', 'figure'),
    [Input('submit-rate', 'n_clicks')],
    [State('custom-rate-state-dropdown', 'value'), State('custom-rate-input', 'value')]
)
def update_custom_rate_graph(n_clicks, selected_state, custom_rate):
    if n_clicks is not None and n_clicks > 0:
        filtered_data = loan_data[loan_data['State'] == selected_state]

        filtered_data['Monthly_Rate'] = filtered_data['Mortgage_rate'] / 1200
        custom_monthly_rate = custom_rate / 1200

        n_payments = 30 * 12

        filtered_data['Principal'] = filtered_data.apply(
            lambda row: row['Monthly_loan_payment'] * ((1 + row['Monthly_Rate'])**n_payments - 1) / (row['Monthly_Rate'] * (1 + row['Monthly_Rate'])**n_payments),
            axis=1
        )

        filtered_data['Custom_Monthly_Payment'] = filtered_data.apply(
            lambda row: (row['Principal'] * custom_monthly_rate * ((1 + custom_monthly_rate) ** n_payments)) / (((1 + custom_monthly_rate) ** n_payments) - 1),
            axis=1
        )

        filtered_data['Year_Quarter'] = filtered_data['Year'].astype(str) + ' Q' + filtered_data['Quarter'].astype(str)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_data['Year_Quarter'], y=filtered_data['Monthly_loan_payment'], mode='lines+markers', name='Actual Monthly Payment'))
        fig.add_trace(go.Scatter(x=filtered_data['Year_Quarter'], y=filtered_data['Custom_Monthly_Payment'], mode='lines+markers', name='Modified Monthly Payment'))

        fig.update_layout(
            title=f'Quarterly Comparison of Monthly Payments for {selected_state}',
            xaxis_title='Year and Quarter',
            yaxis_title='Monthly Payment ($)',
            legend_title='Payment Type'
        )

        return fig
    return go.Figure()