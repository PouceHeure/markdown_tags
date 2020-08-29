import json
import os 
from lib.md import MardownFile
from PIL import Image,ImageDraw,ImageFont, ImageOps

GITHUB_USER = "PouceHeure"
GITHUB_REPO = "markdown_tags"
GITHUB_BRANCH = "master"

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

def load_config_tags(path_file=PATH_FILE_CONFIG_TAGS):
    data = None
    with open(path_file) as f:
        data = json.load(f)
    return data 

def generate_image(content,font, color=(255,255,255),padding=PADDING_SIZE):
    size_img = list(font.getsize(content))
    size_img[0] += 2*padding
    size_img[1] = int(FONT_SIZE*1.10) + 2*padding
    img = Image.new('RGB', size_img, color = color)
    img = ImageOps.expand(img,border=BORDER_SIZE,fill='black')
    d = ImageDraw.Draw(img)
    d.text((padding,padding), content,fill = (0,0,0),font=font)
    return img 

def fix_conflict_name(content,conflict_dict=CONFLICT_CHARS): 
    for c_conflict, c_resolve in conflict_dict.items(): 
        content = content.replace(c_conflict,c_resolve)
    return content

def create_path_base_link(user,repo,branch): 
    return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/"


if __name__ == "__main__":
    path_url_base = create_path_base_link(GITHUB_USER,GITHUB_REPO,GITHUB_BRANCH)
    font = ImageFont.truetype(PATH_FILE_FONT,FONT_SIZE)

    md_file = MardownFile()
    md_file.add_title("markdown_tags")

    config_tags = load_config_tags()
    for cat, cat_tags in config_tags.items():
        path_cat = os.path.join(PATH_DIR_TAGS,cat)
        if not os.path.exists(path_cat):
            os.makedirs(path_cat)
        md_file.add_section(cat) 
        for tag in cat_tags: 
            # generate img 
            img = generate_image(tag,font=font)
            file_name = f"{fix_conflict_name(tag)}.png"
            file_path = os.path.join(path_cat,file_name)
            img.save(file_path)

            # generate doc information 
            # extract relative path 
            file_path_rel = os.path.relpath(file_path,PATH_DIR_CURRENT) 
            # add relative path to url 
            file_url = os.path.join(path_url_base,file_path_rel) 
            # write tag information inside markdown 
            md_file.add_subsection(tag)
            desc = f"tag:{cat}:{tag}"
            tag_img_md_format = md_file.add_image(desc,file_url)
            md_file.add_new_line()
            md_file.add_element_quote(tag_img_md_format)

    md_file.write(os.path.join(PATH_DIR_CURRENT,"readme.md"))



