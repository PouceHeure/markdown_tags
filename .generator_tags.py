import json
import os 
from PIL import Image,ImageDraw,ImageFont, ImageOps

FONT_SIZE = 20
PADDING_SIZE = 10
BORDER_SIZE = 2
FONT = ImageFont.truetype("./font/Rubik-Regular.ttf",FONT_SIZE)


PATH_DIR_TAGS = "./tags/"

def load_config_tags(path_file="./config_tags.json"):
    data = None
    with open(path_file) as f:
        data = json.load(f)
    return data 

def generate_image(content,color=(255,255,255),font=FONT,padding=PADDING_SIZE):
    size_img = list(font.getsize(content))
    size_img[0] += 2*padding
    size_img[1] += 2*padding
    img = Image.new('RGB', size_img, color = color)
    img = ImageOps.expand(img,border=BORDER_SIZE,fill='black')
    d = ImageDraw.Draw(img)
    d.text((padding,padding), content,fill = (0,0,0),font=font)
    return img 

config_tags = load_config_tags()
for cat, cat_tags in config_tags.items():
    path_cat = os.path.join(PATH_DIR_TAGS,cat)
    if not os.path.exists(path_cat):
        os.makedirs(path_cat)
    for tag in cat_tags: 
        img = generate_image(tag)
        img.save(os.path.join(path_cat,f"{tag}.png"))


print(config_tags)


# img = generate_image("ROS")
# img.show()
