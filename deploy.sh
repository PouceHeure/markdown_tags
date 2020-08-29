#!/usr/bin/sh 

git rm --cached ./tags

# generate tags 
python3 .generator_tags.py

# generate doc 
python3 .generator_doc.py 

git add readme.md  
git add config_tags.json
git add tags 

git commit -m "add new tags"
git push origin master