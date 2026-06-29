# Introduction

**CheckPaper** is an AI-powered academic paper verification agent system. It automatically detects various issues in academic papers — including formatting non-compliance, citation errors, reference fraud, and data integrity problems — helping researchers improve the quality and reliability of their work.

## Why CheckPaper?

Academic papers undergo rigorous review processes, but common issues often slip through:

- **Formatting inconsistencies** — heading hierarchy errors, missing figure/table references, inconsistent numbering
- **Citation problems** — in-text citations that don't match the reference list, duplicate or missing references
- **Reference fraud** — fabricated DOIs, non-existent papers, predatory journal citations
- **Data integrity concerns** — inconsistent statistics, unverifiable data sources, suspicious p-values

CheckPaper addresses all of these challenges through AI-driven analysis combined with academic database verification.

## Core Architecture

```
┌─────────────────────────────────────────────────────┐
│                  React Frontend                      │
│         (Upload · Validation · Reports · History)    │
└─────────────────────┬───────────────────────────────┘
                      │ HTTP API
┌─────────────────────▼───────────────────────────────┐
│               FastAPI Backend                        │
│  ┌──────────┐ ┌────────────┐ ┌──────────────────┐  │
│  │ Document  │ │ Validation │ │ Report Generator │  │
│  │ Service   │ │ Service    │ │                  │  │
│  └─────┬────┘ └─────┬──────┘ └──────────────────┘  │
│        │             │                               │
│  ┌─────▼─────────────▼──────┐                       │
│  │    Agent Service          │                       │
│  │  (OpenAI Agents SDK)     │                       │
│  └─────────────┬────────────┘                       │
│                │ MCP Protocol                        │
│  ┌─────────────▼────────────┐                       │
│  │    MCP Tool Server        │                       │
│  │  parse · check · verify   │                       │
│  └──────────────────────────┘                       │
└─────────────────────────────────────────────────────┘
```

## Key Technologies

| Component | Technology |
|-----------|------------|
| Backend | Python 3.11+ · FastAPI · SQLModel |
| Frontend | React 18 · TypeScript · Ant Design |
| AI Agent | OpenAI Agents SDK · MCP Protocol |
| Document Parsing | PyMuPDF · python-docx · pylatexenc |
| Reference Verification | Crossref API · Semantic Scholar API |
| Database | SQLite (dev) · MySQL (production) |
| Deployment | Docker · Docker Compose |

## Supported File Formats

| Format | Extension | Parser |
|--------|-----------|--------|
| PDF | `.pdf` | PyMuPDF |
| Word | `.docx`, `.doc` | python-docx |
| LaTeX | `.tex`, `.latex` | pylatexenc |
| BibTeX | `.bib` | bibtexparser |

## Validation Types

CheckPaper supports **6 core validation types**:

| Type | Description |
|------|-------------|
| **Format** | Heading hierarchy, numbering, layout, TOC consistency |
| **Figure & Table** | Figure/table citation completeness and accuracy |
| **Citation** | In-text citation vs reference list consistency |
| **Data Source** | Data source verification and accessibility |
| **Data Processing** | Statistical method validation, p-value checks |
| **Reference** | DOI verification, metadata matching, fraud detection |

## Next Steps

- [Quick Start](/guide/getting-started) — Install and run CheckPaper in minutes
- [Features](/guide/features) — Deep dive into each validation capability
- [Deployment](/guide/deployment) — Production deployment with Docker
