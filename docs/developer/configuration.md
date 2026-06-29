# Configuration

CheckPaper uses `pydantic-settings` for type-safe configuration management. All settings can be configured via environment variables or a `.env` file.

## Configuration File

The main configuration is in `backend/app/core/config.py`. Settings are loaded from the `.env` file in the project root.

### Quick Setup

```bash
cp .env.example .env
# Edit .env with your settings
```

## Application Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `APP_NAME` | string | `CheckPaper` | Application name |
| `APP_VERSION` | string | `0.1.0` | Application version |
| `DEBUG` | boolean | `false` | Enable debug mode |
| `SECRET_KEY` | string | `change-me-in-production` | Application secret key for security |

## API Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `API_V1_PREFIX` | string | `/api/v1` | API version prefix |
| `PROJECT_NAME` | string | `CheckPaper` | Project name |

## CORS Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `BACKEND_CORS_ORIGINS` | JSON array | `["http://localhost:9032","http://localhost:9031"]` | Allowed CORS origins |

## Database Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DATABASE_URL` | string | `sqlite:///./checkpaper.db` | Database connection URL |
| `DB_ECHO` | boolean | `false` | Log SQL statements |

### SQLite (Development)

```env
DATABASE_URL=sqlite:///./checkpaper.db
```

### MySQL (Production)

```env
DATABASE_URL=mysql+pymysql://checkpaper:password@localhost:3306/checkpaper
```

::: tip
When using MySQL, ensure `pymysql` and `cryptography` packages are installed. They are included in the project dependencies.
:::

## OpenAI Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `OPENAI_API_KEY` | string | `""` | OpenAI API key (empty for local models) |
| `OPENAI_BASE_URL` | string | `http://192.168.56.1:8990` | API base URL (supports local models) |
| `OPENAI_MODEL` | string | `qwythos-9b-claude-mythos-5-1m` | Model name |
| `OPENAI_MAX_TOKENS` | integer | `4096` | Maximum tokens per request |

::: info
CheckPaper supports any OpenAI-compatible API, including locally deployed models. Set `OPENAI_BASE_URL` to your local model's endpoint.
:::

## GROBID Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `GROBID_SERVER_URL` | string | `http://localhost:8070` | GROBID server URL |
| `GROBID_TIMEOUT` | integer | `30` | Request timeout (seconds) |

## File Upload Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MAX_UPLOAD_SIZE_MB` | integer | `50` | Maximum upload file size in MB |
| `UPLOAD_DIR` | string | `./uploads` | Upload directory path |
| `ALLOWED_EXTENSIONS` | string | `pdf,docx,doc,tex,latex,bib` | Comma-separated allowed extensions |

## Reference Verification Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CROSSREF_API_KEY` | string | `None` | Crossref API key (optional, enables polite pool) |
| `CROSSREF_MAILTO` | string | `user@example.com` | Email for Crossref polite pool |
| `SEMANTIC_SCHOLAR_API_KEY` | string | `None` | Semantic Scholar API key (optional) |

## Report Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `REPORT_OUTPUT_DIR` | string | `./reports` | Report output directory |
| `REPORT_TEMPLATE_DIR` | string | `./templates` | Report template directory |

## Logging Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `LOG_LEVEL` | string | `INFO` | Log level: DEBUG, INFO, WARNING, ERROR |
| `LOG_FILE` | string | `./logs/checkpaper.log` | Log file path |

## Agent Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `AGENT_MAX_TURNS` | integer | `15` | Maximum agent conversation turns |
| `AGENT_SANDBOX_ENABLED` | boolean | `true` | Enable code execution sandbox |
| `AGENT_CODE_EXECUTION_TIMEOUT` | integer | `60` | Code execution timeout (seconds) |

## MCP Server Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MCP_SERVER_HOST` | string | `0.0.0.0` | MCP server bind address |
| `MCP_SERVER_PORT` | integer | `8001` | MCP server port |

## Docker Environment

When using Docker Compose, environment variables are passed from the `.env` file. The `docker-compose.yml` maps these variables to container environment variables.

### Volume Mounts

| Host Path | Container Path | Description |
|-----------|----------------|-------------|
| `./uploads` | `/app/uploads` | Uploaded files |
| `./reports` | `/app/reports` | Generated reports |
| `./logs` | `/app/logs` | Application logs |

### Port Mapping

| Service | Container Port | Host Port |
|---------|---------------|-----------|
| Backend | 9031 | 9031 |
| Frontend | 80 | 9032 |
| MCP Server | 8001 | 8001 |
| MySQL | 3306 | 3306 |
