# Deployment Guide

This guide covers how to deploy the application to production.

## Prerequisites

- Docker installed on the deployment server
- Access to the production database
- SSL certificates configured
- Environment variables set up

## Deployment Steps

### 1. Build the Docker Image

```bash
docker build -t myapp:latest .
```

### 2. Configure Environment Variables

Create a `.env` file with the following variables:

```
DATABASE_URL=postgresql://user:password@localhost:5432/production_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-production-secret-key
API_KEY=your-api-key
```

### 3. Run Database Migrations

```bash
docker run --rm --env-file .env myapp:latest python manage.py migrate
```

### 4. Start the Application

```bash
docker run -d \
  --name myapp \
  --env-file .env \
  -p 8000:8000 \
  myapp:latest
```

### 5. Set Up Nginx Reverse Proxy

Configure Nginx to proxy requests to the application:

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 6. Configure SSL with Let's Encrypt

```bash
certbot --nginx -d example.com
```

## Monitoring

- Check logs: `docker logs myapp`
- Health check endpoint: `https://example.com/api/health`
- Set up monitoring with Prometheus and Grafana

## Rollback Procedure

If deployment fails:

1. Stop the new container: `docker stop myapp`
2. Start the previous version: `docker start myapp-previous`
3. Investigate issues in logs
