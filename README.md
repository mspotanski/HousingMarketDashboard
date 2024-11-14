# US Housing Market Analysis Dashboard
### This dashboard was made as a collaborative class project at the University of Minnesota between Akshat Ghoshal, Rohan Shanbhag, and Marcus Spotanski. 

This repository contains a Dash application that provides an interactive dashboard for analyzing housing market trends across the United States. The dashboard allows users to explore key data points such as the Housing Price Index, median household income, median home sale prices, minimum income needed, mortgage rates, and monthly payments for different states and time periods. This dashboard was made as a collaborative class project at the University of Minnesota between Akshat Ghoshal, Rohan Shanbhag, and Marcus Spotanski.

For a concise recount of the project and its key findings, see the final report and presentation! Below, you'll find a quick run down on how to use the dashboard and the code. 

## Features

- Interactive choropleth map of the United States displaying housing market data by state
- Dropdown menu to switch between different data points (Housing Price Index and Minimum Monthly Income Needed)
- Sliders to select specific years or quarters for data analysis
- Customizable comparison of monthly mortgage payments using user-defined interest rates
- Easy-to-read and digestible data presentation
## Dependencies
pip install dash dash-bootstrap-components pandas plotly

## Running

Navigate to the project directory:

then run app.py

Open a web browser and visit http://localhost:8050/ to access the dashboard.


The dashboard utilizes the following data sources:

Housing Price Index (HPI) data: HPI_EXP_state.txt
Median household income data: h08.csv
Loan, housing, and income data(derived): merged_data_with_loan_payment_and_income.csv
Sale Price: Metro_median

