server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name 34.67.90.15 franhevy.spg.com.ar;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}