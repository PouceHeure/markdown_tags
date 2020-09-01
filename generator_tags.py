#! /usr/bin/python3

import json
import argparse
import os 
from lib.md import MardownFile
from PIL import Image,ImageDraw,ImageFont, ImageOps

GITHUB_USER = "PouceHeure"
GITHUB_REPO = "markdown_tags"
GITHUB_BRANCH_OR_TAG = "master"

## DON'T CHANGE THESE SETTINGS 

PATH_DIR_CURRENT = os.path.dirname(os.path.realpath(__file__))
PATH_DIR_TAGS = os.path.join(PATH_DIR_CURRENT,"tags/")
PATH_FILE_FONT = os.path.join(PATH_DIR_CURRENT,"font/RussoOne-Regular.ttf")
PATH_FILE_CONFIG_TAGS = os.path.join(PATH_DIR_CURRENT,"tags.json")

FONT_SIZE = 15
PADDING_SIZE = 10
BORDER_SIZE = 2

CONFLICT_CHARS = {
    "#":"sharp",
    "\\":"_",
    " ":"_",
    ":":"_",
    ".":"_"
}

COLORS = {
    "white": {
        "bg": "#FFFFFF",
        "font": "#000000"
    }, 
    "red": {
        "bg": "#d50000",
        "font": "#FFFFFF"
    },
    "green": {
        "bg": "#00c853",
        "font": "#FFFFFF"
    } ,
    "blue": {
        "bg": "#2979ff",
        "font": "#FFFFFF",
    }  
}

def load_config_tags(path_file=PATH_FILE_CONFIG_TAGS):
    data = None
    with open(path_file) as f:
        data = json.load(f)
    return data 

def generate_image(content,font, font_color=(0,0,0), bg_color=(255,255,255),padding=PADDING_SIZE):
    size_img = list(font.getsize(content))
    size_img[0] += 2*padding
    size_img[1] = int(FONT_SIZE*1.10) + 2*padding
    img = Image.new('RGB', size_img, color = bg_color)
    img = ImageOps.expand(img,border=BORDER_SIZE,fill='black')
    d = ImageDraw.Draw(img)
    d.text((padding,padding), content,fill = font_color,font=font)
    return img 

def fix_conflict_name(content,conflict_dict=CONFLICT_CHARS): 
    for c_conflict, c_resolve in conflict_dict.items(): 
        content = content.replace(c_conflict,c_resolve)
    return content

def create_path_base_link(user,repo,branch): 
    return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", type=str, default=GITHUB_BRANCH_OR_TAG, help="github tag version")
    args = parser.parse_args()
    github_branch = args.version

    path_url_base = create_path_base_link(GITHUB_USER,GITHUB_REPO,github_branch)
    font = ImageFont.truetype(PATH_FILE_FONT,FONT_SIZE)

    md_file = MardownFile()
    md_file.add_title("markdown_tags")
    md_file.add_element(f"version: {github_branch}")
    md_file.add_new_line()
    md_file.add_element(f"add tag: pull-request **tags.json**")

    headers = ["img","markdown command"]

    config_tags = load_config_tags()
    for cat, cat_tags in config_tags.items():
        path_cat = os.path.join(PATH_DIR_TAGS,cat)
        if not os.path.exists(path_cat):
            os.makedirs(path_cat)
        md_file.add_section(cat) 
        for tag in cat_tags: 
            tag_name_no_conflit = fix_conflict_name(tag)
            file_path_tag = os.path.join(path_cat,tag_name_no_conflit)
            if not os.path.exists(file_path_tag):
                os.makedirs(file_path_tag)
            md_file.add_subsection(tag)
            md_file.add_array_header(headers)
            for color in COLORS.keys():
                font_color = COLORS[color]["font"]    
                bg_color = COLORS[color]["bg"]

                # generate img 
                img = generate_image(tag,font=font,font_color=font_color,bg_color=bg_color)
                file_name = f"{tag_name_no_conflit}_{color}.png"
                file_path = os.path.join(file_path_tag,file_name)
                img.save(file_path)

                # generate doc information 
                # extract relative path 
                file_path_rel = os.path.relpath(file_path,PATH_DIR_CURRENT) 
                # add relative path to url 
                file_url = os.path.join(path_url_base,file_path_rel) 
                # write tag information inside markdown 
                desc = f"tag:{cat}:{tag}"
                url_image = md_file.format_img(desc,file_path_rel)
                url_quote_img = md_file.format_quote(md_file.format_img(desc,file_url))
                md_file.add_array_row(url_image,url_quote_img)
               

    md_file.write(os.path.join(PATH_DIR_CURRENT,"readme.md"))



