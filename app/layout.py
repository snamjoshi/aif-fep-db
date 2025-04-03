# import dash_bootstrap_components as dbc

import pandas as pd 

from dash import Dash, html, dash_table

# nav = dbc.Nav(
#     [
#         dbc.NavItem(dbc.NavLink("Active", active=True, href="#")),
#         dbc.NavItem(dbc.NavLink("A link", href="#")),
#         dbc.NavItem(dbc.NavLink("Another link", href="#")),
#         dbc.NavItem(dbc.NavLink("Disabled", disabled=True, href="#")),
#     ],
#     pills=True,
# )

# def create_layout(dash: Dash):

#     dash.layout = html.Div(children=[
#         html.H1(children='Hello Dash'),

#         html.Div(children='''
#             Dash: A web application framework for your data.
#         '''),
        
#     # Test
#     # Test again

#     ])
    
def create_layout(dash: Dash, database: pd.DataFrame):
    
    dash.layout = html.Div(
    children=[
        # dcc.Dropdown(
        #     id="filter_dropdown",
        #     options=[{"label": st, "value": st} for st in states],
        #     placeholder="-Select a State-",
        #     multi=True,
        #     value=df.State.values,
        # ),
        dash_table.DataTable(
            id="table-container",
            columns=[{"name": i, "id": i} for i in database.columns],
            data=database.to_dict("records")
        )
    ]
)
