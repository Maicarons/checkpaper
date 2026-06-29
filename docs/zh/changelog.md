# 更新日志

CheckPaper 的所有重要变更都将记录在此文件中。

## [0.1.0] - 2026-06-30

### 新增

- **文档解析**
  - 通过 PyMuPDF 实现 PDF 解析
  - 通过 python-docx 实现 Word (.docx) 解析
  - 通过 pylatexenc 实现 LaTeX 解析
  - 自动格式检测和结构化数据提取

- **验证功能**
  - 格式和结构检查（标题层级、编号规范、布局）
  - 图表引用完整性验证
  - 参考文献引用完整性检查
  - 数据来源验证
  - 数据处理验证（GRIM/SPRITE 测试）
  - 参考文献真实性验证（Crossref、Semantic Scholar）

- **MCP 工具服务器**
  - 8 个 MCP 工具：parse_pdf、parse_docx、parse_latex、check_citations、verify_references、check_figures、check_format、web_search_reference
  - Stdio 传输协议
  - OpenAI Agents SDK 集成

- **API**
  - 基于 FastAPI 的 RESTful API
  - 文档上传、管理和下载
  - 验证任务管理（创建、轮询、取消）
  - 报告生成和导出（MD、HTML、PDF）
  - 健康检查端点
  - Swagger UI 和 ReDoc 文档

- **前端**
  - React 18 + TypeScript + Ant Design
  - 首页功能概览
  - 拖拽上传论文
  - 验证类型选择
  - 实时验证进度追踪
  - 验证报告查看器（Markdown 渲染）
  - 验证历史管理

- **基础设施**
  - Docker Compose 部署（后端、前端、MCP 服务器、MySQL）
  - SQLite（开发）/ MySQL（生产）
  - 基于 pydantic-settings 的环境变量配置
  - CORS 支持、请求计时中间件
  - 全局异常处理
