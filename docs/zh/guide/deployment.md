# 部署指南

本指南涵盖 CheckPaper 在各种环境中的部署方式。

## Docker 部署（推荐）

### 快速开始

```bash
# 1. 克隆并配置
git clone https://github.com/Maicarons/checkpaper.git
cd checkpaper
cp .env.example .env
# 编辑 .env 文件

# 2. 启动所有服务
docker-compose up -d

# 3. 验证
curl http://localhost:9031/health
```

### 服务概览

| 服务 | 容器名 | 端口 | 说明 |
|------|--------|------|------|
| 后端 API | `checkpaper-backend` | 9031 | FastAPI 应用服务器 |
| MCP 服务器 | `checkpaper-mcp` | 8001 | 模型上下文协议工具服务器 |
| 前端 | `checkpaper-frontend` | 9032 | React Web 应用 |
| MySQL | `checkpaper-mysql` | 3306 | 生产数据库（可选） |

### 生产环境（含 MySQL）

```bash
docker-compose --profile production up -d
```

更新 `.env` 文件：

```env
DATABASE_URL=mysql+pymysql://checkpaper:password@checkpaper-mysql:3306/checkpaper
```

### Docker Compose 配置说明

`docker-compose.yml` 包含：

- **健康检查** — 所有服务 30 秒间隔检查
- **卷挂载** — 上传文件、报告和日志持久化
- **环境变量** — 从 `.env` 文件传入
- **重启策略** — `unless-stopped`
- **网络隔离** — 服务间网络隔离

### 管理服务

```bash
# 查看日志
docker-compose logs -f backend
docker-compose logs -f mcp-server

# 重启特定服务
docker-compose restart backend

# 停止所有服务
docker-compose down

# 停止并删除卷
docker-compose down -v

# 代码变更后重新构建
docker-compose build backend
docker-compose up -d backend
```

## 手动部署

### 后端

```bash
# 安装 Python 3.11+
python --version  # 应为 3.11+

# 安装依赖
pip install -e .

# 配置环境
cp .env.example .env
# 编辑 .env

# 启动服务
uvicorn backend.app.main:app \
  --host 0.0.0.0 \
  --port 9031 \
  --workers 4 \
  --log-level info
```

### 前端

```bash
cd frontend

# 安装依赖
npm install

# 构建生产版本
npm run build

# 使用 nginx 或其他静态文件服务器提供服务
# 构建输出在 dist/ 目录
```

### MCP 服务器

```bash
# 启动 MCP 服务器
python -c "from backend.mcp_server.server import main; main()"
```

## 环境变量

### 必填配置

| 变量 | 说明 | 示例 |
|------|------|------|
| `OPENAI_API_KEY` | OpenAI API 密钥（或本地模型密钥） | `sk-...` |
| `OPENAI_BASE_URL` | API 基础 URL | `https://api.openai.com/v1` |
| `OPENAI_MODEL` | 模型名称 | `gpt-4o` |

### 数据库配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DATABASE_URL` | 数据库连接字符串 | `sqlite:///./checkpaper.db` |
| `DB_ECHO` | 记录 SQL 查询 | `false` |

### 应用配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DEBUG` | 调试模式 | `false` |
| `SECRET_KEY` | 应用密钥 | `change-me-in-production` |
| `API_V1_PREFIX` | API 路由前缀 | `/api/v1` |
| `LOG_LEVEL` | 日志级别 | `INFO` |

### 文件存储配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `UPLOAD_DIR` | 上传目录 | `./uploads` |
| `REPORT_OUTPUT_DIR` | 报告输出目录 | `./reports` |
| `MAX_UPLOAD_SIZE_MB` | 最大文件大小 (MB) | `50` |
| `ALLOWED_EXTENSIONS` | 允许的文件扩展名 | `pdf,docx,doc,tex,latex,bib` |

### 外部 API 配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `CROSSREF_API_KEY` | Crossref API 密钥 | `None` |
| `CROSSREF_MAILTO` | Crossref 礼貌池邮箱 | `user@example.com` |
| `SEMANTIC_SCHOLAR_API_KEY` | Semantic Scholar API 密钥 | `None` |
| `GROBID_SERVER_URL` | GROBID 服务器 URL | `http://localhost:8070` |

### CORS 配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `BACKEND_CORS_ORIGINS` | 允许的 CORS 来源 | `["http://localhost:9032","http://localhost:9031"]` |

## 反向代理配置

### Nginx

```nginx
server {
    listen 80;
    server_name checkpaper.example.com;

    # 前端
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://127.0.0.1:9031;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 50M;
    }
}
```

## SSL/TLS 配置

```bash
# 安装 certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d checkpaper.example.com

# 自动续期
sudo certbot renew --dry-run
```

## 监控

### 健康检查

```bash
# 基础健康检查
curl http://localhost:9031/health

# 详细健康检查（含系统信息）
curl http://localhost:9031/health/detailed
```

### 日志

```bash
# 查看应用日志
tail -f logs/checkpaper.log

# Docker 日志
docker-compose logs -f --tail=100 backend
```

## 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 端口被占用 | 同一端口已有其他服务 | 在 `.env` 或 `docker-compose.yml` 中修改端口 |
| 数据库连接错误 | DATABASE_URL 配置错误 | 检查连接字符串 |
| OpenAI API 错误 | API 密钥或 URL 无效 | 检查 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL` |
| 文件上传失败 | 文件过大或格式不对 | 检查 `MAX_UPLOAD_SIZE_MB` 和 `ALLOWED_EXTENSIONS` |
| CORS 错误 | 前端来源未被允许 | 更新 `BACKEND_CORS_ORIGINS` |

### 重置应用

```bash
# 停止服务
docker-compose down

# 删除数据库
rm -f checkpaper.db

# 删除上传文件和报告
rm -rf uploads/ reports/

# 重启
docker-compose up -d
```
