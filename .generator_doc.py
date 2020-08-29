#!/usr/bin/python3 

import os 
import sys 
import json
from lib.md import MardownFile

GITHUB_USER = "PouceHeure"
GITHUB_REPO = "markdown_tags"
GITHUB_BRANCH = "master"

PATH_DIR_CURRENT = os.path.dirname(os.path.realpath(__file__))
PATH_DIR_TAGS = os.path.join(PATH_DIR_CURRENT,"tags/")

class Tag: 

    def __init__(self,path,cat,name): 
        self.path = path
        self.cat = cat 
        self.name = name 

    def create_markdown_link(self):
        return f"![tag:{self.cat}:{self.name}]({self.path})"

    def __repr__(self):
        return f"path: {self.path} cat: {self.cat} name: {self.name}"

def create_json_index_markdown(path_dir_tags,path_repo):
    tags_by_cat = {}
    for root, _, files in os.walk(path_dir_tags):
        for name in files:
            full_path = os.path.join(root,name)
            short_path = os.path.relpath(full_path, path_dir_tags)
            cat = os.path.dirname(short_path)

            path = os.path.join(path_repo,"tags",short_path)
            name = os.path.splitext(os.path.basename(short_path))[0]
            tag = Tag(path,cat,name)

            if(not cat in tags_by_cat.keys()): 
                tags_by_cat[cat] = {}
            
            tags_by_cat[cat][name] = tag
    return tags_by_cat


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