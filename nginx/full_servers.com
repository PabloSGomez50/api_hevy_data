# frontend.conf

# Redirect HTTP traffic to HTTPS
server {
    listen 80;
    server_name frontend.spg.com.ar;

    return 301 https://$host$request_uri;
}

# HTTPS server block for the frontend app
server {
    listen 443 ssl;
    server_name frontend.spg.com.ar;

    ssl_certificate /etc/letsencrypt/live/frontend.spg.com.ar/fullchain.pem; # Replace with your SSL certificate path
    ssl_certificate_key /etc/letsencrypt/live/frontend.spg.com.ar/privkey.pem; # Replace with your SSL private key path

    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        # Your frontend app configuration
        root /path/to/frontend/app;
        index index.html;

        # Add any additional configurations needed for your frontend app
    }
}

# Server block for the Django API
server {
    listen 443 ssl;
    server_name labapi.spg.com.ar;

    ssl_certificate /etc/letsencrypt/live/labapi.spg.com.ar/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/labapi.spg.com.ar/privkey.pem;

    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        # Add any additional proxy configurations if needed
    }
}

# Server block for the FastAPI API
server {
    listen 443 ssl;
    server_name franhevy.spg.com.ar;

    ssl_certificate /etc/letsencrypt/live/franhevy.spg.com.ar/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/franhevy.spg.com.ar/privkey.pem;

    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        # Add any additional proxy configurations if needed
    }
}