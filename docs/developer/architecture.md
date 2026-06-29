# System Architecture

This document describes the high-level architecture of CheckPaper.

## Overview

CheckPaper follows a **layered architecture** with clear separation between the API layer, business logic services, and data access. The system integrates AI agents via the MCP protocol for intelligent paper verification.

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     Client Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Web Browser  │  │  REST Client │  │  MCP Client  │   │
│  │  (React UI)   │  │  (curl/etc)  │  │  (AI Agent)  │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
└─────────┼─────────────────┼─────────────────┼────────────┘
          │                 │                 │
┌─────────▼─────────────────▼─────────────────▼────────────┐
│                    API Layer                              │
│  ┌──────────┐ ┌────────────┐ ┌──────────┐ ┌──────────┐  │
│  │Documents │ │ Validation │ │ Reports  │ │ Health   │  │
│  │Endpoint  │ │ Endpoint   │ │ Endpoint │ │ Endpoint │  │
│  └─────┬────┘ └─────┬──────┘ └─────┬────┘ └──────────┘  │
└────────┼────────────┼──────────────┼─────────────────────┘
         │            │              │
┌────────▼────────────▼──────────────▼─────────────────────┐
│                  Service Layer                            │
│  ┌────────────┐ ┌────────────┐ ┌────────────────────┐   │
│  │ Document   │ │ Validation │ │ Report             │   │
│  │ Service    │ │ Service    │ │ Service            │   │
│  └─────┬──────┘ └─────┬──────┘ └────────┬───────────┘   │
│        │               │                 │                │
│        │        ┌──────▼──────┐          │                │
│        │        │ Agent       │          │                │
│        │        │ Service     │          │                │
│        │        └──────┬──────┘          │                │
└────────┼───────────────┼─────────────────┼───────────────┘
         │               │                 │
┌────────▼───────────────▼─────────────────▼───────────────┐
│                  Infrastructure Layer                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐  │
│  │ Database │ │ File     │ │ OpenAI   │ │ MCP Server │  │
│  │ (SQLite/ │ │ Storage  │ │ API      │ │ (Tools)    │  │
│  │  MySQL)  │ │          │ │          │ │            │  │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘  │
└──────────────────────────────────────────────────────────┘
```

## Component Details

### API Layer (`backend/app/api/`)

The API layer handles HTTP request/response processing:

```
api/
├── v1/
│   ├── __init__.py          # Router aggregation
│   └── endpoints/
│       ├── documents.py     # Document CRUD + upload/download
│       ├── validation.py    # Validation task management
│       ├── reports.py       # Report management
│       └── health.py        # Health check endpoints
├── deps.py                  # Dependency injection
```

**Key patterns:**
- Versioned API routes (`/api/v1/`)
- Dependency injection via FastAPI `Depends()`
- Automatic OpenAPI schema generation
- Global exception handlers for consistent error responses

### Service Layer (`backend/app/services/`)

Services contain the core business logic:

```
services/
├── __init__.py              # Service registry
├── document/
│   └── __init__.py          # DocumentService - file management, parsing
├── validation/
│   └── __init__.py          # ValidationService - task lifecycle
├── agent/
│   └── __init__.py          # AgentService - AI verification logic
└── report/
    └── __init__.py          # ReportService - report generation
```

**Service responsibilities:**

| Service | Responsibility |
|---------|---------------|
| `DocumentService` | File storage, document CRUD, parsing orchestration |
| `ValidationService` | Task creation, status tracking, result aggregation |
| `AgentService` | AI-powered verification, prompt management, OpenAI integration |
| `ReportService` | Report generation, template rendering, export (MD/HTML/PDF) |

### Agent Service (AI Core)

The Agent Service is the intelligence layer that performs verification:

```
AgentService
├── run_validation()          # Main entry - dispatches to type-specific validators
├── _validate_format()        # Format checking via LLM analysis
├── _validate_figure_table()  # Figure/table reference validation
├── _validate_citation()      # Citation integrity checking
├── _validate_data_source()   # Data source verification
├── _validate_data_processing() # Statistical consistency testing
└── _validate_reference()     # Reference authenticity via API
```

**Flow:**
1. Receives document content and validation types
2. For each type, constructs a specialized prompt
3. Sends prompt to OpenAI API (or local model)
4. Parses LLM response into structured issues
5. Returns aggregated results

### MCP Server (`backend/mcp_server/`)

The MCP server provides tools via the Model Context Protocol:

```
mcp_server/
├── server.py                # MCP server setup and tool registration
├── __main__.py              # Entry point
└── tools/
    └── __init__.py          # Tool implementations
```

**Tools exposed:**

| Tool | Purpose |
|------|---------|
| `parse_pdf` | Extract structured data from PDF |
| `parse_docx` | Extract structured data from Word |
| `parse_latex` | Extract structured data from LaTeX |
| `check_citations` | Verify citation completeness |
| `verify_references` | Cross-check references via APIs |
| `check_figures` | Validate figure/table references |
| `check_format` | Check formatting compliance |
| `web_search_reference` | Search for references online |

### Schema Layer (`backend/app/schemas/`)

Pydantic models define data contracts:

```
schemas/
├── __init__.py              # Model exports
├── document.py              # Document, DocumentTypeEnum, ParsedContent
├── validation.py            # ValidationTask, ValidationTypeEnum, Issues
└── report.py                # Report, ReportStatus
```

### Configuration (`backend/app/core/`)

Centralized configuration using pydantic-settings:

```
core/
├── config.py                # Settings class (reads .env)
├── db.py                    # Database initialization and session management
└── security.py              # JWT authentication
```

## Data Flow

### Document Upload and Validation Flow

```
1. Client uploads document
   ↓
2. DocumentService stores file + creates DB record
   ↓
3. Client starts validation with selected types
   ↓
4. ValidationService creates task (status: pending)
   ↓
5. AgentService.run_validation() is called
   ↓
6. For each validation type:
   a. Construct specialized prompt
   b. Call OpenAI API
   c. Parse response into issues
   ↓
7. ValidationService aggregates results
   ↓
8. ReportService generates Markdown report
   ↓
9. Client polls task status → receives completed results
```

### MCP Tool Invocation Flow

```
1. Agent needs to parse a document
   ↓
2. Agent sends MCP tool call via protocol
   ↓
3. MCP Server receives call
   ↓
4. Tool implementation executes:
   - parse_pdf: uses PyMuPDF
   - parse_docx: uses python-docx
   - parse_latex: uses pylatexenc
   ↓
5. Results returned to Agent via MCP
   ↓
6. Agent incorporates results into verification
```

## Database Schema

### Tables

| Table | Description |
|-------|-------------|
| `document` | Uploaded documents with metadata |
| `validationtask` | Validation task records with status |
| `validationresult` | Individual validation results per type |
| `validationissue` | Specific issues found during validation |
| `report` | Generated verification reports |

### Key Relationships

```
Document 1──N ValidationTask
ValidationTask 1──N ValidationResult
ValidationResult 1──N ValidationIssue
Document 1──N Report
```

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | React + TypeScript + Ant Design | User interface |
| API | FastAPI + Pydantic | REST API |
| Services | Python business logic | Core verification |
| AI | OpenAI API + Agents SDK | Intelligent analysis |
| Tools | MCP Protocol | Standardized tool access |
| Database | SQLModel + SQLite/MySQL | Data persistence |
| Deployment | Docker + Docker Compose | Containerized deployment |
