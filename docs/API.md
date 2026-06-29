# CheckPaper API 文档

## 概述

CheckPaper API 提供论文验证相关的所有功能，包括文档上传、验证任务管理、报告生成等。

**基础URL**: `http://localhost:8000/api/v1`

**认证方式**: Bearer Token (JWT)

## API 端点

### 1. 文档管理

#### 1.1 上传文档

**POST** `/documents/upload`

上传论文文档进行验证。

**请求**:
- Content-Type: `multipart/form-data`
- Body:
  - `file`: 论文文件 (必填)
  - `document_type`: 文档类型 (可选: pdf, word, latex, bibtex)
  - `title`: 文档标题 (可选)

**响应**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "paper.pdf",
  "file_type": "pdf",
  "file_size": 1024000,
  "upload_time": "2024-01-01T00:00:00",
  "message": "文档上传成功"
}
```

**错误响应**:
- 400: 文件格式不支持
- 413: 文件太大
- 500: 服务器错误

#### 1.2 获取文档列表

**GET** `/documents/`

获取已上传的文档列表。

**查询参数**:
- `page`: 页码 (默认: 1)
- `page_size`: 每页大小 (默认: 20, 最大: 100)
- `status`: 状态过滤 (uploaded, parsing, parsed, failed)
- `document_type`: 文档类型过滤

**响应**:
```json
{
  "documents": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "filename": "paper.pdf",
      "file_type": "pdf",
      "file_size": 1024000,
      "title": "My Paper",
      "status": "parsed",
      "upload_time": "2024-01-01T00:00:00",
      "parsed_time": "2024-01-01T00:01:00"
    }
  ],
  "total": 10,
  "page": 1,
  "page_size": 20
}
```

#### 1.3 获取文档详情

**GET** `/documents/{document_id}`

获取指定文档的详细信息。

**路径参数**:
- `document_id`: 文档ID

**响应**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "paper.pdf",
  "file_type": "pdf",
  "file_size": 1024000,
  "title": "My Paper",
  "status": "parsed",
  "upload_time": "2024-01-01T00:00:00",
  "parsed_time": "2024-01-01T00:01:00"
}
```

#### 1.4 删除文档

**DELETE** `/documents/{document_id}`

删除指定文档。

**路径参数**:
- `document_id`: 文档ID

**响应**:
```json
{
  "message": "文档删除成功"
}
```

#### 1.5 下载文档

**GET** `/documents/{document_id}/download`

下载原始文档。

**路径参数**:
- `document_id`: 文档ID

**响应**: 文件流

#### 1.6 解析文档

**POST** `/documents/{document_id}/parse`

触发文档解析。

**路径参数**:
- `document_id`: 文档ID

**响应**:
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "parsed_content": {
    "title": "Paper Title",
    "abstract": "...",
    "sections": [],
    "figures": [],
    "tables": [],
    "references": [],
    "citations": []
  },
  "message": "文档解析完成"
}
```

### 2. 验证任务

#### 2.1 开始验证

**POST** `/validation/start`

创建新的验证任务。

**请求体**:
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "validation_types": ["format", "citation", "reference"],
  "options": {}
}
```

**响应**:
```json
{
  "task_id": "660e8400-e29b-41d4-a716-446655440000",
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "验证任务已创建，正在后台执行",
  "created_at": "2024-01-01T00:00:00"
}
```

#### 2.2 快速验证

**POST** `/validation/quick`

同步执行验证（适用于小型文档）。

**查询参数**:
- `document_id`: 文档ID (必填)
- `validation_types`: 验证类型列表 (可选)

**响应**: 完整的验证结果

#### 2.3 获取任务列表

**GET** `/validation/tasks`

获取验证任务列表。

**查询参数**:
- `page`: 页码
- `page_size`: 每页大小
- `document_id`: 文档ID过滤
- `status`: 状态过滤

#### 2.4 获取任务详情

**GET** `/validation/tasks/{task_id}`

获取指定任务的详细信息。

#### 2.5 获取验证结果

**GET** `/validation/tasks/{task_id}/results`

获取验证任务的结果。

**响应**:
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
      "summary": "格式检查完成",
      "issues": [
        {
          "id": "issue-1",
          "severity": "warning",
          "category": "格式问题",
          "title": "标题层级不规范",
          "description": "第3节标题编号错误",
          "location": "第3页",
          "suggestion": "检查标题编号连续性"
        }
      ]
    }
  ],
  "created_at": "2024-01-01T00:00:00",
  "completed_at": "2024-01-01T00:05:00"
}
```

#### 2.6 取消任务

**POST** `/validation/tasks/{task_id}/cancel`

取消正在执行的验证任务。

#### 2.7 获取验证类型

**GET** `/validation/types`

获取支持的验证类型列表。

**响应**:
```json
[
  {
    "type": "format",
    "name": "格式检查",
    "description": "检查论文格式、结构、目录对应关系"
  },
  {
    "type": "figure_table",
    "name": "图表引用检查",
    "description": "检查图片、表格是否在文中被显式引用"
  }
]
```

### 3. 报告管理

#### 3.1 获取报告列表

**GET** `/reports/`

获取验证报告列表。

#### 3.2 获取报告详情

**GET** `/reports/{report_id}`

获取指定报告的详细信息，包含完整的 Markdown 内容。

#### 3.3 下载报告

**GET** `/reports/{report_id}/download`

下载报告文件。

**查询参数**:
- `format`: 下载格式 (md, pdf, html)

**响应**: 文件流

#### 3.4 删除报告

**DELETE** `/reports/{report_id}`

删除指定报告。

### 4. 健康检查

#### 4.1 基础健康检查

**GET** `/health/`

**响应**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00",
  "version": "0.1.0"
}
```

#### 4.2 详细健康检查

**GET** `/health/detailed`

**响应**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00",
  "version": "0.1.0",
  "system": {
    "platform": "Linux",
    "python_version": "3.11.0",
    "cpu_count": 8,
    "memory_total_gb": 16.0,
    "memory_available_gb": 8.0,
    "disk_usage_percent": 50.0
  }
}
```

## 错误响应格式

所有错误响应都遵循以下格式：

```json
{
  "error": "error_type",
  "detail": "错误描述",
  "status_code": 400
}
```

常见错误类型：
- `validation_error`: 请求参数验证错误
- `http_error`: HTTP 错误
- `internal_error`: 服务器内部错误

## 验证类型说明

| 类型 | 名称 | 说明 |
|------|------|------|
| `format` | 格式检查 | 检查论文格式、结构、目录对应关系 |
| `figure_table` | 图表引用检查 | 检查图片、表格是否在文中被显式引用 |
| `citation` | 参考文献引用检查 | 检查参考文献是否在文中被引用 |
| `data_source` | 数据来源验证 | 验证论文中数据来源的真实性 |
| `data_processing` | 数据处理验证 | 验证论文数据处理的真实性 |
| `reference` | 参考文献验证 | 验证参考文献的真实性（联网搜索） |

## 问题严重程度

| 级别 | 名称 | 说明 |
|------|------|------|
| `critical` | 严重 | 数据造假、引用造假等严重问题 |
| `warning` | 警告 | 格式问题、引用不完整等 |
| `info` | 信息 | 建议改进的地方 |

## 速率限制

- 上传文件: 10次/分钟
- 创建验证任务: 20次/分钟
- 其他API: 100次/分钟

## 示例代码

### Python

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 上传文档
with open("paper.pdf", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/documents/upload",
        files={"file": f}
    )
    document = response.json()
    print(f"文档ID: {document['id']}")

# 开始验证
response = requests.post(
    f"{BASE_URL}/validation/start",
    json={
        "document_id": document["id"],
        "validation_types": ["format", "citation"]
    }
)
task = response.json()
print(f"任务ID: {task['task_id']}")

# 获取结果
response = requests.get(
    f"{BASE_URL}/validation/tasks/{task['task_id']}/results"
)
results = response.json()
print(f"总问题数: {results['total_issues']}")
```

### cURL

```bash
# 上传文档
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@paper.pdf"

# 开始验证
curl -X POST "http://localhost:8000/api/v1/validation/start" \
  -H "Content-Type: application/json" \
  -d '{"document_id": "DOC_ID", "validation_types": ["format"]}'

# 获取结果
curl "http://localhost:8000/api/v1/validation/tasks/TASK_ID/results"
```
