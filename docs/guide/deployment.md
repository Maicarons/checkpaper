# Deployment

This guide covers deploying CheckPaper in various environments.

## Docker Deployment (Recommended)

### Quick Start

```bash
# 1. Clone and configure
git clone https://github.com/Maicarons/checkpaper.git
cd checkpaper
cp .env.example .env
# Edit .env with your settings

# 2. Start all services
docker-compose up -d

# 3. Verify
curl http://localhost:9031/health
```

### Services Overview

| Service | Container | Port | Description |
|---------|-----------|------|-------------|
| Backend API | `checkpaper-backend` | 9031 | FastAPI application server |
| MCP Server | `checkpaper-mcp` | 8001 | Model Context Protocol tool server |
| Frontend | `checkpaper-frontend` | 9032 | React web application |
| MySQL | `checkpaper-mysql` | 3306 | Production database (optional) |

### Production Deployment with MySQL

```bash
# Start with MySQL database
docker-compose --profile production up -d
```

This adds a MySQL 8.0 instance. Update your `.env`:

```env
DATABASE_URL=mysql+pymysql://checkpaper:password@checkpaper-mysql:3306/checkpaper
```

### Docker Compose Configuration

The `docker-compose.yml` includes:

- **Health checks** for all services (30-second intervals)
- **Volume mounts** for uploads, reports, and logs
- **Environment variable** passthrough from `.env`
- **Restart policies** (`unless-stopped`)
- **Network isolation** between services

### Managing Services

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f mcp-server

# Restart a specific service
docker-compose restart backend

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild after code changes
docker-compose build backend
docker-compose up -d backend
```

## Manual Deployment

### Backend

```bash
# Install Python 3.11+
python --version  # Should be 3.11+

# Install dependencies
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env

# Start with uvicorn
uvicorn backend.app.main:app \
  --host 0.0.0.0 \
  --port 9031 \
  --workers 4 \
  --log-level info
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Serve with nginx or any static file server
# The build output is in dist/
```

### MCP Server

```bash
# Start the MCP server
python -c "from backend.mcp_server.server import main; main()"
```

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (or local model key) | `sk-...` |
| `OPENAI_BASE_URL` | API base URL | `https://api.openai.com/v1` |
| `OPENAI_MODEL` | Model name | `gpt-4o` |

### Database

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./checkpaper.db` |
| `DB_ECHO` | Log SQL queries | `false` |

### Application

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Debug mode | `false` |
| `SECRET_KEY` | Application secret key | `change-me-in-production` |
| `API_V1_PREFIX` | API route prefix | `/api/v1` |
| `LOG_LEVEL` | Logging level | `INFO` |

### File Storage

| Variable | Description | Default |
|----------|-------------|---------|
| `UPLOAD_DIR` | Upload directory | `./uploads` |
| `REPORT_OUTPUT_DIR` | Report output directory | `./reports` |
| `MAX_UPLOAD_SIZE_MB` | Maximum file size (MB) | `50` |
| `ALLOWED_EXTENSIONS` | Allowed file extensions | `pdf,docx,doc,tex,latex,bib` |

### External APIs

| Variable | Description | Default |
|----------|-------------|---------|
| `CROSSREF_API_KEY` | Crossref API key | `None` |
| `CROSSREF_MAILTO` | Crossref polite pool email | `user@example.com` |
| `SEMANTIC_SCHOLAR_API_KEY` | Semantic Scholar API key | `None` |
| `GROBID_SERVER_URL` | GROBID server URL | `http://localhost:8070` |

### CORS

| Variable | Description | Default |
|----------|-------------|---------|
| `BACKEND_CORS_ORIGINS` | Allowed CORS origins | `["http://localhost:9032","http://localhost:9031"]` |

## Reverse Proxy Configuration

### Nginx

```nginx
server {
    listen 80;
    server_name checkpaper.example.com;

    # Frontend
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:9031;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 50M;
    }

    # WebSocket (for future real-time updates)
    location /ws/ {
        proxy_pass http://127.0.0.1:9031;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## SSL/TLS with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d checkpaper.example.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Monitoring

### Health Check Endpoint

```bash
# Basic health check
curl http://localhost:9031/health

# Detailed health check (includes system info)
curl http://localhost:9031/health/detailed
```

### Log Files

Logs are stored in the `logs/` directory:

```bash
# View application logs
tail -f logs/checkpaper.log

# Docker logs
docker-compose logs -f --tail=100 backend
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Port already in use | Another service on the same port | Change the port in `.env` or `docker-compose.yml` |
| Database connection error | Wrong DATABASE_URL | Verify the connection string |
| OpenAI API error | Invalid API key or base URL | Check `OPENAI_API_KEY` and `OPENAI_BASE_URL` |
| File upload fails | File too large or wrong format | Check `MAX_UPLOAD_SIZE_MB` and `ALLOWED_EXTENSIONS` |
| CORS error | Frontend origin not allowed | Update `BACKEND_CORS_ORIGINS` |

### Resetting the Application

```bash
# Stop services
docker-compose down

# Remove database
rm -f checkpaper.db

# Remove uploads and reports
rm -rf uploads/ reports/

# Restart
docker-compose up -d
```
