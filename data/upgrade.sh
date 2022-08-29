#!/bin/bash

cd editions

for ed in `ls`
do
    echo "upgrading edition $ed"
    cp ../editionsBetter/$ed/meta/* $ed/meta
    cp ../editionsBetter/$ed/texts/* $ed/texts
done
