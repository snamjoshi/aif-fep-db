from db import Database


class Tags:
    """
    Class that loads, and adds tags to an existing database.
    """
    
    def __init__(self, db: Database) -> None:
        pass
    
    def create_tag_file(self, path):
        """ Creates a new tag file """
        # Possibility for tag groups? One can specify the tag group when creating a tag
        # This tag group allows you to group different types of tags with similar values together
        # A tag file always has a tag list that one can choose from when adding tags
        # If tag is not there, it must be added to the tag list first.
        # Start backward from a tag file: What the structure is and load it.
        # Work backward to figure out what an empty version looks like
        empty_tags = {}
    
    def load_tags(self):
        """ A tag file should consist of a PMID and a set of tags"""
        self._check_db_exists()
        
    def add_new_list(self):
        # TODO
        self._check_db_exists()
        # Check list of available tags
        # Functionality for adding new tags to set of possible tags
        # Adding a tag will write to the tag file. 
        
    def add_tags_interactive(self):
        """ Interactive tag adding mode"""
        # TODO
        self._check_db_exists()