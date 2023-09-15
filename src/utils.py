import yaml

from collections.abc import Mapping

def validate_tag_file(tag_file: dict):
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
    