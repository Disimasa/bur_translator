FROM nginx:alpine

RUN rm /etc/nginx/conf.d/*

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./html /etc/nginx/html
COPY ../keys/translate-bur.crt /etc/nginx/translate-bur.crt
COPY ../keys/translate-bur.key /etc/nginx/translate-bur.key

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
#CMD ["service", "nginx", "reload"]
