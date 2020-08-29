import json
import os 
from PIL import Image,ImageDraw,ImageFont, ImageOps

FONT_SIZE = 15
PADDING_SIZE = 10
BORDER_SIZE = 2

PATH_DIR_CURRENT = os.path.dirname(os.path.realpath(__file__))
PATH_DIR_TAGS = os.path.join(PATH_DIR_CURRENT,"tags/")
PATH_FILE_FONT = os.path.join(PATH_DIR_CURRENT,"font/RussoOne-Regular.ttf")
PATH_FILE_CONFIG_TAGS = os.path.join(PATH_DIR_CURRENT,"config_tags.json")

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
    size_img[1] += 2*padding
    img = Image.new('RGB', size_img, color = color)
    img = ImageOps.expand(img,border=BORDER_SIZE,fill='black')
    d = ImageDraw.Draw(img)
    d.text((padding,padding), content,fill = (0,0,0),font=font)
    return img 

def fix_conflict_name(content,conflict_dict=CONFLICT_CHARS): 
    for c_conflict, c_resolve in conflict_dict.items(): 
        content = content.replace(c_conflict,c_resolve)
    return content

if __name__ == "__main__":
    font = ImageFont.truetype(PATH_FILE_FONT,FONT_SIZE)

    config_tags = load_config_tags()
    for cat, cat_tags in config_tags.items():
        path_cat = os.path.join(PATH_DIR_TAGS,cat)
        if not os.path.exists(path_cat):
            os.makedirs(path_cat)
        for tag in cat_tags: 
            img = generate_image(tag,font=font)
            file_name = f"{fix_conflict_name(tag)}.png"
            img.save(os.path.join(path_cat,file_name))

