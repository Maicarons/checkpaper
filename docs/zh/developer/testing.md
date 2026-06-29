# 测试

本指南涵盖 CheckPaper 的测试策略和工具。

## 测试概览

| 类型 | 工具 | 位置 | 用途 |
|------|------|------|------|
| 单元测试 | pytest | `backend/tests/` | 测试独立函数和类 |
| 集成测试 | pytest | `backend/tests/` | 测试 API 端点和服务交互 |
| 前端测试 | Jest/Vitest | `frontend/src/` | 测试 React 组件和 Hook |
| E2E 测试 | Playwright | `tests/` | 测试完整用户工作流 |
| 代码检查 | Ruff, ESLint | — | 代码质量执行 |
| 类型检查 | mypy | — | 静态类型分析 |

## 后端测试

### 安装

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行详细输出
pytest -v

# 运行特定测试文件
pytest backend/tests/test_validation.py

# 运行特定测试函数
pytest backend/tests/test_validation.py::test_format_check

# 运行带覆盖率的测试
pytest --cov=backend/app --cov-report=html

# 运行异步测试
pytest -xvs backend/tests/test_mcp_tools.py
```

### 编写测试

测试位于 `backend/tests/`，遵循 `test_*.py` 命名约定。

#### 单元测试示例

```python
import pytest
from backend.app.services.document import DocumentService

class TestDocumentService:
    def test_create_document(self, session):
        service = DocumentService()
        doc = service.create_document(session, {
            "filename": "test.pdf",
            "file_type": "pdf",
            "file_size": 1024
        })
        assert doc.id is not None
        assert doc.filename == "test.pdf"

    def test_get_document_not_found(self, session):
        service = DocumentService()
        doc = service.get_document(session, "nonexistent-id")
        assert doc is None
```

#### API 测试示例

```python
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_upload_document():
    with open("test_paper.pdf", "rb") as f:
        response = client.post(
            "/api/v1/documents/upload",
            files={"file": ("test.pdf", f, "application/pdf")}
        )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
```

### 测试配置

pytest 配置在 `pyproject.toml` 中：

```toml
[tool.pytest.ini_options]
testpaths = ["backend/tests"]
python_files = ["test_*.py"]
addopts = "-v --cov=backend/app --cov-report=term-missing"
```

## 前端测试

### 安装

```bash
cd frontend
npm install
```

### 运行测试

```bash
# 运行所有测试
npm test

# 运行带覆盖率的测试
npm test -- --coverage

# 监听模式运行
npm test -- --watch
```

### 编写组件测试

```tsx
import { render, screen } from '@testing-library/react'
import HomePage from '../pages/HomePage'

describe('HomePage', () => {
  it('渲染主标题', () => {
    render(<HomePage />)
    expect(screen.getByText('CheckPaper')).toBeInTheDocument()
  })

  it('显示开始验证按钮', () => {
    render(<HomePage />)
    expect(screen.getByText('开始验证')).toBeInTheDocument()
  })
})
```

## 端到端测试

### 安装

```bash
npm install -g playwright
npx playwright install
```

### 运行 E2E 测试

```bash
# 运行所有 E2E 测试
npx playwright test

# 运行特定测试
npx playwright test tests/upload.spec.ts

# 有头浏览器模式运行
npx playwright test --headed

# 查看测试报告
npx playwright show-report
```

### E2E 测试示例

```typescript
import { test, expect } from '@playwright/test'

test('上传并验证论文', async ({ page }) => {
  // 导航到上传页面
  await page.goto('http://localhost:9032/upload')

  // 上传文件
  const fileInput = page.locator('input[type="file"]')
  await fileInput.setInputFiles('test-paper.pdf')

  // 选择验证类型
  await page.check('input[value="format"]')
  await page.check('input[value="citation"]')

  // 开始验证
  await page.click('button:has-text("开始验证")')

  // 等待验证完成
  await page.waitForURL(/\/validation\//)
  await page.waitForSelector('text=已完成', { timeout: 300000 })

  // 查看报告
  await page.click('button:has-text("查看报告")')
  await expect(page.locator('text=验证报告')).toBeVisible()
})
```

## 代码检查和质量

### Python

```bash
# Ruff 检查
ruff check .
ruff check . --fix  # 自动修复

# Black 格式化
black .

# mypy 类型检查
mypy .
```

### TypeScript / React

```bash
cd frontend

# 代码检查
npm run lint

# 格式化
npm run format
```

## 覆盖率报告

### 后端覆盖率

```bash
pytest --cov=backend/app --cov-report=html
# 在浏览器中打开 htmlcov/index.html
```

### 覆盖率目标

| 模块 | 目标覆盖率 |
|------|-----------|
| `services/` | > 80% |
| `api/` | > 70% |
| `schemas/` | > 90% |
| `core/` | > 80% |
| 总体 | > 75% |

## CI/CD 集成

测试通过 GitHub Actions 自动运行：

- 每次推送到 `main` 或 `develop`
- 每个 Pull Request
- 定时每晚运行

```yaml
# .github/workflows/test.yml（示例）
name: Tests
on: [push, pull_request]
jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -e ".[dev]"
      - run: pytest --cov=backend/app

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: cd frontend && npm install && npm test
```
