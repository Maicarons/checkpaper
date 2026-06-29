# MCP 工具服务器

CheckPaper 包含一个 **模型上下文协议 (MCP)** 服务器，将论文解析和验证工具作为 MCP 兼容端点暴露。这使得系统可以与 AI 智能体和其他 MCP 兼容客户端集成。

## 概述

MCP 服务器作为独立服务运行，通过 stdio 传输协议通信。它提供了文档解析、引用检查、参考文献验证和网页搜索等工具。

## 可用工具

### parse_pdf

解析 PDF 论文并返回结构化数据。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_path` | string | 是 | PDF 文件路径 |

**返回：**
```json
{
  "title": "论文标题",
  "content": "全文内容...",
  "figures": [{"page": 1, "index": 0, "xref": 42}],
  "references": [{"id": "ref-1", "text": "..."}],
  "citations": [{"text": "[1]", "page": 2}],
  "page_count": 15
}
```

---

### parse_docx

解析 Word 文档并返回结构化数据。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_path` | string | 是 | DOCX 文件路径 |

**返回：**
```json
{
  "title": "论文标题",
  "content": "全文内容...",
  "tables": [[["表头1", "表头2"], ["数据1", "数据2"]]],
  "paragraph_count": 120
}
```

---

### parse_latex

解析 LaTeX 文档并返回结构化数据。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_path` | string | 是 | TEX 文件路径 |

**返回：**
```json
{
  "title": "论文标题",
  "content": "全文内容...",
  "sections": [{"heading": "引言", "level": 1}],
  "references": [{"key": "author2024", "text": "..."}],
  "citations": [{"text": "\\cite{author2024}"}]
}
```

---

### check_citations

检查文档中的引用完整性。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `document_content` | string | 是 | 文档全文 |
| `references` | string | 是 | 参考文献列表文本 |

**返回：**
```json
{
  "total_citations": 25,
  "matched": 23,
  "unmatched": ["[30]", "[31]"],
  "unused_references": ["ref-key-15"],
  "issues": [
    {
      "severity": "warning",
      "description": "引用 [30] 在参考文献列表中未找到"
    }
  ]
}
```

---

### verify_references

通过外部数据库验证参考文献。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `references` | string | 是 | 参考文献列表文本 |

**返回：**
```json
{
  "verified": 20,
  "suspicious": 2,
  "not_found": 1,
  "results": [
    {
      "reference": "...",
      "status": "verified",
      "doi": "10.1234/example",
      "source": "crossref"
    }
  ]
}
```

---

### check_figures

检查文档中的图表引用。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `document_content` | string | 是 | 文档全文 |

**返回：**
```json
{
  "defined_figures": 5,
  "defined_tables": 3,
  "cited_figures": 4,
  "cited_tables": 3,
  "uncited": ["Figure 5"],
  "orphan_references": [],
  "issues": [
    {
      "severity": "warning",
      "description": "Figure 5 已定义但正文中从未引用"
    }
  ]
}
```

---

### check_format

检查论文格式合规性。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `document_content` | string | 是 | 文档全文 |

---

### web_search_reference

在线搜索参考文献以验证其存在性。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | 是 | 搜索查询（如论文标题+作者） |

## 启动 MCP 服务器

### 独立运行

```bash
python -c "from backend.mcp_server.server import main; main()"
```

### 通过 Docker Compose

MCP 服务器作为 Docker Compose 栈的一部分自动运行：

```bash
docker-compose up mcp-server
```

### 配置

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `MCP_SERVER_HOST` | `0.0.0.0` | 服务器绑定地址 |
| `MCP_SERVER_PORT` | `8001` | 服务器端口 |

## 与 AI 智能体集成

MCP 服务器设计为与 OpenAI Agents SDK 和其他 MCP 兼容的智能体框架配合使用。Agent 服务通过 MCP 协议连接到工具服务器，在验证工作流中执行文档解析和验证工具。

```
Agent 服务 → MCP 协议 → 工具服务器
                  ↓
    parse_pdf / check_citations / verify_references / ...
```
