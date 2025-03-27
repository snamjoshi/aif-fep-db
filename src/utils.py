import logging
import os
import pandas as pd
import re
import yaml

from collections.abc import Mapping

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)


DOI_REGEX_PATTERN = r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$"


def validate_tag_file(tag_file: dict):
    # TODO: Replace this with pydantic validation
    """ Check that the loaded tag file is valid """
    
    # Assert that tag_file is a dict
    assert isinstance(tag_file, Mapping), "Tag file incorrect data type. Expected dict."
    
    # Assert number of keys in dict = 2
    assert len(tag_file) == 3, "Tag file must only have three elements: 'category', 'tag_list' and 'tagged_papers'."
    
    # Assert that the keys are "category", "tag_list" and "tags"
    for tag in list(tag_file.keys()):
        assert tag in ["category", "tag_list", "tagged_papers"], "Incorrect keys in tag file. Expected 'category', 'tag_list' and 'tagged_papers'."
    
    # Assert that "category" is a string
    assert isinstance(tag_file["category"], str), "Key 'category' in tag file must be a string."
    
    # Assert that "tag_list" is a list
    assert isinstance(tag_file["tag_list"], list), "Key 'tag_list' in tag file must be a list."
    
    # Assert that "tags" is a list 
    assert isinstance(tag_file["tagged_papers"], list), "Key 'tagged_papers' in tag file must be a list."

def write_yaml(file, path):
    with open(path, "w") as outfile:
        yaml.dump(file, outfile, default_flow_style=False)
        
def progress_bar(prog):
    """ Creates a visual progress bar for the terminal """
    prog = prog - 1
    remainder = 100 - prog
    
    prog = ''.join(["="] * prog)
    remainder = ''.join(["-"] * remainder)
    
    return(f"[{prog}>{remainder}]")

def load_tables(table_dir: str):
    
    table_list = []
    table_names = os.listdir(table_dir)
    table_paths = [table_dir + "/" + table_name for table_name in table_names]

    for table_path in table_paths:
        table = pd.read_csv(table_path)
        table_list.append(table)
        
    return table_list

def process_doi(doi: str):
    doi = doi.strip("https://doi.org/")
    
    match = re.match(DOI_REGEX_PATTERN, doi, re.IGNORECASE)

    if not bool(match):
        LOGGER.warning(f"Warning: {doi} failed DOI validation!")
        
    return doi