# CheckPaper - AI论文验证智能体系统

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 项目简介

CheckPaper 是一个基于 AI 的学术论文验证智能体系统。它能自动检测学术论文中的各种问题，包括格式不规范、引用错误、参考文献造假、数据真实性问题等，帮助研究者提升论文质量和可信度。

## 功能特性

- **格式检查** — 验证标题层级、编号规范、字体一致性、页面布局和目录准确性
- **图表引用检查** — 交叉验证所有图表定义与正文引用，检测"孤儿引用"和"未引用"的图表
- **引用完整性检查** — 验证正文引用与参考文献列表的一致性，检测重复引用和缺失引用
- **数据来源验证** — 验证数据来源的真实性和可访问性
- **数据处理验证** — 执行 GRIM/SPRITE 统计一致性测试，验证 p 值和置信区间
- **参考文献验证** — 通过 Crossref 和 Semantic Scholar API 验证参考文献真实性，检查 DOI 有效性，检测可疑引用

## 支持格式

| 格式 | 扩展名 | 解析器 |
|------|--------|--------|
| PDF | `.pdf` | PyMuPDF |
| Word | `.docx`, `.doc` | python-docx |
| LaTeX | `.tex`, `.latex` | pylatexenc |
| BibTeX | `.bib` | bibtexparser |

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+（前端开发）
- Docker & Docker Compose（可选）

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/Maicarons/checkpaper.git
cd checkpaper

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置 OpenAI API Key 等

# 3. 安装后端依赖
pip install uv
uv sync

# 4. 启动后端服务
uvicorn backend.app.main:app --reload --port 9031

# 5. 安装并启动前端
cd frontend
npm install
npm start
```

应用访问地址：
- **前端界面：** http://localhost:9032
- **后端 API：** http://localhost:9031
- **Swagger 文档：** http://localhost:9031/docs

### Docker 部署

```bash
# 启动所有服务
docker-compose up -d

# 生产环境（包含 MySQL）
docker-compose --profile production up -d
```

## 项目结构

```
checkpaper/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/v1/endpoints/   # API 路由处理
│   │   ├── core/               # 配置、安全、数据库
│   │   ├── services/           # 业务逻辑
│   │   │   ├── document/       # 文档解析服务
│   │   │   ├── validation/     # 验证编排
│   │   │   ├── agent/          # AI Agent 服务
│   │   │   └── report/         # 报告生成
│   │   ├── schemas/            # Pydantic 数据模型
│   │   ├── prompts/            # LLM 提示词模板
│   │   └── main.py             # FastAPI 应用入口
│   ├── mcp_server/             # MCP 工具服务器
│   │   ├── tools/              # 工具实现
│   │   └── server.py           # MCP 服务器入口
│   └── tests/                  # 测试文件
├── frontend/                   # React 前端应用
│   └── src/
│       ├── pages/              # 页面组件
│       ├── components/         # 可复用组件
│       ├── services/           # API 客户端
│       └── hooks/              # 自定义 React Hook
├── docs/                       # VitePress 文档
├── docker-compose.yml          # Docker 配置
├── pyproject.toml              # Python 项目配置
└── .env.example                # 环境变量模板
```

## 技术栈

| 组件 | 技术 |
|------|------|
| 后端 | Python 3.11+ · FastAPI · SQLModel |
| 前端 | React 18 · TypeScript · Ant Design |
| AI Agent | OpenAI Agents SDK · MCP 协议 |
| 文档解析 | PyMuPDF · python-docx · pylatexenc |
| 参考文献验证 | Crossref API · Semantic Scholar API |
| 数据库 | SQLite (开发) · MySQL (生产) |
| 部署 | Docker · Docker Compose |

## API 参考

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/documents/upload` | POST | 上传论文文档 |
| `/api/v1/documents/` | GET | 获取文档列表 |
| `/api/v1/documents/{id}` | GET | 获取文档详情 |
| `/api/v1/documents/{id}/parse` | POST | 解析文档内容 |
| `/api/v1/validation/start` | POST | 开始验证任务 |
| `/api/v1/validation/tasks/{id}/results` | GET | 获取验证结果 |
| `/api/v1/validation/types` | GET | 获取验证类型列表 |
| `/api/v1/reports/` | GET | 获取报告列表 |
| `/api/v1/reports/{id}/download` | GET | 下载报告（md/pdf/html） |
| `/health` | GET | 健康检查 |

完整 API 文档请参考 [docs/zh/api/](docs/zh/api/)，或在服务运行时访问 `http://localhost:9031/docs`。

## 验证类型

| 类型 | 说明 |
|------|------|
| `format` | 格式和结构检查 |
| `figure_table` | 图表引用验证 |
| `citation` | 引用完整性检查 |
| `data_source` | 数据来源验证 |
| `data_processing` | 统计一致性验证 |
| `reference` | 参考文献真实性验证 |

## 文档

完整的文档使用 [VitePress](https://vitepress.dev/) 构建：

```bash
cd docs
npm install
npm run dev     # 开发服务器
npm run build   # 生产构建
```

- **中文文档：** [docs/zh/guide/introduction.md](docs/zh/guide/introduction.md)
- **English:** [docs/guide/introduction.md](docs/guide/introduction.md)

## 配置说明

主要环境变量（完整选项请参见 [`.env.example`](.env.example)）：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENAI_API_KEY` | OpenAI API 密钥 | — |
| `OPENAI_BASE_URL` | API 基础 URL | `http://192.168.56.1:8990` |
| `DATABASE_URL` | 数据库连接 | `sqlite:///./checkpaper.db` |
| `DEBUG` | 调试模式 | `false` |
| `SECRET_KEY` | 应用密钥 | `change-me-in-production` |

## 测试

```bash
# 后端测试
pytest

# 后端测试（含覆盖率）
pytest --cov=backend/app --cov-report=html

# 前端测试
cd frontend && npm test

# 代码检查
ruff check . && mypy .
```

## 贡献

欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 或 [开发者指南](docs/zh/developer/contributing.md) 了解详情。

## 许可证

本项目采用 MIT 许可证 — 详见 [LICENSE](LICENSE) 文件。

## 致谢

使用 [FastAPI](https://fastapi.tiangolo.com/)、[OpenAI](https://openai.com/)、[PyMuPDF](https://pymupdf.readthedocs.io/)、[Ant Design](https://ant.design/) 和 [MCP 协议](https://modelcontextprotocol.io/) 构建。

---

[English Documentation](README.md)
