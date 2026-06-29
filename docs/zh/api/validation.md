# 验证任务 API

## 开始验证

创建并启动新的验证任务。

**POST** `/validation/start`

### 请求体

```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "validation_types": ["format", "citation", "reference"],
  "options": {}
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `document_id` | string (UUID) | 是 | 要验证的文档 ID |
| `validation_types` | string[] | 是 | 要执行的验证类型列表 |
| `options` | object | 否 | 附加验证选项 |

### 可用验证类型

| 值 | 说明 |
|------|-------------|
| `format` | 格式和结构检查 |
| `figure_table` | 图表引用检查 |
| `citation` | 引用完整性检查 |
| `data_source` | 数据来源验证 |
| `data_processing` | 数据处理验证 |
| `reference` | 参考文献真实性验证 |

### 响应

```json
{
  "task_id": "660e8400-e29b-41d4-a716-446655440000",
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "验证任务已创建，正在后台执行",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## 快速验证

同步执行验证（适用于小型文档）。

**POST** `/validation/quick`

### 查询参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `document_id` | string (UUID) | 是 | 文档 ID |
| `validation_types` | string | 否 | 逗号分隔的验证类型 |

### 响应

完整的验证结果（格式同[获取验证结果](#获取验证结果)）。

---

## 获取任务列表

获取验证任务的分页列表。

**GET** `/validation/tasks`

### 查询参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `page` | integer | 1 | 页码 |
| `page_size` | integer | 20 | 每页数量 |
| `document_id` | string | — | 按文档 ID 过滤 |
| `status` | string | — | 过滤：`pending`、`running`、`completed`、`failed`、`cancelled` |

### 响应

```json
{
  "tasks": [
    {
      "task_id": "660e8400-e29b-41d4-a716-446655440000",
      "document_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "completed",
      "created_at": "2024-01-15T10:30:00Z",
      "completed_at": "2024-01-15T10:35:00Z"
    }
  ],
  "total": 8,
  "page": 1,
  "page_size": 20
}
```

---

## 获取任务详情

获取指定验证任务的详细信息。

**GET** `/validation/tasks/{task_id}`

### 路径参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `task_id` | string (UUID) | 任务 ID |

---

## 获取验证结果

获取已完成验证任务的详细结果。

**GET** `/validation/tasks/{task_id}/results`

### 响应

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
      "summary": "格式检查完成，发现 2 个问题。",
      "issues": [
        {
          "id": "issue-1",
          "severity": "warning",
          "category": "标题",
          "title": "标题编号不连续",
          "description": "第 3 节标题编号错误",
          "location": "第 3 页",
          "suggestion": "检查标题编号连续性"
        }
      ]
    }
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:35:00Z"
}
```

### 问题结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 唯一问题标识符 |
| `severity` | string | `critical`、`warning` 或 `info` |
| `category` | string | 问题类别（如"标题"、"引用"） |
| `title` | string | 问题简述 |
| `description` | string | 详细描述 |
| `location` | string | 文档中的位置 |
| `suggestion` | string | 建议修复方案 |

---

## 取消任务

取消正在执行的验证任务。

**POST** `/validation/tasks/{task_id}/cancel`

---

## 获取验证类型

获取支持的验证类型列表。

**GET** `/validation/types`

### 响应

```json
[
  {
    "type": "format",
    "name": "格式检查",
    "description": "检查论文格式、结构和目录一致性"
  },
  {
    "type": "figure_table",
    "name": "图表引用检查",
    "description": "检查图表引用的完整性"
  },
  {
    "type": "citation",
    "name": "参考文献引用检查",
    "description": "检查引用与参考文献列表的一致性"
  },
  {
    "type": "data_source",
    "name": "数据来源验证",
    "description": "验证数据来源的真实性"
  },
  {
    "type": "data_processing",
    "name": "数据处理验证",
    "description": "验证数据处理的正确性"
  },
  {
    "type": "reference",
    "name": "参考文献验证",
    "description": "验证参考文献的真实性（联网搜索）"
  }
]
```
