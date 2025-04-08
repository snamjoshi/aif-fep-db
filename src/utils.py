import logging
import os
import pandas as pd
import re
import yaml

from collections.abc import Mapping
from typing import List, Union

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

DOI_REGEX_PATTERN = r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$"


def validate_tag_file(tag_file: dict) -> None:
    """ Checks that the loaded tag file is valid """
    
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

def write_yaml(file: dict, path: str) -> None:
    """ Write dict to YAML file at specified path """
    
    with open(path, "w") as outfile:
        yaml.dump(file, outfile, default_flow_style=False)

def load_tables(table_dir: str) -> list:
    """ Loads CSVs in a directory """
    
    table_list = []
    table_names = os.listdir(table_dir)
    table_paths = [table_dir + "/" + table_name for table_name in table_names]

    for table_path in table_paths:
        table = pd.read_csv(table_path)
        table_list.append(table)
        
    return table_list

def process_doi(doi: str) -> str:
    """ Strips URL from DOI and checks if the DOI is valid """
    doi = doi.strip("https://doi.org/")
    
    # Note that this pattern will probably not catch everything but it's fairly comprehensive
    match = re.match(DOI_REGEX_PATTERN, doi, re.IGNORECASE)

    if not bool(match):
        LOGGER.warning(f"Warning: {doi} failed DOI validation!")
        
    return doi

def split_camel_case(name: str) -> str:
    """ Removes space in camel case, e.g. CamelCase -> Camel Case"""
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', name)

def flatten_keywords(keywords: List[Union[str, List[str]]]) -> List[str]:
    """ 
    Keywords for the scraper can be a list of strings, a list of lists of strings, or a combination
    of both. For all three cases, this function returns a flat list of strings.
    """
    
    flattened = []
    for item in keywords:
        if isinstance(item, str):
            flattened.append(item)
        elif isinstance(item, list):
            flattened.extend(flatten_keywords(item))
        else:
            raise ValueError(f"Unsupported type in list: {type(item)}")
    return flattened
