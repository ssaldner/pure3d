#!/bin/bash

BASE=github/clariah/pure3d
PROJECT_DIR="$BASE/data/projects"
LOCAL_DIR="$BASE/_local/generated/projects"

cd ~/$PROJECT_DIR

projects=`ls`

for project in $projects
do
    echo "Model $project"
    cd $project
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
