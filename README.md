# CheckPaper - AI Paper Verification Agent

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)

## About

CheckPaper is an AI-powered academic paper verification agent system. It automatically detects various issues in academic papers — including formatting non-compliance, citation errors, reference fraud, and data integrity problems — helping researchers improve the quality and reliability of their work.

## Features

- **Format Checking** — Validates heading hierarchy, numbering consistency, font uniformity, page layout, and TOC accuracy
- **Figure & Table Reference Check** — Cross-references all figure/table definitions against in-text citations; detects orphan and uncited references
- **Citation Integrity Check** — Validates that every in-text citation matches a reference list entry; detects duplicates and missing references
- **Data Source Verification** — Verifies data source authenticity and accessibility
- **Data Processing Verification** — Runs GRIM/SPRITE statistical consistency tests; validates p-values and confidence intervals
- **Reference Verification** — Verifies references against Crossref and Semantic Scholar APIs; checks DOI validity and detects potentially fraudulent citations

## Supported Formats

| Format | Extensions | Parser |
|--------|-----------|--------|
| PDF | `.pdf` | PyMuPDF |
| Word | `.docx`, `.doc` | python-docx |
| LaTeX | `.tex`, `.latex` | pylatexenc |
| BibTeX | `.bib` | bibtexparser |

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend development)
- Docker & Docker Compose (optional)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Maicarons/checkpaper.git
cd checkpaper

# 2. Configure environment variables
cp .env.example .env
# Edit .env with your OpenAI API key and settings

# 3. Install backend dependencies
pip install uv
uv sync

# 4. Start the backend server
uvicorn backend.app.main:app --reload --port 9031

# 5. Install and start the frontend
cd frontend
npm install
npm start
```

The application will be available at:
- **Frontend:** http://localhost:9032
- **Backend API:** http://localhost:9031
- **Swagger UI:** http://localhost:9031/docs

### Docker Deployment

```bash
# Start all services
docker-compose up -d

# Production with MySQL
docker-compose --profile production up -d
```

## Project Structure

```
checkpaper/
├── backend/                    # Backend services
│   ├── app/
│   │   ├── api/v1/endpoints/   # API route handlers
│   │   ├── core/               # Configuration, security, DB
│   │   ├── services/           # Business logic
│   │   │   ├── document/       # Document parsing service
│   │   │   ├── validation/     # Validation orchestration
│   │   │   ├── agent/          # AI agent service
│   │   │   └── report/         # Report generation
│   │   ├── schemas/            # Pydantic data models
│   │   ├── prompts/            # LLM prompt templates
│   │   └── main.py             # FastAPI application entry
│   ├── mcp_server/             # MCP tool server
│   │   ├── tools/              # Tool implementations
│   │   └── server.py           # MCP server entry
│   └── tests/                  # Test files
├── frontend/                   # React frontend application
│   └── src/
│       ├── pages/              # Page components
│       ├── components/         # Reusable components
│       ├── services/           # API client
│       └── hooks/              # Custom React hooks
├── docs/                       # VitePress documentation
├── docker-compose.yml          # Docker configuration
├── pyproject.toml              # Python project configuration
└── .env.example                # Environment variable template
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.11+ · FastAPI · SQLModel |
| Frontend | React 18 · TypeScript · Ant Design |
| AI Agent | OpenAI Agents SDK · MCP Protocol |
| Document Parsing | PyMuPDF · python-docx · pylatexenc |
| Reference Verification | Crossref API · Semantic Scholar API |
| Database | SQLite (dev) · MySQL (production) |
| Deployment | Docker · Docker Compose |

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/documents/upload` | POST | Upload a paper document |
| `/api/v1/documents/` | GET | List uploaded documents |
| `/api/v1/documents/{id}` | GET | Get document details |
| `/api/v1/documents/{id}/parse` | POST | Parse document content |
| `/api/v1/validation/start` | POST | Start a validation task |
| `/api/v1/validation/tasks/{id}/results` | GET | Get validation results |
| `/api/v1/validation/types` | GET | List validation types |
| `/api/v1/reports/` | GET | List reports |
| `/api/v1/reports/{id}/download` | GET | Download report (md/pdf/html) |
| `/health` | GET | Health check |

Full API documentation available at `http://localhost:9031/docs` (Swagger UI) when the backend is running.

User documentation (VitePress) is available at `http://localhost:9032/docs/` when the frontend is running.
Start it with: `cd docs && npm install && npm run dev`

## Validation Types

| Type | Description |
|------|-------------|
| `format` | Format and structure checking |
| `figure_table` | Figure and table reference validation |
| `citation` | Citation integrity checking |
| `data_source` | Data source verification |
| `data_processing` | Statistical consistency verification |
| `reference` | Reference authenticity verification |

## Documentation

Full documentation is built with [VitePress](https://vitepress.dev/):

```bash
cd docs
npm install
npm run dev     # Development server
npm run build   # Production build
```

- **English:** [docs/guide/introduction.md](docs/guide/introduction.md)
- **中文:** [docs/zh/guide/introduction.md](docs/zh/guide/introduction.md)

## Configuration

Key environment variables (see [`.env.example`](.env.example) for all options):

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | — |
| `OPENAI_BASE_URL` | API base URL | `http://192.168.56.1:8990` |
| `DATABASE_URL` | Database connection | `sqlite:///./checkpaper.db` |
| `DEBUG` | Debug mode | `false` |
| `SECRET_KEY` | Application secret | `change-me-in-production` |

## Testing

```bash
# Backend tests
pytest

# Backend with coverage
pytest --cov=backend/app --cov-report=html

# Frontend tests
cd frontend && npm test

# Linting
ruff check . && mypy .
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details, or read the [Developer Guide](docs/developer/contributing.md).

## License

This project is licensed under the GNU Affero General Public License v3.0 — see [LICENSE](LICENSE) for details.

## Acknowledgments

Built with [FastAPI](https://fastapi.tiangolo.com/), [OpenAI](https://openai.com/), [PyMuPDF](https://pymupdf.readthedocs.io/), [Ant Design](https://ant.design/), and the [MCP Protocol](https://modelcontextprotocol.io/).

---

[中文文档](README_zh.md)
