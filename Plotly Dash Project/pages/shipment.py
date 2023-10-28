import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
import pyodbc
import pandas as pd

dash.register_page(__name__)

layout = html.Div(
    style={'backgroundColor': 'white', 'padding': '20px'},
    children=[
        dmc.Group(
            position="center",
            align="center",
            spacing="xs",
            style={
                'margin-top': '40px'
            },
            children=[
                html.H2('Enter Shipment ID:', style={'color': '#20B2AA'}),
                dcc.Input(id='shipment-input', type='text'),
                html.Button('Submit', id='submit-button', n_clicks=0),
            ],
        ),
        html.H2(
            'Shipment Details:', 
            style={
                'color': '#FFE4B5', 
                'margin-top': '30px', 
                'background-color': 
                'gray', 'padding': '10px'
            }
        ),
        html.Div(
            id='shipment-details', 
            style={
                'margin-top': '10px', 
                'background-color': 'white', 
                'padding': '10px'
            }
        ),
    ]
)

# Callback function to handle button click and retrieve shipment details
@callback(
    Output('shipment-details', 'children'),
    Input('submit-button', 'n_clicks'),
    Input('shipment-input', 'value')
)
def retrieve_shipment_details(n_clicks, shipment_id):
    print('ship..#', n_clicks, shipment_id)
    if n_clicks > 0:
        # Establish a new connection to the SQL Server
        conn = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};'
            'Server=20.207.202.225;'
            'Database=Analysis Dashboard;'
            'UID=Hanumant;'
            'PWD=GIGtel@20152;'
        )

        # SQL query to retrieve shipment details based on the given Shipment ID
        shipment_details_query = f"""
            SELECT *
            FROM ShipmentProfile
            WHERE ShipmentID = '{shipment_id}'
        """

        # Execute the query and fetch the data into a DataFrame
        shipment_details_df = pd.read_sql(shipment_details_query, conn)

        # Close the database connection
        conn.close()

        print('shipment..#', shipment_details_df)
        
        if not shipment_details_df.empty:
            
            return html.Div(
                style = {
                    'overflow': 'auto'
                },
                children = [   
                    dmc.Table(
                        striped=True,
                        highlightOnHover=True,
                        withBorder=True,
                        withColumnBorders=True,
                        children = [
                            html.Thead(
                                html.Tr(
                                    [html.Th(col) for col in shipment_details_df.columns]
                                )
                            )
                        ] + [
                            html.Tbody([
                                html.Tr(
                                    [html.Td(data) for data in row]
                                ) for row in shipment_details_df.values
                            ])
                        ] 
                    ),
                ]
            )

        return html.Div('No shipment details found for the given Shipment ID.', style={'color': 'red'})

    return ''