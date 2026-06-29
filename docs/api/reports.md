# Reports API

## List Reports

Get a paginated list of verification reports.

**GET** `/reports/`

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number |
| `page_size` | integer | 20 | Items per page |
| `document_id` | string | — | Filter by document ID |

### Response

```json
{
  "reports": [
    {
      "id": "report-uuid",
      "document_id": "doc-uuid",
      "title": "Verification Report for paper.pdf",
      "status": "completed",
      "created_at": "2024-01-15T10:35:00Z"
    }
  ],
  "total": 5,
  "page": 1,
  "page_size": 20
}
```

---

## Get Report Details

Get detailed information about a specific report, including full Markdown content.

**GET** `/reports/{report_id}`

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `report_id` | string (UUID) | Report ID |

### Response

```json
{
  "id": "report-uuid",
  "document_id": "doc-uuid",
  "title": "Verification Report for paper.pdf",
  "status": "completed",
  "content": "# Verification Report\n\n...",
  "created_at": "2024-01-15T10:35:00Z"
}
```

---

## Download Report

Download the report file in the specified format.

**GET** `/reports/{report_id}/download`

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `format` | string | `md` | Download format: `md`, `pdf`, `html` |

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `report_id` | string (UUID) | Report ID |

### Response

File stream with appropriate content type:
- `md` → `text/markdown`
- `html` → `text/html`
- `pdf` → `application/pdf`

---

## Delete Report

Delete a specific report.

**DELETE** `/reports/{report_id}`

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `report_id` | string (UUID) | Report ID |

### Response

```json
{
  "message": "Report deleted successfully"
}
```
