import logging
import os
import pandas as pd

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

class Database:
    """
    Main database class. Takes in each individual table the user specifies and joins them into
    a single table. Includes basic helper methods for filtering, sorting, and saving.
    """
    
    def __init__(self) -> None:
        
        self.db = None
        self._data_version = "Thursday, Sept. 14, 2023"
        
        # Database attributes
        self.PMID = None
        
    def _check_tables(self, tables: list):
        
        # Check to see that user input tables match currently supported tables.
        current_tables = os.listdir("../data")
        current_tables = [table.split(".")[0] for table in current_tables]
        
        for table in tables:
            assert table in current_tables, f"'{table}' is not a currently supported table."
    
    def load(self, tables: list):
        
        LOGGER.info("Checking tables...")
        self._check_tables(tables)
        
        # Load CSV tables as dataframes into list
        db_list = []
        
        LOGGER.info("Loading tables...")
        for table in tables:
            table_path = f"../data/{table}.csv"
            db_list.append(pd.read_csv(table_path))
        
        self.db = pd.concat(db_list).drop_duplicates()
        
        LOGGER.info(f"Tables downloaded from PubMed on {self._data_version}.")

    """ These methods should only work if self.db is not None. 
        if self.db:
            ...
        else:
            raise KeyError("No database is loaded. Please load the database first.)
        """
    def load_tags(self):
        ...
        
    def add_tags(self):
        ...
        
    def add_tags_interactive(self):
        ...
        
    def sort(self, field, ascending):
        ...
        
    def drop(self):
        ...
        
    def filter(self, term, field):
        ...
        
    def save(self, path):
        ...
        
    def refresh(self):
        """ Reincorporates tables from pubmed with a current db, drop duplicates.
            Also checks for drops so they are not in the table.
            """
        ...
        
    

# Functions: load (specify tables, including ALL. Auto filter duplicates)