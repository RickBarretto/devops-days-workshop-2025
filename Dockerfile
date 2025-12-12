FROM nginx:1.29-alpine

COPY ./aws-ec2 /usr/share/nginx/html
