import dash

def run_app() -> dash.Dash.server:
    """ Top-level Dash app """
    
    app = dash.Dash(__name__)
    
    # db = load_database()
    # app = create_layouts() --> Creates a Dash layout for the table and banner
    
    return app.server