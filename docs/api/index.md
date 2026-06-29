# API Reference

CheckPaper provides a RESTful API for all paper verification operations.

## Base URL

```
http://localhost:9031/api/v1
```

## Authentication

The API uses Bearer Token (JWT) authentication. Include the token in the `Authorization` header:

```
Authorization: Bearer <your-token>
```

::: tip Note
For local development with `DEBUG=true`, authentication may be optional depending on configuration.
:::

## API Modules

| Module | Prefix | Description |
|--------|--------|-------------|
| [Documents](/api/documents) | `/documents` | File upload, management, and parsing |
| [Validation](/api/validation) | `/validation` | Verification task management and execution |
| [Reports](/api/reports) | `/reports` | Verification report management and export |
| [Health](/api/health) | `/health` | System health checks |
| [MCP Tools](/api/mcp-tools) | — | Model Context Protocol tool server |

## Request Format

- **Content-Type:** `application/json` for JSON bodies
- **Content-Type:** `multipart/form-data` for file uploads
- **Query Parameters:** for filtering and pagination

## Response Format

### Success Response

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success",
  "data": { ... }
}
```

### Error Response

```json
{
  "error": "error_type",
  "detail": "Error description",
  "status_code": 400
}
```

### Error Types

| Error Type | Status Code | Description |
|------------|-------------|-------------|
| `validation_error` | 422 | Request parameter validation failed |
| `http_error` | 4xx | HTTP client error |
| `internal_error` | 500 | Server internal error |

## Pagination

List endpoints support pagination via query parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number |
| `page_size` | integer | 20 | Items per page (max: 100) |

Paginated response format:

```json
{
  "items": [...],
  "total": 42,
  "page": 1,
  "page_size": 20
}
```

## Rate Limits

| Endpoint Group | Limit |
|----------------|-------|
| File upload | 10 requests/minute |
| Validation creation | 20 requests/minute |
| Other endpoints | 100 requests/minute |

## Interactive Documentation

When the server is running, interactive API documentation is available at:

- **Swagger UI:** `http://localhost:9031/docs`
- **ReDoc:** `http://localhost:9031/redoc`
- **OpenAPI JSON:** `http://localhost:9031/openapi.json`
