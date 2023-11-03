import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

site_list = spacex_df['Launch Site'].unique().tolist()
opt_list = [{'label': site, 'value': site} for site in site_list]
options = [{'label': 'All Sites', 'value': 'ALL'}]
options.extend(opt_list)


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id='site-dropdown',
                                             options=options,
                                             value='ALL',
                                             placeholder="Choose Launch Site",
                                             searchable=True
                                            ),                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                marks={
                                                    0: '0 kg',
                                                    1000: '1000 kg',
                                                    2000: '2000 kg',
                                                    3000: '3000 kg',
                                                    4000: '4000 kg',
                                                    5000: '5000 kg',
                                                    6000: '6000 kg',
                                                    7000: '7000 kg',
                                                    8000: '8000 kg',
                                                    9000: '9000 kg',
                                                    10000: '10000 kg'
                                                },
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class',
                     names='Launch Site',
                     title='Total Success Launches by Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df,
                     names='class',
                     title=f'Total Success Launches for site {entered_site}')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value"))
def get_pie_chart(entered_site, min_max):
    min, max = min_max
    mask = (spacex_df['Payload Mass (kg)'] >= min) & (spacex_df['Payload Mass (kg)'] <= max)
    filtered_df = spacex_df[mask]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',                         
                         title='Correlation between Payload and Success for all Sites',
                         hover_data=['Launch Site'],
                         color="Booster Version Category")
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',                         
                         title=f'Correlation between Payload and Success by {entered_site}',
                         hover_data=['Launch Site'],
                         color="Booster Version Category")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
