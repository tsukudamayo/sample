#!/bin/bash

if [ $# != 1 ]; then
    echo "define profile name"
    echo "usage: ./init.sh profile_name"
    exit 1
else
    echo "profile name" $1
fi

aws configure --profile $1
mkdir infra && cd infra
npm install -g typescript \
    aws-cdk
cdk init app --language=typescript
npm install -D \
    eslint \
    @typescript-eslint/parser \
    @typescript-eslint/eslint-plugin \
    prettier \
    eslint-config-prettier \
    eslint-plugin-prettier

cp ../config/.eslintrc.js ./
cp ../config/.prettierrc.js ./
echo "!.eslintrc.js" >> .gitignore
echo "!.prettierrc.js" >> .gitignore
