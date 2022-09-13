#!/bin/bash

cd projects

for ed in `ls`
do
    echo "upgrading project $ed"
    cp ../projectsBetter/$ed/meta/* $ed/meta
    cp ../projectsBetter/$ed/texts/* $ed/texts
done
