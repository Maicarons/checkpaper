# 配置说明

CheckPaper 使用 `pydantic-settings` 进行类型安全的配置管理。所有配置可通过环境变量或 `.env` 文件设置。

## 配置文件

主配置位于 `backend/app/core/config.py`。设置从项目根目录的 `.env` 文件加载。

### 快速配置

```bash
cp .env.example .env
# 编辑 .env 文件
```

## 应用设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `APP_NAME` | string | `CheckPaper` | 应用名称 |
| `APP_VERSION` | string | `0.1.0` | 应用版本 |
| `DEBUG` | boolean | `false` | 调试模式 |
| `SECRET_KEY` | string | `change-me-in-production` | 应用密钥 |

## API 设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `API_V1_PREFIX` | string | `/api/v1` | API 版本前缀 |
| `PROJECT_NAME` | string | `CheckPaper` | 项目名称 |

## CORS 设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `BACKEND_CORS_ORIGINS` | JSON 数组 | `["http://localhost:9032","http://localhost:9031"]` | 允许的 CORS 来源 |

## 数据库设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `DATABASE_URL` | string | `sqlite:///./checkpaper.db` | 数据库连接 URL |
| `DB_ECHO` | boolean | `false` | 记录 SQL 语句 |

### SQLite（开发环境）

```env
DATABASE_URL=sqlite:///./checkpaper.db
```

### MySQL（生产环境）

```env
DATABASE_URL=mysql+pymysql://checkpaper:password@localhost:3306/checkpaper
```

::: tip
使用 MySQL 时，请确保安装了 `pymysql` 和 `cryptography` 包。它们已包含在项目依赖中。
:::

## OpenAI 设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `OPENAI_API_KEY` | string | `""` | OpenAI API 密钥（本地模型可为空） |
| `OPENAI_BASE_URL` | string | `http://192.168.56.1:8990` | API 基础 URL（支持本地模型） |
| `OPENAI_MODEL` | string | `qwythos-9b-claude-mythos-5-1m` | 模型名称 |
| `OPENAI_MAX_TOKENS` | integer | `4096` | 每次请求的最大令牌数 |

::: info
CheckPaper 支持任何 OpenAI 兼容的 API，包括本地部署的模型。将 `OPENAI_BASE_URL` 设置为你的本地模型端点即可。
:::

## GROBID 设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `GROBID_SERVER_URL` | string | `http://localhost:8070` | GROBID 服务器 URL |
| `GROBID_TIMEOUT` | integer | `30` | 请求超时（秒） |

## 文件上传设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `MAX_UPLOAD_SIZE_MB` | integer | `50` | 最大上传文件大小 (MB) |
| `UPLOAD_DIR` | string | `./uploads` | 上传目录路径 |
| `ALLOWED_EXTENSIONS` | string | `pdf,docx,doc,tex,latex,bib` | 允许的文件扩展名（逗号分隔） |

## 参考文献验证设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `CROSSREF_API_KEY` | string | `None` | Crossref API 密钥（可选，启用礼貌池） |
| `CROSSREF_MAILTO` | string | `user@example.com` | Crossref 礼貌池邮箱 |
| `SEMANTIC_SCHOLAR_API_KEY` | string | `None` | Semantic Scholar API 密钥（可选） |

## 报告设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `REPORT_OUTPUT_DIR` | string | `./reports` | 报告输出目录 |
| `REPORT_TEMPLATE_DIR` | string | `./templates` | 报告模板目录 |

## 日志设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `LOG_LEVEL` | string | `INFO` | 日志级别：DEBUG、INFO、WARNING、ERROR |
| `LOG_FILE` | string | `./logs/checkpaper.log` | 日志文件路径 |

## Agent 设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `AGENT_MAX_TURNS` | integer | `15` | Agent 最大对话轮次 |
| `AGENT_SANDBOX_ENABLED` | boolean | `true` | 启用代码执行沙箱 |
| `AGENT_CODE_EXECUTION_TIMEOUT` | integer | `60` | 代码执行超时（秒） |

## MCP 服务器设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `MCP_SERVER_HOST` | string | `0.0.0.0` | MCP 服务器绑定地址 |
| `MCP_SERVER_PORT` | integer | `8001` | MCP 服务器端口 |

## Docker 环境

使用 Docker Compose 时，环境变量从 `.env` 文件传入。`docker-compose.yml` 将这些变量映射到容器环境变量。

### 卷挂载

| 宿主机路径 | 容器路径 | 说明 |
|-----------|---------|------|
| `./uploads` | `/app/uploads` | 上传的文件 |
| `./reports` | `/app/reports` | 生成的报告 |
| `./logs` | `/app/logs` | 应用日志 |

### 端口映射

| 服务 | 容器端口 | 宿主机端口 |
|------|---------|-----------|
| Backend | 9031 | 9031 |
| Frontend | 80 | 9032 |
| MCP Server | 8001 | 8001 |
| MySQL | 3306 | 3306 |
