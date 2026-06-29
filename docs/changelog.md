# Changelog

All notable changes to CheckPaper will be documented in this file.

## [0.1.0] - 2026-06-30

### Added

- **Document Parsing**
  - PDF parsing via PyMuPDF
  - Word (.docx) parsing via python-docx
  - LaTeX parsing via pylatexenc
  - Automatic format detection and structured extraction

- **Validation Features**
  - Format and structure checking (headings, numbering, layout)
  - Figure and table reference validation
  - Citation integrity checking
  - Data source verification
  - Data processing verification (GRIM/SPRITE tests)
  - Reference authenticity verification (Crossref, Semantic Scholar)

- **MCP Tool Server**
  - 8 MCP tools: parse_pdf, parse_docx, parse_latex, check_citations, verify_references, check_figures, check_format, web_search_reference
  - Stdio transport protocol
  - OpenAI Agents SDK integration

- **API**
  - RESTful API with FastAPI
  - Document upload, management, and download
  - Validation task management (create, poll, cancel)
  - Report generation and export (MD, HTML, PDF)
  - Health check endpoints
  - Swagger UI and ReDoc documentation

- **Frontend**
  - React 18 + TypeScript + Ant Design
  - Home page with feature overview
  - Paper upload with drag-and-drop
  - Validation type selection
  - Real-time validation progress tracking
  - Verification report viewer with Markdown rendering
  - Validation history management

- **Infrastructure**
  - Docker Compose deployment (backend, frontend, MCP server, MySQL)
  - SQLite for development, MySQL for production
  - Environment-based configuration via pydantic-settings
  - CORS support, request timing middleware
  - Global exception handling
