#!/bin/bash

cd ../data/projects

for pr in `ls`
do
    echo "renaming 3d to editionsin projects $pr"
    mv ../$pr/3d ../$pr/editions
done
