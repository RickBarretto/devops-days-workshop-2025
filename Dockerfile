FROM nginx:1.29-alpine

COPY ./aws-deploy /usr/share/nginx/html
