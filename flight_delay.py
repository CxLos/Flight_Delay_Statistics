# IMPORTS ---------------------------------------------------------------------------------------------------
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc, html
# from dash import html
from dash.dependencies import Input, Output
from dash.development.base_component import Component
import os
import sys

# DATA--------------------------------------------------------------------------------------------------

# data = r'C:\Users\CxLos\OneDrive\Documents\IBM Data Analyst Professional Certificate\IBM Practice Labs\8. Data Visualization with Python\W4 - Creating Dashboards with Plotly and Dash\Data\airline_data.csv'

# WORKING DIRECTORY ----------------------------------------------------------------------

# Get the current working directory
current_dir = os.getcwd()
# print('Current Directory:', current_dir)
# print(os.listdir(current_dir))

# Join the 'Data' directory to the current working directory
imm_dir = os.path.join(current_dir, "Flight_Delay_Statistics")

# List the files and directories in the 'Immigration Statistics 20 yrs' directory
# print(os.listdir(current_dir))

# Get the current directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
# print('Script Directory:', script_dir)

# Define the relative path to your CSV file
relative_path = 'Data/airline_data.csv'
# print('Relative Path:', relative_path)

# Join the script directory with the relative path to get the full file path
file_path = os.path.join(script_dir, relative_path)

# Read the CSV file using the full file path

airline_data = pd.read_csv(file_path,
                   encoding="ISO-8859-1",
                   dtype={'Div1Airport': str, 'Div1TailNum': str, 
                          'Div2Airport': str, 'Div2TailNum': str})

# print(airline_data.head())
# print(airline_data.columns)
# print(airline_data.dtypes)

# CREATE DASH APPLICATION ------------------------------------------------------------------------------

# Create a dash application layout
app = dash.Dash(__name__)
server= app.server

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add a html.Div and core input text component
# Finally, add graph component.
# Build dash app layout

# Define the layout of the app
app.layout = html.Div(children=[
    # Title
    html.H1(
        'Flight Delay Time Statistics',
        style={'textAlign': 'center', 'color': 'cadetblue', 'fontSize': 45, 'font-family': 'Calibri'}
    ),

    # Input box
    html.Div(
        [
            html.Span(
                "Input Year: ",
                style={'margin-left': '20px'}
            ),
            dcc.Input(
                id='input-year',
                value='2010',
                type='number',
                style={'height': '35px', 'font-size': 30, 'font-family': 'Calibri'}
            )
        ],
        style={'font-size': 30, 'font-family': 'Calibri'}
    ),

    html.Br(),
    html.Br(),

    # Segment 1
    html.Div(
        [
            html.Div(dcc.Graph(id='carrier-plot')),
            html.Div(dcc.Graph(id='weather-plot'))
        ],
        style={'display': 'flex'}
    ),

    # Segment 2
    html.Div(
        [
            html.Div(dcc.Graph(id='nas-plot')),
            html.Div(dcc.Graph(id='security-plot'))
        ],
        style={'display': 'flex'}
    ),

    # Segment 3
    html.Div(
        dcc.Graph(id='late-plot'),
        style={'width': '65%', 'margin': '0 auto'}
    )
])

# Define the function to compute the necessary data
def compute_info(airline_data, entered_year):
    # Select data
    df = airline_data[airline_data['Year'] == int(entered_year)]

    # Compute delay averages
    avg_car = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late

# Define the callback function to update the graphs
@app.callback([Output(component_id='carrier-plot', component_property='figure'),
               Output(component_id='weather-plot', component_property='figure'),
               Output(component_id='nas-plot', component_property='figure'),
               Output(component_id='security-plot', component_property='figure'),
               Output(component_id='late-plot', component_property='figure')],
              [Input(component_id='input-year', component_property='value')])
def get_graph(entered_year):
    # Compute required information for creating graph from the data
    avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(airline_data, entered_year)

    # Line plot for carrier delay
    carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline')
    carrier_fig.update_layout(
        title={'text': 'Average carrier delay time (minutes) by airline', 'x': 0.45},
        xaxis_title='Month',
        yaxis_title='Delay'
    )

    # Create the weather delay figure
    weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline')
    weather_fig.update_layout(
        title={'text': 'Average weather delay time (minutes) by airline', 'x': 0.45},
        xaxis_title='Month',
        yaxis_title='Delay'
    )

    # Create the NAS delay figure
    nas_fig = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline')
    nas_fig.update_layout(
        title={'text': 'Average NAS delay time (minutes) by airline', 'x': 0.45},
        xaxis_title='Month',
        yaxis_title='Delay'
    )

    # Create the security delay figure
    sec_fig = px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline')
    sec_fig.update_layout(
        title={'text': 'Average security delay time (minutes) by airline', 'x': 0.45},
        xaxis_title='Month',
        yaxis_title='Delay'
    )

    # Create the late aircraft delay figure
    late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline')
    late_fig.update_layout(
        title={'text': 'Average late aircraft delay time (minutes) by airline', 'x': 0.45},
        xaxis_title='Month',
        yaxis_title='Delay'
    )

    return [carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

# Prints ------------------------------------------------------------------------------------------------

# print(airline_data.head())

#  KILL PORT --------------------------------------------

# netstat -ano | findstr :8050
# taskkill /PID 24772 /F
# npx kill-port 8050

# Host Application ------------------------------

# 1. pip freeze > requirements.txt
# 2. add this to procfile: 'web: gunicorn <your_app_filename>:app'
# 3. heroku login
# 4. heroku create
# 5. git push heroku main

# Update PIP Setup Tools:
# pip install --upgrade pip setuptools

# Install all dependencies in the requirements file:
# pip install -r requirements.txt

# Check dependency tree:
# pipdeptree
# pip show package-name

# Clear Heroku Cache:
# heroku plugins:install heroku-repo
# heroku repo:purge_cache -a flight-delay-statistics

# Heroku:
# heroku login
# heroku create flight-delay-statistics
# heroku git:remote -a flight-delay-statistics
# heroku ps:scale web=1  # run the app with a 1 heroku "dyno"
# git push heroku main

# Set Buildpack
# heroku buildpacks:set heroku/python
