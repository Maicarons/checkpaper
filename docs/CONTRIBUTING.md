# 贡献指南

感谢您对 CheckPaper 项目的关注！我们欢迎任何形式的贡献。

## 如何贡献

### 报告 Bug

1. 在 [Issues](https://github.com/yourusername/checkpaper/issues) 页面创建新 Issue
2. 使用 Bug 报告模板
3. 提供详细的问题描述、复现步骤、期望行为和实际行为
4. 如果可能，提供截图或错误日志

### 提出新功能

1. 在 [Issues](https://github.com/yourusername/checkpaper/issues) 页面创建新 Issue
2. 使用功能请求模板
3. 详细描述功能需求和使用场景
4. 说明为什么这个功能对项目有价值

### 提交代码

#### 1. Fork 项目

```bash
# 点击项目页面右上角的 Fork 按钮
```

#### 2. 克隆到本地

```bash
git clone https://github.com/yourusername/checkpaper.git
cd checkpaper
```

#### 3. 创建功能分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

#### 4. 配置开发环境

```bash
# 后端
cd backend
pip install -e ".[dev]"

# 前端
cd frontend
npm install
```

#### 5. 进行修改

- 遵循项目的代码风格
- 添加必要的测试
- 更新相关文档

#### 6. 运行测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm test

# 代码检查
cd backend
ruff check .
mypy .
```

#### 7. 提交更改

```bash
git add .
git commit -m "feat: add your feature description"
```

#### 8. 推送到 GitHub

```bash
git push origin feature/your-feature-name
```

#### 9. 创建 Pull Request

1. 访问您的 Fork 页面
2. 点击 "New Pull Request"
3. 填写 PR 描述
4. 等待代码审查

## 代码规范

### Python 代码风格

- 遵循 [PEP 8](https://peps.python.org/pep-0008/) 规范
- 使用 [Black](https://github.com/psf/black) 格式化代码
- 使用 [Ruff](https://github.com/astral-sh/ruff) 进行代码检查
- 使用 [mypy](https://mypy-lang.org/) 进行类型检查

```bash
# 格式化代码
black .

# 检查代码
ruff check .

# 类型检查
mypy .
```

### TypeScript/React 代码风格

- 使用 ESLint 进行代码检查
- 使用 Prettier 格式化代码
- 遵循 React Hooks 最佳实践

```bash
# 检查代码
npm run lint

# 格式化代码
npm run format
```

### Git 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

类型说明：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行的变动）
- `refactor`: 重构（既不是新功能，也不是修改 bug 的代码变动）
- `perf`: 性能优化
- `test`: 增加测试
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat(validation): add data processing validation
fix(api): fix document upload error
docs(readme): update installation guide
```

## 项目结构

```
checkpaper/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/               # API 路由
│   │   ├── core/              # 核心配置
│   │   ├── services/          # 业务服务
│   │   ├── schemas/           # 数据模型
│   │   └── prompts/           # 提示词模板
│   ├── mcp_server/            # MCP 服务器
│   └── tests/                 # 测试文件
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── components/        # React 组件
│   │   ├── pages/             # 页面组件
│   │   ├── services/          # API 服务
│   │   └── hooks/             # 自定义 Hook
│   └── package.json
├── docs/                       # 文档
├── docker-compose.yml          # Docker 配置
└── pyproject.toml              # Python 项目配置
```

## 开发指南

### 添加新的验证类型

1. 在 `backend/app/schemas/validation.py` 中添加新的枚举值
2. 在 `backend/app/services/agent.py` 中实现验证逻辑
3. 在 `backend/mcp_server/tools/` 中添加 MCP 工具
4. 更新前端验证类型列表

### 添加新的 API 端点

1. 在 `backend/app/api/v1/endpoints/` 中创建或修改路由文件
2. 在 `backend/app/schemas/` 中定义请求/响应模型
3. 在 `backend/app/services/` 中实现业务逻辑
4. 添加测试用例

### 添加新的前端页面

1. 在 `frontend/src/pages/` 中创建页面组件
2. 在 `frontend/src/App.tsx` 中添加路由
3. 在 `frontend/src/layouts/MainLayout.tsx` 中添加菜单项
4. 在 `frontend/src/services/api.ts` 中添加 API 调用

## 测试

### 后端测试

```bash
cd backend

# 运行所有测试
pytest

# 运行带覆盖率的测试
pytest --cov=app --cov-report=html

# 运行特定测试
pytest tests/test_validation.py

# 运行异步测试
pytest -xvs tests/test_mcp_tools.py
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

API 文档由 FastAPI 自动生成，访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 更新用户手册

用户手册位于 `docs/USER_GUIDE.md`，使用 Markdown 格式编写。

## 发布流程

1. 更新版本号（`pyproject.toml` 和 `package.json`）
2. 更新 `CHANGELOG.md`
3. 创建 Git Tag
4. GitHub Actions 自动构建和发布

## 行为准则

### 我们的承诺

为了营造一个开放和友好的环境，我们作为贡献者和维护者承诺：

- 尊重所有参与者
- 接受建设性的批评
- 专注于对社区最有利的事情
- 对其他社区成员表示同理心

### 我们的标准

积极行为包括：
- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性的批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

不可接受的行为包括：
- 使用性暗示的语言或图像
- 恶意评论或人身攻击
- 公开或私下骚扰
- 未经许可发布他人的私人信息

## 联系方式

如有任何问题，请通过以下方式联系我们：

- **Issues**: https://github.com/yourusername/checkpaper/issues
- **Discussions**: https://github.com/yourusername/checkpaper/discussions
- **Email**: contributors@checkpaper.com

## 许可证

参与本项目即表示您同意您的贡献将在 [MIT 许可证](LICENSE) 下发布。
