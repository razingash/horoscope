FROM node:21-alpine AS build

WORKDIR /app

COPY package.json /app/
COPY package-lock.json /app/

RUN npm install

COPY . /app/
ARG REACT_APP_BASE_URL="http://localhost:8080/api/"
ENV REACT_APP_BASE_URL=$REACT_APP_BASE_URL

RUN npm run build


FROM nginx

COPY --from=build /app/build /usr/share/nginx/html
COPY --from=build /app/static/translations /usr/share/nginx/html/static/js

COPY ./nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
