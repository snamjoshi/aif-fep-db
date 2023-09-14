import yaml

from collections.abc import Mapping

def validate_tag_file(tag_file: dict):
    """ Check that the loaded tag file is valid """
    
    # Assert that tag_file is a dict
    assert isinstance(tag_file, Mapping), "Tag file incorrect data type. Expected dict."
    
    # Assert number of keys in dict = 2
    assert len(tag_file) == 2, "Tag file must only have two elements: 'tag_list' and 'tags'."
    
    # Assert that the keys are "tag_list" and "tags"
    for tag in list(tag_file.keys()):
        assert tag in ['tag_list', 'tags'], "Incorrect keys in tag file. Expected 'tag_list' and 'tags'."
    
    # Assert that "tag_list" is a list
    assert isinstance(tag_file["tag_list"], list), "Key 'tag_list' in tag file must be a list."
    
    # Assert that "tags" is a list 
    assert isinstance(tag_file["tags"], list), "Key 'tags' in tag file must be a list."

def write_yaml(file, path):
    with open(path, "w") as outfile:
        yaml.dump(file, outfile, default_flow_style=False)
    