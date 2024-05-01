FROM nginx:alpine

RUN rm /etc/nginx/conf.d/*

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./html /etc/nginx/html
COPY ../keys/translate /etc/nginx/translate-bur.key
COPY ../keys/translate_crt /etc/nginx/translate-bur.crt

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
#CMD ["service", "nginx", "reload"]
