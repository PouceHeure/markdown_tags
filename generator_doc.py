#!/usr/bin/python3 

import os 
import sys 
from lib.tag import * 
from lib.md import MardownFile


if __name__ == "__main__":
    path_dir_current = os.path.dirname(os.path.realpath(__file__))
    tags_by_cat = create_json_index_markdown(PATH_DIR_TAGS,path_dir_current)
    
    md_file = MardownFile()
    for cat, cat_dict in tags_by_cat.items(): 
        md_file.add_section(cat) 
        for img_name, img_path in cat_dict.items(): 
            md_file.add_subsection(img_name)
            md_file.add_element(img_path)
    
    md_file.write("tags.md")