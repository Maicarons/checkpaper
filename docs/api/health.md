# Health Check API

## Basic Health Check

Returns the basic health status of the application.

**GET** `/health/`

### Response

```json
{
  "status": "healthy",
  "timestamp": 1704067200.0,
  "version": "0.1.0"
}
```

---

## Detailed Health Check

Returns comprehensive system information including resource usage.

**GET** `/health/detailed`

### Response

```json
{
  "status": "healthy",
  "timestamp": 1704067200.0,
  "version": "0.1.0",
  "system": {
    "platform": "Linux",
    "python_version": "3.11.7",
    "cpu_count": 8,
    "memory_total_gb": 16.0,
    "memory_available_gb": 8.5,
    "disk_usage_percent": 45.2
  }
}
```

---

## Root Endpoint

Returns application information.

**GET** `/`

### Response

```json
{
  "message": "Welcome to CheckPaper - AI Paper Verification Agent",
  "version": "0.1.0",
  "docs": "/docs"
}
```

---

## Application Info

Returns application configuration information.

**GET** `/info`

### Response

```json
{
  "name": "CheckPaper",
  "version": "0.1.0",
  "debug": true,
  "database": "sqlite"
}
```
