#!/bin/bash

if [ $# != 1 ]; then
    echo "define profile name"
    exit 1
else
    echo "profile name" $1
fi

aws configure --profile $1
mkdir infra && cd infra
cdk init app --language=typescript
npm install -D \
    eslint \
    @typescript-eslint/parser \
    @typescript-eslint/eslint-plugin \
    prettier \
    eslint-config-prettier \
    eslint-plugin-prettier

cp ../.eslintrc.js ./
cp ../.prettierrc.js ./
echo "!.eslintrc.js" >> .gitignore
echo "!.prettierrc.js" >> .gitignore
