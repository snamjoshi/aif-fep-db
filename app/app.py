import pandas as pd

from dash import Dash

from preprocessing import get_metadata, get_tags, load_database, prepare_database
from layout import create_layout

def run_app(db_path):
    """ Top-level Dash app """
    
    database = load_database(db_path=db_path)
    metadata = get_metadata(database=database)
    mapping, tags = get_tags(database=database)
    database = prepare_database(database=database)
    defintions = pd.read_csv("data/tag_definitions.csv")

    app = Dash()
    app = create_layout(app=app, database=database, metadata=metadata, mapping=mapping, tags=tags, definitions=defintions)
    
    return app.server
