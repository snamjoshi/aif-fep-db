from db import Database


class Tags:
    """
    Class that loads, and adds tags to an existing database.
    """
    
    def __init__(self, db: Database) -> None:
        pass
    
    def create_tag_file(self, path):
    
    def load_tags(self):
        """ A tag file should consist of a PMID and a set of tags"""
        self._check_db_exists()
        
    def add_tags(self):
        # TODO
        self._check_db_exists()
        # Check list of available tags
        # Functionality for adding new tags to set of possible tags
        # Adding a tag will write to the tag file. 
        
    def add_tags_interactive(self):
        # TODO
        self._check_db_exists()