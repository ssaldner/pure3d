#!/bin/bash

HELP="
Copies data to /var directory
"
cd /var/data/pure3d

for d in ~/github/clariah/pure3d/data/*
do
    echo "Copy from data folder in Pure3D repo" 
    sudo cp -f -r $d .
    echo "Files have been overwritten"
done
