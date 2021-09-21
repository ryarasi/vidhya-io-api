upstream vidhya {
    server web:$PORT;
}

server {

    listen 80;

    location /static {
        alias /vol/static;
    }
    
    location / {
        proxy_pass              http://vidhya;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header        Host web;
        proxy_redirect          off;
        client_max_body_size    10M;
    }
}