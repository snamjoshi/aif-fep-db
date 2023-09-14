import logging
import os
import pandas as pd

from src.tags import Tags

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

class Database:
    """
    Class that stores the database object and performs operations on it. Takes in each individual 
    table the user specifies and joins them into a single table. Includes basic helper methods for
    filtering, sorting, and saving.
    """
    
    def __init__(self) -> None:
        
        self.db               = None
        self.data_version     = "Thursday, Sept. 14, 2023"
        self._data_dir        = "data"
        
        # Database attributes
        self.tables           = None
        self.id               = None
        self.title            = None
        self.authors          = None
        self.citation         = None
        self.first_author     = None
        self.journal_book     = None
        self.publication_year = None
        self.create_date      = None
        self.pmcid            = None
        self.nihms_id         = None
        self.doi              = None
        
    def load(self, tables: list, add_remove_history = None):
        
        LOGGER.info("Checking tables...")
        self._check_tables(tables)
        
        # Load CSV tables as dataframes into list
        db_list = []
        
        LOGGER.info("Loading tables...")
        for table in tables:
            table_path = f"{self._data_dir}/{table}.csv"
            db_list.append(pd.read_csv(table_path))
        
        self.db = pd.concat(db_list).drop_duplicates()
        self._load_attributes()
        self.tables = tables
        
        LOGGER.info(f"Tables downloaded from PubMed on {self.data_version}.")
        
    def sort(self, fields: list, ascending: bool):
        """ Sort database columns """
        self._check_db_exists()
        return self.db.sort_values(by=fields, ascending=ascending)
        
    def drop_rows(self, ids: list):
        self._check_db_exists()
        ids = [int(p) for p in ids]
        return self.db[~self.db["id"].isin(ids)]
        
    def select(self, fields: list):
        """ Select columns from database"""
        self._check_db_exists()
        return self.db[fields]
        
    def filter_by_field(self, field: str, terms: list):
        """ Filter by field. """
        self._check_db_exists()
        return self.db[self.db[field].isin(terms)]
    
    def filter_by_tag(self, tags: list):
        """ If no tags then error. """
        # TODO
        self._check_db_exists()
        
    def add_paper_to_db(self, add_table: pd.DataFrame, id_type: str):
        # TODO
        # Check the added table to ensure all the columns are correct. 
        # Check id column based on type: currently just ArXiv.
        ...
        # id, title, authors, 
        # citation, first_author, journal_book, 
        # publication_year, create_data, pmcid,
        # nihms_id, doi
        
    # def load_tag_file(self, tags: Tags):
    #     # TODO: This method will convert the YAML tag dict to JSON and join it to the db.
    #     # Can load as many tag files as you like. 
    #     ...
        
    def save(self, path: str):
        """ Write current DB to path. """
        self._check_db_exists()
        self.db.to_csv(path)
        LOGGER.info(f"Database saved to {path}.")
        
    def refresh(self):
        # TODO
        """ Reincorporates tables from pubmed with a current db, drop duplicates.
            Also checks for drops so they are not in the table.
            """
        self._check_db_exists()
    
    def list_columns(self):
        """ Print out the list of columns in the database """
        self._check_db_exists()
        print("Current columns: \n", self.db.columns.to_list())
        
    def _check_db_exists(self):
        """ Checks to see that a database is loaded."""
        if self.db is not None:
            pass
        else:
            raise KeyError("No database is loaded. Please load the database first using 'Database.load()'.")
        
    def _check_tables(self, tables: list):
        
        # Check to see that user input tables match currently supported tables.
        current_tables = os.listdir(self._data_dir)
        current_tables = [table.split(".")[0] for table in current_tables]
        
        for table in tables:
            assert table in current_tables, f"'{table}' is not a currently supported table."
    
    def _load_attributes(self):
        """ Loads the table attributes """
        self._check_db_exists()
        
        # Change format of column names
        self.db.columns = ["id", "title", "authors", "citation", "first_author", "journal_book",
                           "publication_year", "create_date", "pmcid", "nihms_id", "doi"]
        
        # Attributes
        self.pmid             = self.db["id"]
        self.title            = self.db["title"]
        self.authors          = self.db["authors"]
        self.citation         = self.db["citation"]
        self.first_author     = self.db["first_author"]
        self.journal_book     = self.db["journal_book"]
        self.publication_year = self.db["publication_year"]
        self.create_date      = self.db["create_date"]
        self.pmcid            = self.db["pmcid"]
        self.nihms_id         = self.db["nihms_id"]
        self.doi              = self.db["doi"]
