#!/usr/bin/sh 

# version information
version_name="v1.10"
version_desc="version 1.10"

# generate tags 
./generator_tags.py --version ${version_name}

# add all tags, readme and tags.json
git rm -r --cached tags/
git add readme.md  
git add tags.json
git add tags

# create commit 
git commit -m "add new tags" 

# create tag 
git tag -a ${version_name} -m '${version_desc}' 

# push modification
git push origin master --tags