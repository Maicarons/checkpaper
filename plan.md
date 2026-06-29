# CheckPaper - AI论文验证智能体项目计划

## 项目概述
基于Python和FastAPI的AI论文验证agent智能体项目，支持多种格式（LaTeX、Word、PDF）的论文验证，包括格式检查、引用验证、数据真实性验证等功能，并提供完整的报告生成和React前端界面。

## 技术栈
- **后端**: Python 3.11+ + FastAPI + OpenAI Agents SDK
- **前端**: React 18+ + TypeScript + Ant Design
- **文档解析**: PyMuPDF, python-docx, pylatexenc, GROBID
- **参考文献验证**: Crossref API, Semantic Scholar API
- **Agent框架**: OpenAI Agents SDK + MCP (Model Context Protocol)
- **数据库**: SQLite (本地开发) / MySQL (生产环境)
- **部署**: Docker + Docker Compose

## 项目结构
```
checkpaper/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/               # API路由层
│   │   │   ├── v1/           # API版本管理
│   │   │   │   └── endpoints/ # API端点
│   │   │   └── deps.py       # 依赖注入
│   │   ├── core/             # 核心配置
│   │   │   ├── config.py     # 配置管理
│   │   │   ├── security.py   # 安全认证
│   │   │   └── db.py         # 数据库连接
│   │   ├── services/         # 业务服务层
│   │   │   ├── document/     # 文档解析服务
│   │   │   ├── validation/   # 验证服务
│   │   │   ├── agent/        # Agent服务
│   │   │   └── report/       # 报告生成服务
│   │   ├── models/           # 数据模型
│   │   ├── schemas/          # Pydantic模式
│   │   ├── prompts/          # 提示词模板（与代码分离）
│   │   │   └── templates/    # 提示词模板文件
│   │   └── main.py           # FastAPI应用入口
│   ├── mcp_server/           # MCP服务器
│   │   ├── tools/            # MCP工具实现
│   │   └── server.py         # MCP服务器入口
│   ├── tests/                # 测试文件
│   ├── pyproject.toml        # 项目配置
│   └── Dockerfile            # 后端容器配置
├── frontend/                  # 前端应用
│   ├── src/
│   │   ├── components/       # React组件
│   │   ├── pages/           # 页面组件
│   │   ├── services/        # API服务
│   │   ├── hooks/           # 自定义Hook
│   │   └── utils/           # 工具函数
│   ├── package.json
│   └── Dockerfile           # 前端容器配置
├── docker-compose.yml        # 容器编排
├── plan.md                   # 项目计划（本文件）
├── .env.example             # 环境变量示例
└── README.md                # 项目文档
```

## 分层实施计划

### 阶段1: 项目基础架构搭建 ✅
- **1.1 创建项目目录结构和配置文件** ✅
  - ✅ 创建完整的项目目录结构
  - ✅ 配置pyproject.toml（依赖管理）
  - ✅ 创建.env.example环境变量模板
  - ✅ 配置.gitignore和.gitkeep文件
  - ✅ 创建README.md项目文档

- **1.2 搭建FastAPI后端基础框架** ✅
  - ✅ 创建FastAPI应用入口（main.py）
  - ✅ 实现配置管理（pydantic-settings）
  - ✅ 设置数据库连接（SQLModel + SQLite/MySQL）
  - ✅ 创建基础API路由结构
  - ✅ 实现错误处理中间件
  - ✅ 创建安全认证模块

- **1.3 搭建React前端基础框架**
  - 使用Vite创建React + TypeScript项目
  - 配置Ant Design组件库
  - 设置API客户端（axios）
  - 创建基础布局和路由结构

### 阶段2: 文档解析模块实现
- **2.1 实现PDF文档解析服务** ✅
  - ✅ 集成PyMuPDF进行PDF文本提取
  - ✅ 实现PDF表格检测和提取
  - ✅ 实现PDF图片提取和引用检测
  - 创建PDF解析结果的数据模型

- **2.2 实现Word文档解析服务** ✅
  - ✅ 集成python-docx进行DOCX解析
  - ✅ 提取段落、表格、图片引用
  - ✅ 实现Word文档结构化输出

- **2.3 实现LaTeX文档解析服务** ✅
  - ✅ 集成pylatexenc进行LaTeX解析
  - ✅ 提取章节结构、公式、引用
  - ✅ 解析参考文献（.bib文件）
  - ✅ 实现LaTeX到结构化数据的转换

- **2.4 创建统一文档处理接口** ✅
  - ✅ 设计统一的文档解析接口
  - ✅ 实现格式自动检测和分发
  - ✅ 创建文档结构标准化模型

### 阶段3: 论文验证核心功能
- **3.1 实现格式和结构检查**
  - 检查标题层级和编号规范
  - 验证字体、字号一致性
  - 检查页面布局（页边距、页眉页脚）
  - 验证目录与正文对应关系
  - 检查图表编号连续性

- **3.2 实现图片/表格引用检查**
  - 提取所有图片/表格定义标签
  - 提取正文中所有引用标签
  - 交叉验证引用完整性
  - 检测"孤儿引用"和"未引用"项目

- **3.3 实现参考文献引用检查**
  - 提取正文中的引用标记
  - 提取参考文献列表
  - 验证内部引用一致性
  - 检测重复引用和缺失引用

- **3.4 实现参考文献真实性验证**
  - 集成Crossref API验证DOI真实性
  - 实现标题+作者模糊匹配
  - 验证文献元数据（期刊、年份等）
  - 检测可疑或虚假参考文献

- **3.5 实现数据真实性验证**
  - 提取论文中的数值数据
  - 实现GRIM/SPRITE统计一致性测试
  - 验证p值、置信区间合理性
  - 检查图表数据与正文报告的一致性

### 阶段4: MCP Server和Agent编排
- **4.1 创建MCP验证工具服务器** ✅
  - ✅ 设计MCP工具接口规范
  - ✅ 实现文档解析工具（parse_pdf, parse_docx, parse_latex）
  - ✅ 实现验证工具（check_citations, verify_references, check_figures）
  - ✅ 实现搜索工具（web_search_reference）
  - ✅ 配置MCP服务器传输协议

- **4.2 实现OpenAI Agent编排**
  - 集成OpenAI Agents SDK
  - 创建主编排Agent（Orchestrator）
  - 创建专项验证Agent（格式、引用、数据）
  - 实现Agent间任务分发和结果汇总

- **4.3 实现Agent代码执行验证**
  - 创建安全的代码执行沙箱
  - 实现Agent生成验证代码的功能
  - 集成源数据进行算法验证

- **4.4 实现联网搜索验证**
  - 集成OpenAI WebSearchTool
  - 实现参考文献联网搜索验证
  - 配置搜索结果缓存和限流

### 阶段5: 报告生成和前端开发
- **5.1 实现报告生成服务** ✅
  - ✅ 设计报告模板（Markdown格式）
  - ✅ 实现验证结果结构化存储
  - ✅ 生成问题清单和严重程度分级
  - ✅ 支持报告导出（PDF、HTML）

- **5.2 开发前端核心组件**
  - 创建文件上传组件（支持多格式）
  - 实现验证进度显示组件
  - 开发验证结果展示组件
  - 创建报告查看和下载组件

- **5.3 开发前端页面**
  - 创建首页（项目介绍和快速开始）
  - 实现论文上传和验证页面
  - 开发验证历史记录页面
  - 创建报告详情查看页面

- **5.4 集成前后端联调**
  - 实现API接口联调
  - 配置WebSocket实时进度更新
  - 实现文件上传和下载功能

### 阶段6: 测试、文档和部署
- **6.1 编写测试用例**
  - 编写单元测试（pytest）
  - 编写集成测试（API测试）
  - 编写端到端测试（Playwright）
  - 实现测试覆盖率报告

- **6.2 编写项目文档** ✅
  - ✅ 编写详细的README.md
  - 创建API文档（Swagger/OpenAPI）
  - 编写用户使用手册
  - 创建开发者贡献指南

- **6.3 配置容器化和部署** ✅
  - ✅ 创建后端Dockerfile
  - 配置docker-compose.yml ✅
  - ✅ 实现环境变量管理和配置
  - 配置生产环境部署脚本

- **6.4 性能优化和安全加固**
  - 实现API限流和缓存
  - 配置CORS和安全头
  - 实现文件上传大小限制
  - 配置日志和监控

## 关键技术决策

1. **包管理**: 使用uv + pyproject.toml（现代Python标准）
2. **配置管理**: pydantic-settings（类型安全，.env支持）
3. **Agent框架**: OpenAI Agents SDK + MCP（原生集成，标准化工具协议）
4. **文档解析**: PyMuPDF（PDF）、python-docx（Word）、pylatexenc（LaTeX）
5. **前端框架**: React + TypeScript + Ant Design（成熟稳定，组件丰富）
6. **数据库**: SQLite（本地开发）+ MySQL（生产环境）
7. **容器化**: Docker Compose（一键部署，环境一致性）
8. **提示词管理**: 提示词与代码分离，支持模板化

## 数据库配置

### 本地开发 (SQLite)
```env
DATABASE_URL=sqlite:///./checkpaper.db
```

### 生产环境 (MySQL)
```env
DATABASE_URL=mysql+pymysql://checkpaper:password@localhost:3306/checkpaper
```

## 风险评估

1. **GROBID部署复杂性**: 需要Docker部署，增加运维复杂度
   - 缓解: 提供本地安装脚本，支持降级到基础解析

2. **OpenAI API成本**: 大量验证可能产生较高API费用
   - 缓解: 实现缓存机制，支持本地模型部署

3. **学术文献数据库访问限制**: Crossref/Semantic Scholar可能有调用限制
   - 缓解: 实现缓存和限流，支持多API轮换

4. **代码执行安全风险**: Agent生成代码执行存在安全隐患
   - 缓解: 实现严格的沙箱环境，限制文件系统和网络访问

## 成功标准

1. ✅ 支持PDF、Word、LaTeX三种格式的论文解析
2. 实现至少5种核心验证功能
3. ✅ 生成结构化的验证报告（Markdown格式）
4. 提供用户友好的React前端界面
5. 完整的测试覆盖率（>80%）
6. ✅ 详细的项目文档和API文档
7. ✅ 一键Docker部署方案

## 下一步行动

1. **完善验证逻辑**: 实现各种验证功能的具体算法
2. **开发前端界面**: 创建React前端应用
3. **编写测试用例**: 确保代码质量
4. **集成Agent框架**: 连接MCP服务器和OpenAI Agent
5. **性能优化**: 实现缓存和异步处理
