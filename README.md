# CheckPaper - AI论文验证智能体系统

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 项目简介

CheckPaper 是一个基于 AI 的论文验证智能体系统，能够自动检测学术论文中的各种问题，包括格式规范、引用完整性、数据真实性等。

### ✨ 主要功能

- **格式检查**：检查论文格式、结构、目录对应关系
- **图表引用检查**：检测图片/表格是否在文中被显式引用
- **参考文献引用检查**：验证参考文献是否在文中被引用
- **数据来源验证**：验证论文中数据来源的真实性
- **数据处理验证**：验证论文数据处理的真实性
- **参考文献验证**：联网搜索验证参考文献的真实性

### 🎯 支持格式

- PDF
- Word (DOCX)
- LaTeX

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+ (前端开发)
- Docker & Docker Compose (可选)

### 本地开发

1. **克隆项目**
```bash
git clone https://github.com/yourusername/checkpaper.git
cd checkpaper
```

2. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，配置 OpenAI API Key 等
```

3. **安装后端依赖**
```bash
# 使用 uv (推荐)
pip install uv
uv sync

# 或使用 pip
pip install -e .
```

4. **启动后端服务**
```bash
uvicorn backend.app.main:app --reload --port 8000
```

5. **安装前端依赖**
```bash
cd frontend
npm install
npm start
```

### Docker 部署

```bash
# 启动所有服务
docker-compose up -d

# 启动生产环境（包含 MySQL）
docker-compose --profile production up -d
```

## 📁 项目结构

```
checkpaper/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/               # API 路由
│   │   ├── core/              # 核心配置
│   │   ├── services/          # 业务服务
│   │   ├── schemas/           # 数据模型
│   │   ├── prompts/           # 提示词模板
│   │   └── main.py            # 应用入口
│   ├── mcp_server/            # MCP 服务器
│   └── tests/                 # 测试文件
├── frontend/                   # 前端应用
├── docker-compose.yml          # Docker 配置
├── pyproject.toml              # Python 项目配置
└── README.md                   # 项目文档
```

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `OPENAI_API_KEY` | OpenAI API 密钥 | - |
| `DATABASE_URL` | 数据库连接地址 | `sqlite:///./checkpaper.db` |
| `SECRET_KEY` | 应用密钥 | `change-me-in-production` |
| `DEBUG` | 调试模式 | `false` |

### 数据库配置

**本地开发 (SQLite)**
```env
DATABASE_URL=sqlite:///./checkpaper.db
```

**生产环境 (MySQL)**
```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/checkpaper
```

## 📚 API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 主要 API 端点

- `POST /api/v1/documents/upload` - 上传论文
- `POST /api/v1/validation/start` - 开始验证
- `GET /api/v1/validation/tasks/{task_id}/results` - 获取验证结果
- `GET /api/v1/reports/{report_id}` - 获取报告

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行带覆盖率的测试
pytest --cov=backend/app --cov-report=html

# 运行特定测试
pytest backend/tests/test_validation.py
```

## 🛠️ 技术栈

- **后端**: Python, FastAPI, SQLModel, OpenAI Agents SDK
- **前端**: React, TypeScript, Ant Design
- **数据库**: SQLite (开发), MySQL (生产)
- **文档解析**: PyMuPDF, python-docx, pylatexenc
- **部署**: Docker, Docker Compose

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 📧 联系方式

- 项目主页: https://github.com/yourusername/checkpaper
- 问题反馈: https://github.com/yourusername/checkpaper/issues

## 🙏 致谢

感谢以下开源项目：
- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI](https://openai.com/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [Ant Design](https://ant.design/)
