#!/bin/bash

cd projects

for pr in `ls`
do
    echo "renaming 3d to projects in projects $pr"
    sudo mv ../$pr/3d ../$pr/projects
done
