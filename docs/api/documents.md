# Document Management API

## Upload Document

Upload a paper document for verification.

**POST** `/documents/upload`

### Request

- **Content-Type:** `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | file | Yes | Paper file (PDF, DOCX, TEX, LATEX) |
| `document_type` | string | No | Force document type: `pdf`, `word`, `latex`, `bibtex` |
| `title` | string | No | Custom document title |

### Response

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "paper.pdf",
  "file_type": "pdf",
  "file_size": 1024000,
  "upload_time": "2026-06-30T10:30:00Z",
  "message": "Document uploaded successfully"
}
```

### Errors

| Code | Description |
|------|-------------|
| 400 | Unsupported file format |
| 413 | File exceeds maximum size (50MB) |
| 500 | Server error |

---

## List Documents

Get a paginated list of uploaded documents.

**GET** `/documents/`

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number |
| `page_size` | integer | 20 | Items per page (max: 100) |
| `status` | string | — | Filter: `uploaded`, `parsing`, `parsed`, `failed` |
| `document_type` | string | — | Filter: `pdf`, `word`, `latex`, `bibtex` |

### Response

```json
{
  "documents": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "filename": "paper.pdf",
      "file_type": "pdf",
      "file_size": 1024000,
      "title": "My Research Paper",
      "status": "parsed",
      "upload_time": "2026-06-30T10:30:00Z",
      "parsed_time": "2026-06-30T10:31:00Z"
    }
  ],
  "total": 15,
  "page": 1,
  "page_size": 20
}
```

---

## Get Document Details

Get detailed information about a specific document.

**GET** `/documents/{document_id}`

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | string (UUID) | Document ID |

### Response

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "paper.pdf",
  "file_type": "pdf",
  "file_size": 1024000,
  "title": "My Research Paper",
  "status": "parsed",
  "upload_time": "2026-06-30T10:30:00Z",
  "parsed_time": "2026-06-30T10:31:00Z"
}
```

---

## Delete Document

Delete a document and its associated file.

**DELETE** `/documents/{document_id}`

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | string (UUID) | Document ID |

### Response

```json
{
  "message": "Document deleted successfully"
}
```

---

## Download Document

Download the original uploaded document.

**GET** `/documents/{document_id}/download`

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | string (UUID) | Document ID |

### Response

File stream with appropriate `Content-Type` and `Content-Disposition` headers.

---

## Parse Document

Trigger document parsing and return structured content.

**POST** `/documents/{document_id}/parse`

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | string (UUID) | Document ID |

### Response

```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "parsed_content": {
    "title": "Paper Title",
    "abstract": "...",
    "sections": [
      {
        "heading": "Introduction",
        "level": 1,
        "content": "..."
      }
    ],
    "figures": [
      {
        "page": 3,
        "index": 0,
        "label": "Figure 1"
      }
    ],
    "tables": [
      {
        "page": 5,
        "label": "Table 1",
        "data": [["Header 1", "Header 2"], ["Row 1", "Row 2"]]
      }
    ],
    "references": [
      {
        "id": "ref-1",
        "title": "Reference Title",
        "authors": ["Author 1", "Author 2"],
        "year": 2024,
        "journal": "Journal Name"
      }
    ],
    "citations": [
      {
        "text": "[1]",
        "location": "page 2, paragraph 3"
      }
    ]
  },
  "message": "Document parsed successfully"
}
```
