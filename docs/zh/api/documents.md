# 文档管理 API

## 上传文档

上传论文文档进行验证。

**POST** `/documents/upload`

### 请求

- **Content-Type:** `multipart/form-data`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | file | 是 | 论文文件（PDF、DOCX、TEX、LATEX） |
| `document_type` | string | 否 | 强制指定文档类型：`pdf`、`word`、`latex`、`bibtex` |
| `title` | string | 否 | 自定义文档标题 |

### 响应

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "paper.pdf",
  "file_type": "pdf",
  "file_size": 1024000,
  "upload_time": "2026-06-30T10:30:00Z",
  "message": "文档上传成功"
}
```

### 错误

| 状态码 | 说明 |
|--------|------|
| 400 | 不支持的文件格式 |
| 413 | 文件超过最大大小（50MB） |
| 500 | 服务器错误 |

---

## 获取文档列表

获取已上传文档的分页列表。

**GET** `/documents/`

### 查询参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `page` | integer | 1 | 页码 |
| `page_size` | integer | 20 | 每页数量（最大：100） |
| `status` | string | — | 过滤：`uploaded`、`parsing`、`parsed`、`failed` |
| `document_type` | string | — | 过滤：`pdf`、`word`、`latex`、`bibtex` |

### 响应

```json
{
  "documents": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "filename": "paper.pdf",
      "file_type": "pdf",
      "file_size": 1024000,
      "title": "我的研究论文",
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

## 获取文档详情

获取指定文档的详细信息。

**GET** `/documents/{document_id}`

### 路径参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `document_id` | string (UUID) | 文档 ID |

### 响应

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "paper.pdf",
  "file_type": "pdf",
  "file_size": 1024000,
  "title": "我的研究论文",
  "status": "parsed",
  "upload_time": "2026-06-30T10:30:00Z",
  "parsed_time": "2026-06-30T10:31:00Z"
}
```

---

## 删除文档

删除指定文档及其关联文件。

**DELETE** `/documents/{document_id}`

### 路径参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `document_id` | string (UUID) | 文档 ID |

### 响应

```json
{
  "message": "文档删除成功"
}
```

---

## 下载文档

下载原始上传的文档。

**GET** `/documents/{document_id}/download`

### 响应

文件流，包含适当的 `Content-Type` 和 `Content-Disposition` 头。

---

## 解析文档

触发文档解析并返回结构化内容。

**POST** `/documents/{document_id}/parse`

### 响应

```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "parsed_content": {
    "title": "论文标题",
    "abstract": "摘要内容...",
    "sections": [
      {
        "heading": "引言",
        "level": 1,
        "content": "..."
      }
    ],
    "figures": [
      {
        "page": 3,
        "index": 0,
        "label": "图 1"
      }
    ],
    "tables": [
      {
        "page": 5,
        "label": "表 1",
        "data": [["表头1", "表头2"], ["数据1", "数据2"]]
      }
    ],
    "references": [
      {
        "id": "ref-1",
        "title": "参考文献标题",
        "authors": ["作者1", "作者2"],
        "year": 2024,
        "journal": "期刊名称"
      }
    ],
    "citations": [
      {
        "text": "[1]",
        "location": "第 2 页，第 3 段"
      }
    ]
  },
  "message": "文档解析完成"
}
```
