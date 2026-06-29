# 系统架构

本文档描述 CheckPaper 的高层架构设计。

## 概述

CheckPaper 采用**分层架构**，在 API 层、业务逻辑服务和数据访问层之间有清晰的分离。系统通过 MCP 协议集成 AI 智能体，实现智能论文验证。

## 高层架构

```
┌──────────────────────────────────────────────────────────┐
│                       客户端层                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Web 浏览器  │  │   REST 客户端 │  │   MCP 客户端  │   │
│  │   (React UI)  │  │  (curl 等)   │  │  (AI 智能体)  │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
└─────────┼─────────────────┼─────────────────┼────────────┘
          │                 │                 │
┌─────────▼─────────────────▼─────────────────▼────────────┐
│                       API 层                              │
│  ┌──────────┐ ┌────────────┐ ┌──────────┐ ┌──────────┐  │
│  │  文档     │ │  验证      │ │  报告    │ │  健康    │  │
│  │  端点     │ │  端点      │ │  端点    │ │  检查    │  │
│  └─────┬────┘ └─────┬──────┘ └─────┬────┘ └──────────┘  │
└────────┼────────────┼──────────────┼─────────────────────┘
         │            │              │
┌────────▼────────────▼──────────────▼─────────────────────┐
│                     服务层                                │
│  ┌────────────┐ ┌────────────┐ ┌────────────────────┐   │
│  │  文档服务   │ │  验证服务   │ │  报告服务           │   │
│  └─────┬──────┘ └─────┬──────┘ └────────┬───────────┘   │
│        │               │                 │                │
│        │        ┌──────▼──────┐          │                │
│        │        │  Agent 服务  │          │                │
│        │        └──────┬──────┘          │                │
└────────┼───────────────┼─────────────────┼───────────────┘
         │               │                 │
┌────────▼───────────────▼─────────────────▼───────────────┐
│                    基础设施层                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐  │
│  │  数据库   │ │  文件     │ │  OpenAI  │ │ MCP 服务器  │  │
│  │(SQLite/  │ │  存储     │ │  API     │ │  (工具)     │  │
│  │ MySQL)   │ │          │ │          │ │            │  │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘  │
└──────────────────────────────────────────────────────────┘
```

## 组件详解

### API 层 (`backend/app/api/`)

API 层处理 HTTP 请求/响应：

```
api/
├── v1/
│   ├── __init__.py          # 路由聚合
│   └── endpoints/
│       ├── documents.py     # 文档 CRUD + 上传/下载
│       ├── validation.py    # 验证任务管理
│       ├── reports.py       # 报告管理
│       └── health.py        # 健康检查端点
├── deps.py                  # 依赖注入
```

**核心模式：**
- 版本化 API 路由（`/api/v1/`）
- 通过 FastAPI `Depends()` 实现依赖注入
- 自动 OpenAPI Schema 生成
- 全局异常处理器实现一致的错误响应

### 服务层 (`backend/app/services/`)

服务层包含核心业务逻辑：

| 服务 | 职责 |
|------|------|
| `DocumentService` | 文件存储、文档 CRUD、解析编排 |
| `ValidationService` | 任务创建、状态跟踪、结果聚合 |
| `AgentService` | AI 驱动的验证、提示词管理、OpenAI 集成 |
| `ReportService` | 报告生成、模板渲染、导出（MD/HTML/PDF） |

### Agent 服务（AI 核心）

Agent 服务是执行验证的智能层：

```
AgentService
├── run_validation()          # 主入口 - 分发到类型特定的验证器
├── _validate_format()        # 通过 LLM 分析进行格式检查
├── _validate_figure_table()  # 图表引用验证
├── _validate_citation()      # 引用完整性检查
├── _validate_data_source()   # 数据来源验证
├── _validate_data_processing() # 统计一致性测试
└── _validate_reference()     # 通过 API 验证参考文献真实性
```

**流程：**
1. 接收文档内容和验证类型
2. 为每种类型构建专门的提示词
3. 发送到 OpenAI API（或本地模型）
4. 将 LLM 响应解析为结构化问题
5. 返回聚合结果

### MCP 服务器 (`backend/mcp_server/`)

MCP 服务器通过模型上下文协议提供工具：

| 工具 | 用途 |
|------|------|
| `parse_pdf` | 从 PDF 提取结构化数据 |
| `parse_docx` | 从 Word 提取结构化数据 |
| `parse_latex` | 从 LaTeX 提取结构化数据 |
| `check_citations` | 验证引用完整性 |
| `verify_references` | 通过 API 交叉验证参考文献 |
| `check_figures` | 验证图表引用 |
| `check_format` | 检查格式合规性 |
| `web_search_reference` | 在线搜索参考文献 |

### Schema 层 (`backend/app/schemas/`)

Pydantic 模型定义数据契约：

| 模块 | 说明 |
|------|------|
| `document.py` | Document、DocumentTypeEnum、ParsedContent |
| `validation.py` | ValidationTask、ValidationTypeEnum、Issues |
| `report.py` | Report、ReportStatus |

## 数据流

### 文档上传和验证流程

```
1. 客户端上传文档
   ↓
2. DocumentService 存储文件 + 创建数据库记录
   ↓
3. 客户端启动验证（选择验证类型）
   ↓
4. ValidationService 创建任务（状态：pending）
   ↓
5. AgentService.run_validation() 被调用
   ↓
6. 对每种验证类型：
   a. 构建专门的提示词
   b. 调用 OpenAI API
   c. 将响应解析为问题列表
   ↓
7. ValidationService 聚合结果
   ↓
8. ReportService 生成 Markdown 报告
   ↓
9. 客户端轮询任务状态 → 接收完成的结果
```

## 数据库表

| 表名 | 说明 |
|------|------|
| `document` | 已上传文档及元数据 |
| `validationtask` | 验证任务记录及状态 |
| `validationresult` | 每种类型的验证结果 |
| `validationissue` | 验证中发现的具体问题 |
| `report` | 生成的验证报告 |

### 关键关系

```
Document 1──N ValidationTask
ValidationTask 1──N ValidationResult
ValidationResult 1──N ValidationIssue
Document 1──N Report
```

## 技术栈总结

| 层级 | 技术 | 用途 |
|------|------|------|
| 前端 | React + TypeScript + Ant Design | 用户界面 |
| API | FastAPI + Pydantic | REST API |
| 服务 | Python 业务逻辑 | 核心验证 |
| AI | OpenAI API + Agents SDK | 智能分析 |
| 工具 | MCP 协议 | 标准化工具访问 |
| 数据库 | SQLModel + SQLite/MySQL | 数据持久化 |
| 部署 | Docker + Docker Compose | 容器化部署 |
