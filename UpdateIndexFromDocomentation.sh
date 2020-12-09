#!/bin/bash

cd ../website/

#copy files from main repo
cp ../cs107-FinalProject/docs/documentation.ipynb ./documentation.ipynb

#convert notebook to markdown
jupyter nbconvert $(pwd)/documentation.ipynb --to markdown --output $(pwd)/index.md

#add title to file
sed -i '1s/^/---\n/' index.md
sed -i '1s/^/ title: About the code \n/' index.md
sed -i '1s/^/---\n/' index.md

#commit, push and publish
git pull
git add index.md documentation.ipynb
git commit -m 'updated index.md with documentation <automated>'
git push