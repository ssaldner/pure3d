#!/bin/bash

BASE=github/clariah/pure3d
EDITION_DIR="$BASE/data/editions"
LOCAL_DIR="$BASE/_local/generated/editions"

cd ~/$EDITION_DIR

editions=`ls`

for edition in $editions
do
    echo "Edition $edition"
    cd $edition
    if [[ -e "3d" ]]; then
        cd "3d"
        models=`ls`
        for model in $models
        do
            if [[ -e "$model/articlesOrig" ]]; then
                mdhtml --tomd -o $model/articles $model/articlesOrig
            fi
        done
        cd ..
    fi
    cd ..
done

mdhtml --tohtml -o ~/$LOCAL_DIR .
