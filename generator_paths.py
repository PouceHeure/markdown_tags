import os 
import sys 
from lib.tag import *  

def write_json_index_markdown(path_file,data):
    with open(path_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":

    path_from_tags_to_readme = os.path.dirname(os.path.relpath(sys.argv[0]))
    tags_by_cat = create_json_index_markdown(PATH_DIR_TAGS,path_from_tags_to_readme)
    write_json_index_markdown(PATH_FILE_LINK,tags_by_cat)
   

            
