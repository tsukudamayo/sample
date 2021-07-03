#!/bin/bash

aws configure --profile $1
cdk init app --language=typescript
npm install -D \
    eslint \
    @typescript-eslint/parser \
    @typescript-eslint/eslint-plugin \
    prettier \
    eslint-config-prettier \
    eslint-plugin-prettier

echo "!.eslintrc.js" >> .gitignore
echo "!.prettierrc.js" >> .gitignore
