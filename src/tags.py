import logging
import yaml

from db import Database
from utils import validate_tag_file, write_yaml

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)


"""
# Possibility for tag groups? One can specify the tag group when creating a tag
# This tag group allows you to group different types of tags with similar values together
# A tag file always has a tag list that one can choose from when adding tags
# If tag is not there, it must be added to the tag list first.
# Start backward from a tag file: What the structure is and load it.
# Work backward to figure out what an empty version looks like
# Can add any number of tag files
"""
class Tags:
    """
    Class that loads, and adds tags to an existing database.
    """
    
    def __init__(self) -> None:
        self.tags = None
        self.tag_file_path = None
        
        if self.db is None:
            raise KeyError("No database is loaded. Please load the database first using 'Database.load()'.")
    
    def create_empty_tag_file(self, path: str):
        """ Creates an empty tag file """
        
        empty_tags_dict = {
            "tag_list": [],
            "tags": []
        }
        
        write_yaml(empty_tags_dict, path)
        
        # with open(path, "w") as outfile:
        #     yaml.dump(empty_tags_dict, outfile, default_flow_style=False)
            
        LOGGER.info(f"Empty tag YAML output to {path}.")
    
    def load(self, path: str):
        """ Loads a user's tag file """

        with open(path, "r") as file:
            tags = yaml.safe_load(file)
        
        validate_tag_file(tags)
        
        self.tags = tags
        self.tag_file_path = path
        
    def add_tags_to_paper(self, db):
        # May be the only function that requires the db. Remove db from init. 
        # TODO
        """ Add tag to database """
        ...
    
    def check_tag_list(self):
        """ Prints the current tag list """
        print("Current tags: \n", self.tags["tag_list"])
        
    def add_to_tag_list(self, new_tags: list):
        # TODO
        """ Appends new tags to the list of possible tags."""
        self._check_tag_exists()
        
        # Check if tag is already in the tag list and skip if so. If not, add to tag list.
        for new_tag in new_tags:
            if new_tag in self.tags["tag_list"]:
                LOGGER.info(f"{new_tag} is already in tag list. Skipping.")
            else:
                self.tags["tag_list"].append(new_tag)
                
        # Update tag file
        write_yaml(self.tags, self.tag_file_path)
        
    def add_tags_interactive(self):
        """ Interactive tag adding mode"""
        # May be the only function that requires the db. Remove db from init. 
        # TODO
        self._check_tag_exists()
        
    def _check_tag_exists(self):
        """ Checks to see that a database is loaded."""
        if self.tag is not None:
            pass
        else:
            raise KeyError("No tag YAML file is loaded. Please load the tag file first using 'Tags.load()'.")
        