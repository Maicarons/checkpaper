# Validation API

## Start Validation

Create and start a new validation task.

**POST** `/validation/start`

### Request Body

```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "validation_types": ["format", "citation", "reference"],
  "options": {}
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `document_id` | string (UUID) | Yes | ID of the document to validate |
| `validation_types` | string[] | Yes | Validation types to run |
| `options` | object | No | Additional validation options |

### Available Validation Types

| Value | Description |
|-------|-------------|
| `format` | Format and structure checking |
| `figure_table` | Figure and table reference checking |
| `citation` | Citation integrity checking |
| `data_source` | Data source verification |
| `data_processing` | Data processing verification |
| `reference` | Reference authenticity verification |

### Response

```json
{
  "task_id": "660e8400-e29b-41d4-a716-446655440000",
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Validation task created, executing in background",
  "created_at": "2026-06-30T10:30:00Z"
}
```

---

## Quick Validation

Synchronously execute validation (suitable for small documents).

**POST** `/validation/quick`

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `document_id` | string (UUID) | Yes | Document ID |
| `validation_types` | string | No | Comma-separated validation types |

### Response

Complete validation results (same format as [Get Validation Results](#get-validation-results)).

---

## List Validation Tasks

Get a paginated list of validation tasks.

**GET** `/validation/tasks`

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number |
| `page_size` | integer | 20 | Items per page |
| `document_id` | string | — | Filter by document ID |
| `status` | string | — | Filter: `pending`, `running`, `completed`, `failed`, `cancelled` |

### Response

```json
{
  "tasks": [
    {
      "task_id": "660e8400-e29b-41d4-a716-446655440000",
      "document_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "completed",
      "created_at": "2026-06-30T10:30:00Z",
      "completed_at": "2026-06-30T10:35:00Z"
    }
  ],
  "total": 8,
  "page": 1,
  "page_size": 20
}
```

---

## Get Task Details

Get details of a specific validation task.

**GET** `/validation/tasks/{task_id}`

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `task_id` | string (UUID) | Task ID |

### Response

```json
{
  "task_id": "660e8400-e29b-41d4-a716-446655440000",
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "message": "Validation completed",
  "created_at": "2026-06-30T10:30:00Z",
  "started_at": "2026-06-30T10:30:01Z",
  "completed_at": "2026-06-30T10:35:00Z"
}
```

---

## Get Validation Results

Get the detailed results of a completed validation task.

**GET** `/validation/tasks/{task_id}/results`

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `task_id` | string (UUID) | Task ID |

### Response

```json
{
  "task_id": "660e8400-e29b-41d4-a716-446655440000",
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "total_issues": 5,
  "critical_issues": 1,
  "warning_issues": 3,
  "info_issues": 1,
  "results": [
    {
      "id": "result-1",
      "validation_type": "format",
      "status": "completed",
      "issues_count": 2,
      "critical_count": 0,
      "warning_count": 2,
      "info_count": 0,
      "summary": "Format check completed. Found 2 issues.",
      "issues": [
        {
          "id": "issue-1",
          "severity": "warning",
          "category": "Heading",
          "title": "Non-sequential heading numbers",
          "description": "Section 3 heading number is incorrect",
          "location": "Page 3",
          "suggestion": "Check heading numbering continuity"
        }
      ]
    }
  ],
  "created_at": "2026-06-30T10:30:00Z",
  "completed_at": "2026-06-30T10:35:00Z"
}
```

### Issue Structure

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique issue identifier |
| `severity` | string | `critical`, `warning`, or `info` |
| `category` | string | Issue category (e.g., "Heading", "Citation") |
| `title` | string | Short issue title |
| `description` | string | Detailed description |
| `location` | string | Location in the document |
| `suggestion` | string | Recommended fix |

---

## Cancel Task

Cancel a running validation task.

**POST** `/validation/tasks/{task_id}/cancel`

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `task_id` | string (UUID) | Task ID |

### Response

```json
{
  "message": "Task cancelled successfully"
}
```

---

## Get Validation Types

Get the list of supported validation types.

**GET** `/validation/types`

### Response

```json
[
  {
    "type": "format",
    "name": "Format Check",
    "description": "Check paper format, structure, and TOC consistency"
  },
  {
    "type": "figure_table",
    "name": "Figure & Table Check",
    "description": "Check figure and table reference completeness"
  },
  {
    "type": "citation",
    "name": "Citation Check",
    "description": "Check citation consistency with reference list"
  },
  {
    "type": "data_source",
    "name": "Data Source Verification",
    "description": "Verify data source authenticity"
  },
  {
    "type": "data_processing",
    "name": "Data Processing Verification",
    "description": "Verify data processing correctness"
  },
  {
    "type": "reference",
    "name": "Reference Verification",
    "description": "Verify reference authenticity (online search)"
  }
]
```
