# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id = 'site-dropdown', 
                                options = [{'label':'All sites','value':'ALL'},
                                {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'}],
                                value='ALL',
                                searchable=True
                                ),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                        100: '100',
                                                        2500: '2500',
                                                        5000: '5000',
                                                        7500: '7500',
                                                        10000: '10000'},
                                                value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output('success-pie-chart','figure'),
            [Input('site-dropdown','value')])
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        figure = px.pie(spacex_df , values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
    else:
        df2 = spacex_df[spacex_df['Launch Site']== entered_site][['Launch Site','class']]
        figure = px.pie(df2 ,  names='class', 
        title='Total Success Launches for site {}'.format(entered_site))
    return figure
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart','figure'),
            [Input('site-dropdown','value'),Input('payload-slider','value')])
def vars(entered_site,val2):
    if entered_site =='ALL':
        df4= spacex_df[spacex_df['Payload Mass (kg)'] < val2[1]]
        df5= df4[df4['Payload Mass (kg)'] > val2[0]]
        figure = px.scatter(data_frame=df5, x='Payload Mass (kg)' , y='class', color='Booster Version Category', title='Correlation between Payload and Success for all Sites')
    else:
        df3 = spacex_df[spacex_df['Launch Site']== entered_site]
        df4= df3[df3['Payload Mass (kg)'] < val2[1]]
        df5= df4[df4['Payload Mass (kg)'] > val2[0]]
        figure = px.scatter(data_frame=df5, x='Payload Mass (kg)' , y='class', color='Booster Version Category')

    return figure


# Run the app
if __name__ == '__main__':
    app.run_server()
