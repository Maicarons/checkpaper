# API 参考

CheckPaper 提供 RESTful API，用于所有论文验证操作。

## 基础 URL

```
http://localhost:9031/api/v1
```

## 认证方式

API 使用 Bearer Token (JWT) 认证。在 `Authorization` 头中包含令牌：

```
Authorization: Bearer <your-token>
```

::: tip 提示
在本地开发模式下（`DEBUG=true`），认证可能是可选的，具体取决于配置。
:::

## API 模块

| 模块 | 前缀 | 说明 |
|------|------|------|
| [文档管理](/zh/api/documents) | `/documents` | 文件上传、管理和解析 |
| [验证任务](/zh/api/validation) | `/validation` | 验证任务管理和执行 |
| [报告管理](/zh/api/reports) | `/reports` | 验证报告管理和导出 |
| [健康检查](/zh/api/health) | `/health` | 系统健康检查 |
| [MCP 工具](/zh/api/mcp-tools) | — | 模型上下文协议工具服务器 |

## 请求格式

- **Content-Type:** `application/json` 用于 JSON 请求体
- **Content-Type:** `multipart/form-data` 用于文件上传
- **查询参数：** 用于过滤和分页

## 响应格式

### 成功响应

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success",
  "data": { ... }
}
```

### 错误响应

```json
{
  "error": "error_type",
  "detail": "错误描述",
  "status_code": 400
}
```

### 错误类型

| 错误类型 | 状态码 | 说明 |
|----------|--------|------|
| `validation_error` | 422 | 请求参数验证失败 |
| `http_error` | 4xx | HTTP 客户端错误 |
| `internal_error` | 500 | 服务器内部错误 |

## 分页

列表端点支持通过查询参数分页：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `page` | integer | 1 | 页码 |
| `page_size` | integer | 20 | 每页数量（最大：100） |

分页响应格式：

```json
{
  "items": [...],
  "total": 42,
  "page": 1,
  "page_size": 20
}
```

## 速率限制

| 端点组 | 限制 |
|--------|------|
| 文件上传 | 10 次/分钟 |
| 验证任务创建 | 20 次/分钟 |
| 其他端点 | 100 次/分钟 |

## 交互式文档

服务运行时，可通过以下地址访问交互式 API 文档：

- **Swagger UI:** `http://localhost:9031/docs`
- **ReDoc:** `http://localhost:9031/redoc`
- **OpenAPI JSON:** `http://localhost:9031/openapi.json`
