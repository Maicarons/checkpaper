# 贡献指南

感谢你对 CheckPaper 项目的关注！本指南将帮助你快速上手。

## 如何贡献

### 报告 Bug

1. 先检查 [已有的 Issues](https://github.com/Maicarons/checkpaper/issues)
2. 使用 Bug Report 模板创建新 Issue
3. 包含：问题描述、复现步骤、期望与实际行为
4. 如有可能，附上截图或错误日志

### 提出新功能

1. 使用 Feature Request 模板创建 Issue
2. 描述功能需求和使用场景
3. 说明该功能对项目的价值

### 提交代码

#### 1. Fork 并克隆

```bash
# 通过 GitHub UI Fork 后：
git clone https://github.com/yourusername/checkpaper.git
cd checkpaper
```

#### 2. 创建功能分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

#### 3. 搭建开发环境

```bash
# 后端
pip install uv
uv sync

# 前端
cd frontend
npm install
```

#### 4. 进行修改

- 遵循项目的代码风格
- 添加必要的测试
- 更新相关文档

#### 5. 运行测试和代码检查

```bash
# 后端测试
pytest

# 后端代码检查
ruff check .
mypy .

# 前端测试
cd frontend
npm test

# 前端代码检查
npm run lint
```

#### 6. 提交并推送

```bash
git add .
git commit -m "feat: 添加你的功能描述"
git push origin feature/your-feature-name
```

#### 7. 创建 Pull Request

1. 在 GitHub 上访问你的 Fork
2. 点击 "New Pull Request"
3. 填写 PR 描述
4. 等待代码审查

## 代码规范

### Python

- 遵循 [PEP 8](https://peps.python.org/pep-0008/)
- 使用 [Ruff](https://github.com/astral-sh/ruff) 进行代码检查
- 使用 [Black](https://github.com/psf/black) 格式化代码
- 使用 [mypy](https://mypy-lang.org/) 进行类型检查

```bash
ruff check . --fix
black .
mypy .
```

### TypeScript / React

- 使用 ESLint 进行代码检查
- 使用 Prettier 格式化代码
- 遵循 React Hooks 最佳实践

```bash
npm run lint
npm run format
```

## Git 提交规范

我们遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <description>

[optional body]
```

### 类型说明

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更新 |
| `style` | 代码格式（不影响逻辑） |
| `refactor` | 代码重构 |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `chore` | 构建或工具变动 |

### 示例

```
feat(validation): 添加数据处理验证功能
fix(api): 修复文档上传超时错误
docs(readme): 更新安装指南
test(agent): 添加 AgentService 单元测试
```

## 项目结构

```
checkpaper/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/   # API 路由处理
│   │   ├── core/               # 配置、安全、数据库
│   │   ├── services/           # 业务逻辑
│   │   │   ├── document/       # 文档解析服务
│   │   │   ├── validation/     # 验证编排
│   │   │   ├── agent/          # AI Agent 服务
│   │   │   └── report/         # 报告生成
│   │   ├── schemas/            # Pydantic 数据模型
│   │   ├── prompts/            # LLM 提示词模板
│   │   └── main.py             # FastAPI 应用入口
│   ├── mcp_server/             # MCP 工具服务器
│   │   ├── tools/              # 工具实现
│   │   └── server.py           # MCP 服务器入口
│   └── tests/                  # 测试文件
├── frontend/
│   └── src/
│       ├── pages/              # 页面组件
│       ├── components/         # 可复用组件
│       ├── services/           # API 客户端
│       ├── hooks/              # 自定义 Hook
│       └── utils/              # 工具函数
├── docs/                       # VitePress 文档
├── docker-compose.yml
└── pyproject.toml
```

## 开发指南

### 添加新的验证类型

1. 在 `backend/app/schemas/validation.py` 中添加枚举值
2. 在 `backend/app/services/agent/__init__.py` 中实现验证逻辑
3. 在 `backend/mcp_server/tools/__init__.py` 中添加 MCP 工具
4. 更新前端验证类型列表 `frontend/src/pages/UploadPage.tsx`
5. 更新文档

### 添加新的 API 端点

1. 在 `backend/app/api/v1/endpoints/` 中创建或修改路由
2. 在 `backend/app/schemas/` 中定义请求/响应模型
3. 在 `backend/app/services/` 中实现业务逻辑
4. 添加测试
5. 更新 API 文档

### 添加新的前端页面

1. 在 `frontend/src/pages/` 中创建页面组件
2. 在 `frontend/src/App.tsx` 中添加路由
3. 在 `frontend/src/layouts/MainLayout.tsx` 中添加菜单项
4. 在 `frontend/src/services/api.ts` 中添加 API 调用

## 测试

### 后端测试

```bash
# 运行所有测试
pytest

# 运行带覆盖率的测试
pytest --cov=backend/app --cov-report=html

# 运行特定测试文件
pytest backend/tests/test_validation.py

# 运行异步测试
pytest -xvs backend/tests/test_mcp_tools.py
```

### 前端测试

```bash
cd frontend

# 运行测试
npm test

# 运行带覆盖率的测试
npm test -- --coverage

# 运行端到端测试
npm run test:e2e
```

## 文档

### 更新 API 文档

API 文档由 FastAPI 自动生成：
- Swagger UI: `http://localhost:9031/docs`
- ReDoc: `http://localhost:9031/redoc`

### 更新用户指南

用户指南位于 `docs/` 目录，使用 VitePress 构建：

```bash
cd docs
npm install
npm run dev    # 本地开发
npm run build  # 生产构建
```

## 发布流程

1. 更新版本号（`pyproject.toml` 和 `package.json`）
2. 更新 `CHANGELOG.md`
3. 创建 Git 标签
4. 推送标签：`git push origin v0.1.0`
5. GitHub Actions 自动构建和发布

## 行为准则

### 我们的承诺

我们致力于为每个人提供开放和友好的体验：

- 尊重所有参与者
- 接受建设性的批评
- 专注于对社区最有利的事情
- 对其他社区成员表示同理心

### 不可接受的行为

- 性暗示的语言或图像
- 恶意评论或人身攻击
- 公开或私下骚扰
- 未经许可发布他人的私人信息

## 获取帮助

- **Issues:** [GitHub Issues](https://github.com/Maicarons/checkpaper/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Maicarons/checkpaper/discussions)
- **邮箱:** team@checkpaper.com

## 许可证

参与本项目即表示您同意您的贡献将在 [GNU Affero 通用公共许可证 v3.0](https://github.com/Maicarons/checkpaper/blob/main/LICENSE) 下发布。
