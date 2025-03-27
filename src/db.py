import logging
import os
import pandas as pd
import pickle

from ast import literal_eval
from datetime import datetime

from src.tags import Tags
from src.utils import process_doi

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)


class Database:
    """ Class that stores the database object and performs operations on it. 
    
    The Database class is intended for use in opening up an existing serialized (pickled) database,
    modifiying it, and then reserializing it. The class may also be used to create a new database.
    """
    
    def __init__(self) -> None:
        self.db            = None   # Database object    [pd.DataFrame]
        self.creation_time = None   # Database timestamp [datetime.datetime]
        self.description   = None   # Database description [str]
        self.tag_version   = None   # Database tag version [str]
        
        self.required_attributes = {"doi", "title", "authors", "year", "where_published"}
    
    def load(self, database_path: str):
        """ Loads and unpacks a pickled database file into a database object. """
        # TODO: Make sure to pull in and set self.creation_time from metadata.
        
        if self.db is not None:
            raise KeyError("A database object is already stored. Use Database.detach() to detach the current database before loading.")
        
        with open(database_path, 'rb') as file:
            database = pickle.load(file)
            metadata = pickle.load(file)
            
        self.creation_time = metadata["creation_time"]
        self.description = metadata["description"]
        self.db = database
        
        LOGGER.info(f"Database loeaded from {database_path}.")
        
        # TODO: Add tag version 
        
    def detach(self):
        """ Detatches a loaded database. """
        self.db            = None
        self.creation_time = None
        self.description   = None
        self.tag_version   = None
        
        LOGGER.info("Database detached.")

    def create(self, table_dir: str):
        """ Creates a new database object from existing CSV data sources. """
        
        assert os.path.isdir(table_dir), "The specified table directory does not exist."
        
        # Load CSV tables as dataframes into list
        db_list = []
        table_names = os.listdir(table_dir)
        table_paths = [table_dir + "/" + table_name for table_name in table_names]
        
        LOGGER.info("Loading tables...")
        for table_path in table_paths:
            table = pd.read_csv(table_path, index_col=0)
            
            assert set(table.columns) == self.required_attributes, f"Table columns must include {self.required_attributes}."
            
            db_list.append(table)
            
        self.db = pd.concat(db_list).drop_duplicates()
        self.creation_time = datetime.now()
        
        LOGGER.info(f"Database created at {str(self.creation_time)}.")
    
    def update_from_dicts_list(self, entries: list):
        """ Adds new paper(s) to the database from a dict or collection of dicts. """
        
        for idx, entry in enumerate(entries):
            
            # Check if all entries are present
            missing_fields = self.required_attributes.difference(set(entry.keys()))
            assert len(missing_fields) == 0, f"Entry {idx} missing attribute {missing_fields}."  
            
            # Process DOI
            entry["doi"] = process_doi(doi = entry["doi"])
            
            # If tags are already attached, make entry untagged
            if "tag" in self.db.columns:
                entry["tag"] = ["untagged"]
        
        # Add entry dicts to database
        new_entries_dataframe = pd.DataFrame(entries)
        self.db = pd.concat([self.db, new_entries_dataframe], ignore_index=True)
        
    def update_from_CSV(self, csv_path: str):
        """ Updates an existing loaded database with new papers from a CSV file. """
        entries = pd.read_csv(csv_path, converters={"authors": literal_eval, "tag": literal_eval})
        entries = entries.to_dict(orient="records")
        
        self.update_from_dicts_list(entries=entries)
        
    def remove(self, doi_list: list):
        """ Removes paper(s) from the database based on DOI """
        
        self.db = self.db[~self.db["doi"].isin(doi_list)].reset_index(drop=True)
    
    def save(self, database_description: str="No description", outpath: str=None):
        """ Saves/exports the database via serialization to a pickle file with metadata. 
            Note that any loaded tags are serialized as a separate object.
        """
        # TODO: If no tag file is presented, then create an empty one where everything is unttaged
        # and notify the user.
        # TODO: Add the tag file hash to the metadata upon saving
        
        self._check_db_exists()
        
        if not outpath:
            database_path = "data/databases/database__" + str(self.creation_time).replace(" ", "__") + ".pkl"
        else:
            database_path = outpath
            
        metadata = {
            'description': database_description,
            'creation_time': str(self.creation_time),
        }
        
        with open(database_path, 'wb') as file:
            pickle.dump(self.db, file)
            pickle.dump(metadata, file)
            
        LOGGER.info(f"Database saved to {database_path}.")
        
    def attach_tags(self, tag_path: str, overwrite: bool=False):
        """ Adds tags to the database object. """
        
        assert os.path.isfile(tag_path), "The specified tag file does not exist."
        # TODO: Test this.
        # assert "tag" in self.db.columns, "Database is already tagged. To overwrite with a new set of tags use Database.attach_tags(overwrite=True)."
        
        if overwrite:
            # TODO: Overwrite attached tag file
            ...
        
        LOGGER.info("Loading tags...")
        tags = Tags()
        tags.load(tag_path)
        tags = pd.DataFrame(tags.tags["tagged_papers"])
        
        LOGGER.info("Adding tags to database...")
        self.db = self.db.merge(tags, on="doi")
        
        # TODO: Capture the id (hash) of the tag file that was added.
        # TODO: Fill in hash to database attribute self.tag_version
        
    def _check_db_exists(self):
        """ Checks that a database is loaded. """
        
        if self.db is None:
            raise KeyError("No database is loaded. Load the database first using 'Database.load()' or create a new database with 'Database.create()'")
   