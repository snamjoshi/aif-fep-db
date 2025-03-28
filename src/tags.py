import logging
import yaml

# from src.db import Database
from src.interactive import InteractiveTagging
from src.utils import validate_tag_file, write_yaml

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)


class Tags:
    """
    Class that loads from an existing tag file or creates a new tag file.
    """
    
    def __init__(self) -> None:
        
        self.tags          = None
        self.tag_file_path = None
        self.category      = None
        self.tag_list      = None
    
    def create(self):
        """ Creates an empty tag file """
        
        empty_tags_dict = {
            "category": "",
            "tag_list": [],
            "tagged_papers": []
        }
        
        self.tags = empty_tags_dict
        LOGGER.info("New tag file created.")
    
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
        
    def detach(self):
        """ Detatches a loaded tag file. """
        
        self.tags          = None
        self.tag_file_path = None
        self.category      = None
        self.tag_list      = None
        
        LOGGER.info("Tag file detached.")
        
    def link_tags_to_doi(self, tag_dict_list: list, verbose: bool=True):
        """ Associates tags in the tag list with a DOI """
        
        self._check_tag_exists()
        currently_tagged = [entry["doi"] for entry in self.tags["tagged_papers"]]
        
        # Loop over each tag dict
        for entry in tag_dict_list:
            doi = entry["doi"]
            
            # If DOI does not existed in tagged papers already, add a new entry
            if doi not in currently_tagged:
                self.tags["tagged_papers"].append(
                        {"doi": entry["doi"],
                         "tags": entry["tags"]}
                        )
                
                if verbose:
                    LOGGER.info(f"Added tags {entry['tags']} to DOI {entry['doi']}")
            
            # If DOI does exist already, append tag to existing entry
            else:
                
                # Loop over tagged papers
                for tagged in self.tags["tagged_papers"]:
                    
                    # Select matching DOI
                    if tagged["doi"] == doi:
                        
                        # Add tags to tag list if not already present
                        LOGGER.info("Checking if any requested tags are not in the tag list...")
                        self.add_to_tag_list(entry["tags"])
                        
                        # Append (unique) new tags to matching DOI
                        new_tag_list = list(set(tagged["tags"] + entry["tags"]))
                        tagged["tags"] = new_tag_list
                    
                        if verbose:
                            LOGGER.info(f"Added tags {entry['tags']} to DOI {entry['doi']}")
        
    def remove_entries(self, doi_list: list):
        """ Removes one or more entries from the tagged papers list """
        raise NotImplementedError
                     
    def save(self, outpath: str):
        """ Saves/exports the tag file. """
        
        self._check_tag_exists()
        write_yaml(self.tags, outpath)
        
        LOGGER.info(f"Empty tag YAML output to {outpath}.")
    
    def view_tag_list(self):
        """ Prints the current tag list for a loaded tag file """
        
        self._check_tag_exists()
        LOGGER.info("Current tags: \n", self.tags["tag_list"])
        
    def set_tag_list_category(self, category_name: str):
        """ Allows the user to set a tag category """
        
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
        
    def _check_tag_exists(self):
        """ Checks to see that a tag file is loaded."""
        
        if self.tags is not None:
            pass
        else:
            raise KeyError("No tag YAML file is loaded. Please load the tag file first using 'Tags.load()'.")
        
    def _load_attributes(self):
        """ Loads the table attributes """
        self._check_tag_exists()
        
        # Attributes
        self.category = self.tags["category"]
        self.tag_list = self.tags["tag_list"]
