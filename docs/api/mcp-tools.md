# MCP Tool Server

CheckPaper includes a **Model Context Protocol (MCP)** server that exposes paper parsing and validation tools as MCP-compliant endpoints. This enables integration with AI agents and other MCP-compatible clients.

## Overview

The MCP server runs as a separate service and communicates via stdio transport. It provides tools for document parsing, citation checking, reference verification, and web search.

## Available Tools

### parse_pdf

Parse a PDF paper and return structured data.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_path` | string | Yes | Path to the PDF file |

**Returns:**
```json
{
  "title": "Paper Title",
  "content": "Full text content...",
  "figures": [{"page": 1, "index": 0, "xref": 42}],
  "references": [{"id": "ref-1", "text": "..."}],
  "citations": [{"text": "[1]", "page": 2}],
  "page_count": 15
}
```

---

### parse_docx

Parse a Word document and return structured data.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_path` | string | Yes | Path to the DOCX file |

**Returns:**
```json
{
  "title": "Paper Title",
  "content": "Full text content...",
  "tables": [[["Header1", "Header2"], ["Data1", "Data2"]]],
  "paragraph_count": 120
}
```

---

### parse_latex

Parse a LaTeX document and return structured data.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_path` | string | Yes | Path to the TEX file |

**Returns:**
```json
{
  "title": "Paper Title",
  "content": "Full text content...",
  "sections": [{"heading": "Introduction", "level": 1}],
  "references": [{"key": "author2024", "text": "..."}],
  "citations": [{"text": "\\cite{author2024}"}]
}
```

---

### check_citations

Check citation integrity in a document.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `document_content` | string | Yes | Full document text |
| `references` | string | Yes | Reference list text |

**Returns:**
```json
{
  "total_citations": 25,
  "matched": 23,
  "unmatched": ["[30]", "[31]"],
  "unused_references": ["ref-key-15"],
  "issues": [
    {
      "severity": "warning",
      "description": "Citation [30] not found in reference list"
    }
  ]
}
```

---

### verify_references

Verify references against external databases.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `references` | string | Yes | Reference list text |

**Returns:**
```json
{
  "verified": 20,
  "suspicious": 2,
  "not_found": 1,
  "results": [
    {
      "reference": "...",
      "status": "verified",
      "doi": "10.1234/example",
      "source": "crossref"
    }
  ]
}
```

---

### check_figures

Check figure and table references in a document.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `document_content` | string | Yes | Full document text |

**Returns:**
```json
{
  "defined_figures": 5,
  "defined_tables": 3,
  "cited_figures": 4,
  "cited_tables": 3,
  "uncited": ["Figure 5"],
  "orphan_references": [],
  "issues": [
    {
      "severity": "warning",
      "description": "Figure 5 is defined but never referenced in the text"
    }
  ]
}
```

---

### check_format

Check paper formatting compliance.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `document_content` | string | Yes | Full document text |

**Returns:**
```json
{
  "issues": [
    {
      "severity": "warning",
      "category": "Heading",
      "description": "Heading level inconsistency detected"
    }
  ]
}
```

---

### web_search_reference

Search for a reference online to verify its existence.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Search query (e.g., paper title + authors) |

**Returns:**
```json
{
  "found": true,
  "results": [
    {
      "title": "Paper Title",
      "url": "https://doi.org/10.1234/example",
      "source": "crossref"
    }
  ]
}
```

## Starting the MCP Server

### Standalone

```bash
python -c "from backend.mcp_server.server import main; main()"
```

### Via Docker Compose

The MCP server runs automatically as part of the Docker Compose stack:

```bash
docker-compose up mcp-server
```

### Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `MCP_SERVER_HOST` | `0.0.0.0` | Server bind address |
| `MCP_SERVER_PORT` | `8001` | Server port |

## Integration with AI Agents

The MCP server is designed to work with the OpenAI Agents SDK and other MCP-compatible agent frameworks. The Agent Service connects to the MCP server to execute document parsing and validation tools during the verification workflow.

```
Agent Service → MCP Protocol → Tool Server
                  ↓
    parse_pdf / check_citations / verify_references / ...
```
