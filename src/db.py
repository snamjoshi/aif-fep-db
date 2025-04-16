import jsonpickle
import logging
import os
import pandas as pd
import pickle
import sys

from ast import literal_eval
from datetime import datetime

from src.tags import Tags
from src.utils import process_doi

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)


class Database:
    """ Class that stores the database object and performs operations on it. 
    
    The Database class is intended for use in opening up an existing serialized (pickled) database, modifiying it, and then reserializing it. The class may also be used to create a new database.
    """
    
    def __init__(self) -> None:
        self.db            = None   # Database object      [pd.DataFrame]
        self.creation_time = None   # Database timestamp   [datetime.datetime]
        self.description   = None   # Database description [str]
        self.tag_version   = None   # Database tag version [int]
        
        self.required_attributes = {"doi", "title", "authors", "year", "where_published"}
    
    def load(self, database_path: str) -> None:
        """ Loads and unpacks a pickled database file into a database object. """
        
        if self.db is not None:
            raise KeyError("A database object is already stored. Use Database.detach() to detach the current database before loading.")
        
        with open(database_path, 'rb') as file:
            database = pickle.load(file)
            metadata = pickle.load(file)
            
        self.creation_time = metadata["creation_time"]
        self.description = metadata["description"]
        
        if "tag_file_id" in metadata:
            self.tag_version = metadata["tag_file_id"]
        self.db = database
        
        LOGGER.info(f"Database loaded from {database_path}.")  
        
    def detach(self) -> None:
        """ Detatches a loaded database or any associated tags. """
        self.db            = None
        self.creation_time = None
        self.description   = None
        self.tag_version   = None
        
        LOGGER.info("Database detached.")

    def create(self, table_dir: str) -> None:
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
    
    def update_from_dicts_list(self, entries: list) -> None:
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
        
        LOGGER.info("Successfully added new papers to database.")
        
    def update_from_CSV(self, csv_path: str) -> None:
        """ Updates an existing loaded database with new papers from a CSV file. """
        
        entries = pd.read_csv(csv_path, converters={"authors": literal_eval, "tag": literal_eval})
        entries = entries.to_dict(orient="records")
        
        self.update_from_dicts_list(entries=entries)
        
    def remove(self, doi_list: list) -> None:
        """ Removes paper(s) from the database based on DOI """
        
        self.db = self.db[~self.db["doi"].isin(doi_list)].reset_index(drop=True)
        
        LOGGER.info("Specified papers have been dropped from the database.")
        
    def save(self, database_description: str="No description", outpath: str=None) -> None:
        """ Saves/exports the database via serialization to a pickle file with metadata. 
            Note that any loaded tags are serialized as a separate object.
        """
        
        self._check_db_exists()
        
        # If no outpath is specified create one based on the date and time
        if not outpath:
            database_path = "data/databases/database__" + str(self.creation_time).replace(" ", "__") + ".pkl"
        else:
            database_path = outpath
            
        # If there are no tags in the database, create an empty tag column
        if "tag" not in self.db.columns: 
            LOGGER.warning("No tags have been attached to this database. Appending database with an empty tag file.")
            self.db["tag"] = ["untagged"] * len(self.db)
            self.db["tag"] = self.db["tag"].apply(lambda x: [x])
            self.tag_version = -1
        
        # Prepare database metadata    
        metadata = {
            'description'  : database_description,
            'creation_time': str(self.creation_time),
            'tag_file_id'  : self.tag_version
        }
        
        with open(database_path, 'wb') as file:
            pickle.dump(self.db, file)
            pickle.dump(metadata, file)
            
        LOGGER.info(f"Database saved to {database_path}.")
        
    def attach_tags(self, tag_path: str, overwrite: bool=False) -> None:
        """ Adds tags to the database object. """
        
        assert os.path.isfile(tag_path), "The specified tag file does not exist."
        
        if "tag" in self.db.columns:
            if overwrite:
                LOGGER.info("Overwriting existing tags...")
                del self.db["tag"]
                self._append_tags_to_database(tag_path=tag_path)
            else:
                raise Exception("Database is already tagged. To overwrite with a new set of tags use Database.attach_tags(overwrite=True).")
        else:
            self._append_tags_to_database(tag_path=tag_path)
        
    def _check_db_exists(self) -> None:
        """ Checks that a database is loaded. """
        
        if self.db is None:
            raise KeyError("No database is loaded. Load the database first using 'Database.load()' or create a new database with 'Database.create()'")
        
    def _append_tags_to_database(self, tag_path: str) -> None:
        """ 
        Loads tag file, takes a hash of the file to set to the tag version, and adds the tag file to the database.
        
        """
        
        LOGGER.info("Loading tags...")
        tags = Tags()
        tags.load(tag_path)
        self.tag_version = self._hash_tag_dict(tag_dict=tags.tags)
        tags = pd.DataFrame(tags.tags["tagged_papers"])
        
        LOGGER.info("Adding tags to database...")
        self.db = self.db.merge(tags, how="outer", on="doi")
        
        # DOIs without a corresponding tag are labeled ["untagged"]
        n_untagged = self.db['tag'].isna().sum()
        
        LOGGER.info(f"{n_untagged} papers are currently untagged.")
        
        self.db.loc[self.db['tag'].isna(), 'tag'] = ["untagged"] * n_untagged
        self.db['tag'] = self.db['tag'].apply(lambda x: ["untagged"] if x == "untagged" else x)
        self.db['tag'] = self.db['tag'].apply(lambda x: x)
        
        self.db = self.db.dropna(axis=0, how="any")
        
    def _hash_tag_dict(self, tag_dict: dict) -> int:
        """ Hashes the string representation of the tag dictionary to serve as a version ID """
        
        h = hash(jsonpickle.encode(tag_dict))
        
        # Ensure that hash is positive
        if h < 0:
            h += sys.maxsize + 1
            
        return h
