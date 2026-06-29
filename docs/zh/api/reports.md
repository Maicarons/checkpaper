# 报告管理 API

## 获取报告列表

获取验证报告的分页列表。

**GET** `/reports/`

### 查询参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `page` | integer | 1 | 页码 |
| `page_size` | integer | 20 | 每页数量 |
| `document_id` | string | — | 按文档 ID 过滤 |

### 响应

```json
{
  "reports": [
    {
      "id": "report-uuid",
      "document_id": "doc-uuid",
      "title": "paper.pdf 验证报告",
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

## 获取报告详情

获取指定报告的详细信息，包含完整的 Markdown 内容。

**GET** `/reports/{report_id}`

### 路径参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `report_id` | string (UUID) | 报告 ID |

### 响应

```json
{
  "id": "report-uuid",
  "document_id": "doc-uuid",
  "title": "paper.pdf 验证报告",
  "status": "completed",
  "content": "# 验证报告\n\n...",
  "created_at": "2024-01-15T10:35:00Z"
}
```

---

## 下载报告

下载指定格式的报告文件。

**GET** `/reports/{report_id}/download`

### 查询参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `format` | string | `md` | 下载格式：`md`、`pdf`、`html` |

### 响应

文件流，包含适当的内容类型：
- `md` → `text/markdown`
- `html` → `text/html`
- `pdf` → `application/pdf`

---

## 删除报告

删除指定报告。

**DELETE** `/reports/{report_id}`

### 响应

```json
{
  "message": "报告删除成功"
}
```
