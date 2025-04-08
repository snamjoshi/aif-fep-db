import pandas as pd

from src.db import Database


def load_database(db_path: str) -> pd.DataFrame:
    """ Loads a serialized database from specified path to pickle file """
    database = Database()
    database.load(db_path)
    
    return database

def get_metadata(database: pd.DataFrame) -> dict:
    """ Extracts metadata from database """
    metadata = {
        "creation_time": database.creation_time,
        "tag_version"  : database.tag_version
    }
    
    return metadata

def get_tags(database: pd.DataFrame) -> list:
    """ Extracts unique tags from database """
    database.db["tag"] = database.db["tag"].apply(lambda lst: [s.lower() for s in lst])
    db_exploded = database.db.explode("tag")
    mapping = db_exploded.groupby("tag")["doi"].apply(list).to_dict()
    tags = list(mapping.keys())
    
    return mapping, tags

def prepare_database(database: pd.DataFrame) -> pd.DataFrame:
    """ Drop tag column for database and rename remaining columns """
    database = database.db.drop('tag', axis=1)
    database.columns = ["Title", "Authors", "Journal", "Year", "DOI"]
    
    return database