FROM node:18-bullseye-slim

ENV LANG ja_JP.UTF-8
ENV HOST 0.0.0.0

RUN apt-get update \
    && apt-get -y install git \
    yarn \
    curl \
    locales \
    && locale-gen ja_JP.UTF-8 \
    && localedef -f UTF-8 -i ja_JP ja_JP.utf8 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

#RUN npx create-next-app --example https://github.com/nikolasburk/blogr-nextjs-prisma/tree/main boaters_app
# RUN git clone -b part-1 https://github.com/m-abdelwahab/awesome-links.git

# deploy local docker-compose
#RUN `echo DATABASE_URL="mysql://${DB_USERNAME}:${DB_PASSWORD}@${DB_HOST}:3306/${DB_TABLENAME}?schema=public" > .env`

# RUN `echo DATABASE_URL="postgresql://${DB_USERNAME}:${DB_PASSWORD}@${DB_HOST}:5432/${DB_TABLENAME}?schema=public" > .env`

# deploy GCP Cloud Run 
#RUN `echo DATABASE_URL="mysql://${DB_USERNAME}:${DB_PASSWORD}@${DB_HOST}:3306/${DB_TABLENAME}?host=/cloudsql/${DB_INSTANCE_NAME}" > .env`

# RUN npm install

EXPOSE 3000
# deploy GCP Cloud Run
#EXPOSE 8080

CMD ["/bin/bash"]
# deploy GCP Cloud Run
#CMD [ "npm", "run", "cloudrun" ]
