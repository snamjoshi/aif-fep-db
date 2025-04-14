import pandas as pd

from dash import dcc, dash_table, html
from dash.dependencies import Input, Output, State
from itertools import chain


def create_layout(app, database: pd.DataFrame, metadata: dict, mapping: dict, tags: list):
    
    creation_time = metadata["creation_time"]
    tag_version = metadata["tag_version"]

    app.layout = html.Div([
        
        # Heading
        html.H1(children='A tagged database of active inference, predictive processing, and free energy principle papers'),
        
        dcc.Tabs([
            dcc.Tab(label="Database Table", children=[
            
                # Store
                dcc.Store(id="filtered_data_store"),
                
                html.Br(),
                
                html.P(children=f"Database creation time: {creation_time}"),
                html.P(children=f"Tag version: {tag_version}"),
                
                html.Br(),
                
                # Download button
                html.Button("Download CSV", id="btn_csv"),
                dcc.Download(id="download-dataframe-csv"),
                
                # Tag filter menu
                dcc.Dropdown(
                    id="filter_dropdown",
                    # options=[{"label": tag, "value": tag} for tag in tags],
                    options=tags,
                    placeholder="Select a tag",
                    multi=True,
                    value=tags,
                ),
                
                # Main table
                dash_table.DataTable(
                    id="database",
                    columns=[
                        {"name": i, "id": i} for i in database.columns],
                    data=database.to_dict("records"),
                    row_deletable=True,
                    filter_action="native",
                    sort_mode="multi",
                    sort_action="native",
                    style_header = {
                        'text_align': 'left',
                        'backgroundColor' : 'rgb(30, 144, 255)'
                    },
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'text_align': 'left'},
                    style_data_conditional=[
                        {'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(240, 240, 240)'}
                    ],
                    style_cell_conditional=[
                        {'if': {'column_id': 'Title'},
                        'width': '350px'},
                        {'if': {'column_id': 'Authors'},
                        'width': '300px'},
                        {'if': {'column_id': 'Year'},
                        'width': '100px'}],
                    style_as_list_view=True
                )
            ]),
            
            dcc.Tab(label="Tag reference", children=[
                html.Div([
                    html.H3("Tag reference"),
                ])]),
            
            dcc.Tab(label="About This App", children=[
                html.Div([
                    html.H3("What is this?"),
                    html.P("This app lets you explore and download a curated list of papers related to active inference, predictive processing, and the free energy principle."),
                    html.P("Use the dropdown to filter by tags, and download the current view using the button."),
                    html.Br(),
                    html.P(["For feature requests and bug reporting please visit the GitHub page: ", html.A("https://github.com/snamjoshi/aif-fep-db", href="https://github.com/snamjoshi/aif-fep-db", target="_blank")])
                ])])
        ])]
    )

    @app.callback(
        Output("database", "data"), 
        Output("filtered_data_store", "data"),
        Input("filter_dropdown", "value")
    )
    def display_table(tags):
        doi_list = [mapping[tag] for tag in tags]
        doi_list = list(chain.from_iterable(doi_list))
        doi_list = list(set(doi_list))
        
        filtered = database[database["DOI"].isin(doi_list)]
        filtered_dict = filtered.to_dict("records")
        return filtered_dict, filtered_dict

    @app.callback(
        Output("download-dataframe-csv", "data"),
        Input("btn_csv", "n_clicks"),
        State("filtered_data_store", "data"),
        prevent_initial_call=True,
    )
    def func(n_clicks, data):
        df = pd.DataFrame(data)
        return dcc.send_data_frame(df.to_csv, "filtered_papers.csv")
    
    return app
