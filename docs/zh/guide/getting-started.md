# 快速开始

本指南将引导你在本地机器上安装和运行 CheckPaper。

## 环境要求

- **Python 3.11+**
- **Node.js 18+**（前端开发）
- **Git**
- **Docker & Docker Compose**（可选，用于容器化部署）

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/Maicarons/checkpaper.git
cd checkpaper
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 必填：OpenAI API 配置
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# 数据库（本地开发使用 SQLite）
DATABASE_URL=sqlite:///./checkpaper.db

# 应用配置
DEBUG=true
SECRET_KEY=your-secret-key
```

### 3. 安装后端依赖

**使用 uv（推荐）：**

```bash
pip install uv
uv sync
```

**使用 pip：**

```bash
pip install -e .
```

### 4. 启动后端服务

```bash
uvicorn backend.app.main:app --reload --port 9031
```

API 服务将在 `http://localhost:9031` 启动。交互式文档：
- Swagger UI: `http://localhost:9031/docs`
- ReDoc: `http://localhost:9031/redoc`

### 5. 安装并启动前端

```bash
cd frontend
npm install
npm start
```

前端将在 `http://localhost:9032` 启动。

### 6. 上传并验证第一篇论文

1. 在浏览器中打开 `http://localhost:9032`
2. 点击首页的 **"开始验证"** 按钮
3. 拖拽或选择论文文件（PDF、Word 或 LaTeX）
4. 选择需要执行的验证类型
5. 点击 **"开始验证"** 并等待结果
6. 查看详细的验证报告

## Docker 部署（替代方式）

一键部署：

```bash
# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 启动所有服务
docker-compose up -d

# 生产环境（包含 MySQL）
docker-compose --profile production up -d
```

服务访问地址：
- 前端: `http://localhost:9032`
- 后端 API: `http://localhost:9031`
- MCP 服务器: 端口 8001

## 验证安装

检查后端是否正常运行：

```bash
curl http://localhost:9031/health
```

预期响应：

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": 1704067200.0
}
```

## 下一步

- [功能特性](/zh/guide/features) — 了解所有验证能力
- [API 参考](/zh/api/) — 探索 REST API 端点
- [部署指南](/zh/guide/deployment) — 生产环境部署
