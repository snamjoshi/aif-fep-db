import logging
import yaml

# from src.db import Database
from src.interactive import InteractiveTagging
from src.utils import validate_tag_file, write_yaml

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)


# TODO: IF no DOI, create a DOI using a hash of the paper information that is available.

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
        
    def associate_tag_with_id(self, tag_id: int, tags: list, db):
        """ Adds a new tag to a paper in the tag file """
        self._check_tag_exists()
        
        tag_id = int(tag_id)
        
        # TODO: Refactor this mess
        # Check to see that tag_id exists in the database
        if tag_id in db.db["id"].tolist():
            
            # Check to see if tag is already in the tagged papers
            if tag_id in [tags["id"] for tags in self.tags["tagged_papers"]]:
                
                # Append each new tag to the current tags
                for tag in tags:
                    
                    # Pull each dict out of the tagged papers list
                    for tag_set in self.tags["tagged_papers"]:
                        
                        # Only append to the tag id specified
                        if tag_set["id"] == tag_id:
                            tag_set["tag"].append(tag)
                            self.tagged_papers = self.tags["tagged_papers"]
                LOGGER.info(f"Added {tags} to {tag_id}.")
            
            # If id is not in tagged papers yet, add it and the tags
            else:
                self.tags["tagged_papers"].append(
                {"id": tag_id,
                "tag": tags}
                )
                self.tagged_papers = self.tags["tagged_papers"]
            
                LOGGER.info(f"Added {tags} to {tag_id}.")
        else:
            raise KeyError(f"The tag_id {tag_id} does not correspond to an id in the database.")
        
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
        
    def add_tags_interactive(self, db, tags):
        """ Interactive tag adding mode        
        """
        # TODO Allow multiple loaded tags (categories) to tbe passed in as a list
        self._check_tag_exists()
        interactive = InteractiveTagging(db, self.tags)
        interactive.run()
        
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