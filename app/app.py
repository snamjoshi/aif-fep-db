import dash

from database import load_database
from layout import create_layout

def run_app():
    """ Top-level Dash app """
    
    app = dash.Dash(__name__)
    
    db = load_database()
    create_layout(app, database=db)
    
    return app.server
