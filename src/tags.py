import logging
import yaml

# from src.db import Database
from src.utils import validate_tag_file, write_yaml

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)


class Tags:
    """
    Class that loads, and adds tags to an existing database.
    """
    
    def __init__(self) -> None:
        
        self.tags = None
        self.tag_file_path = None
        self.category = None
        self.tag_list = None
        self.tagged_papers = None
    
    def create_empty_tag_file(self, path: str):
        """ Creates an empty tag file """
        
        if not path.endswith(".yaml"):
            raise TypeError("Path to tag file must end in '.yaml'.")
        
        empty_tags_dict = {
            "category": "",
            "tag_list": [],
            "tagged_papers": []
        }
        
        write_yaml(empty_tags_dict, path)
        
        # with open(path, "w") as outfile:
        #     yaml.dump(empty_tags_dict, outfile, default_flow_style=False)
            
        LOGGER.info(f"Empty tag YAML output to {path}.")
    
    def load(self, path: str):
        """ Loads a user's tag file """
        
        if not path.endswith(".yaml"):
            raise TypeError("Path to tag file must end in '.yaml'.")

        with open(path, "r") as file:
            tags = yaml.safe_load(file)
        
        validate_tag_file(tags)
        
        LOGGER.info(f"YAML tag file successfully loaded from {path}.")
        
        self.tags = tags
        self.tag_file_path = path
        
        self._load_attributes()
        
    def associate_tag_with_id(self, tag_id, tags):
        """ Adds a new tag to a paper in the tag file """
        self._check_tag_exists()
        self.tags["tagged_papers"].append(
            {"id": tag_id,
             "tag": tags}
        )
        self.tagged_papers = self.tags["tagged_papers"]
        
        LOGGER.info(f"Added {tags} to {tag_id}.")
        
        # Update tag file
        write_yaml(self.tags, self.tag_file_path)
    
    def view_tag_list(self):
        """ Prints the current tag list """
        self._check_tag_exists()
        print("Current tags: \n", self.tags["tag_list"])
        
    def set_tag_list_category(self, category_name: str):
        self._check_tag_exists()
        self.tags["category"] = category_name
        self.category = self.tags["category"]
        
        LOGGER.info(f"Set {self.category} as the tag category.")
        
    def add_to_tag_list(self, new_tags: list):
        """ Appends new tags to the list of possible tags."""
        self._check_tag_exists()
        
        # Check if tag is already in the tag list and skip if so. If not, add to tag list.
        for new_tag in new_tags:
            if new_tag in self.tags["tag_list"]:
                LOGGER.info(f"{new_tag} is already in tag list. Skipping.")
            else:
                self.tags["tag_list"].append(new_tag)
                self.tags_list = self.tags["tag_list"]
                
        LOGGER.info(f"Added {new_tags} to the tag list.")
                
        # Update tag file
        write_yaml(self.tags, self.tag_file_path)
        
    def add_tags_interactive(self):
        """ Interactive tag adding mode
        Features:
        - Show the title, author, and year.
        - Pull abstract with "show abstract"
        - Show "field" to see other fields
        - Only includes non-tagged papers
        - Move forward a paper
        - Move backward a paper
        - Prints current tags at the bottom of the output with numbers associated so it's easy to 
          say which tag to add
        - Saves new tags in the tag list mid-stream
        - Add a new tag on the fly. Terminal will refresh to show the new tag added.
        - Stop interactive mode
        - Progress bar / % left to add or counts out of total
        - Notification of which tags were added
        - Average time with tic toc to finish. Give estimate of remaning items
        - New field in YAML tag for "category" to separate different tag files
        
        """
        # May be the only function that requires the db. Remove db from init. 
        # TODO
        self._check_tag_exists()
        
    def _check_tag_exists(self):
        """ Checks to see that a database is loaded."""
        if self.tags is not None:
            pass
        else:
            raise KeyError("No tag YAML file is loaded. Please load the tag file first using 'Tags.load()'.")
        
    def _load_attributes(self):
        """ Loads the table attributes """
        self._check_tag_exists()
        
        # Attributes
        self.category      = self.tags["category"]
        self.tag_list      = self.tags["tag_list"]
        self.tagged_papers = self.tags["tagged_papers"]

# if self.db is None:
#     raise KeyError("No database is loaded. Please load the database first using 'Database.load()'.") 