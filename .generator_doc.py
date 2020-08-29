#!/usr/bin/python3 

import os 
import sys 
from lib.tag import * 
from lib.md import MardownFile

GITHUB_USER = "PouceHeure"
GITHUB_REPO = "markdown_tags"
GITHUB_BRANCH = "master"

def create_path_base_link(user,repo,branch): 
    return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/"

if __name__ == "__main__":
    path_url_base = create_path_base_link(GITHUB_USER,GITHUB_REPO,GITHUB_BRANCH)
    path_dir_current = os.path.dirname(os.path.realpath(__file__))
    tags_by_cat = create_json_index_markdown(PATH_DIR_TAGS,path_url_base)
    
    md_file = MardownFile()

    md_file.add_title("markdown_tags")

    for cat, cat_dict in tags_by_cat.items(): 
        md_file.add_section(cat) 
        for img_name, tag in cat_dict.items(): 
            md_file.add_subsection(img_name)
            md_file.add_element(tag.create_markdown_link())
            md_file.add_element("")
            md_file.add_element_quote(tag.create_markdown_link())
    
    md_file.write("readme.md")