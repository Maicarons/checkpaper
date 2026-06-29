# 健康检查 API

## 基础健康检查

返回应用的基本健康状态。

**GET** `/health/`

### 响应

```json
{
  "status": "healthy",
  "timestamp": 1704067200.0,
  "version": "0.1.0"
}
```

---

## 详细健康检查

返回全面的系统信息，包括资源使用情况。

**GET** `/health/detailed`

### 响应

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

## 根路由

返回应用信息。

**GET** `/`

### 响应

```json
{
  "message": "欢迎使用 CheckPaper - AI论文验证智能体系统",
  "version": "0.1.0",
  "docs": "/docs"
}
```

---

## 应用信息

返回应用配置信息。

**GET** `/info`

### 响应

```json
{
  "name": "CheckPaper",
  "version": "0.1.0",
  "debug": true,
  "database": "sqlite"
}
```
