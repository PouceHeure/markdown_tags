#!/usr/bin/python3 

import os 
import sys 
import json

PATH_DIR_CURRENT = os.path.dirname(os.path.realpath(__file__))
PATH_DIR_TAGS = os.path.join(PATH_DIR_CURRENT,"../tags/")
PATH_FILE_LINK = os.path.join(PATH_DIR_CURRENT,"../links.json")

class Tag: 

    def __init__(self,path,cat,name): 
        self.path = path
        self.cat = cat 
        self.name = name 

    def create_markdown_link(self):
        return f"![tags:{self.cat}:{self.name}]({self.path})"

    def __repr__(self):
        return f"path: {self.path} cat: {self.cat} name: {self.name}"

def create_json_index_markdown(path_dir_tags,path_real_readme):
    tags_by_cat = {}
    for root, _, files in os.walk(path_dir_tags):
        for name in files:
            full_path = os.path.join(root,name)
            short_path = os.path.relpath(full_path, path_dir_tags)
            cat = os.path.dirname(short_path)

            path = os.path.join(path_real_readme,full_path)
            path = os.path.relpath(path)
            name = os.path.splitext(os.path.basename(short_path))[0]
            tag = Tag(path,cat,name).create_markdown_link()

            if(not cat in tags_by_cat.keys()): 
                tags_by_cat[cat] = {}
            
            tags_by_cat[cat][name] = tag
    return tags_by_cat