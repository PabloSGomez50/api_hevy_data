# API con informacion de entrenamientos
```bash
docker build . -t hevy-api:v1
docker run hevy-api:v1
```

```bash
sudo ln -s /etc/nginx/sites-available/<config_name>.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Obtener certificados SSL
```bash
sudo apt-get install certbot python3-certbot-nginx
certbot --nginx -d <domain-name>
```