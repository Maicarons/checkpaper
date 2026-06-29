# Testing

This guide covers the testing strategy and tools for CheckPaper.

## Testing Overview

| Type | Tool | Location | Purpose |
|------|------|----------|---------|
| Unit Tests | pytest | `backend/tests/` | Test individual functions and classes |
| Integration Tests | pytest | `backend/tests/` | Test API endpoints and service interactions |
| Frontend Tests | Jest/Vitest | `frontend/src/` | Test React components and hooks |
| E2E Tests | Playwright | `tests/` | Test full user workflows |
| Linting | Ruff, ESLint | — | Code quality enforcement |
| Type Checking | mypy | — | Static type analysis |

## Backend Testing

### Setup

```bash
# Install dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest backend/tests/test_validation.py

# Run specific test function
pytest backend/tests/test_validation.py::test_format_check

# Run with coverage report
pytest --cov=backend/app --cov-report=html

# Run only async tests
pytest -xvs backend/tests/test_mcp_tools.py
```

### Writing Tests

Tests are located in `backend/tests/` and follow the naming convention `test_*.py`.

#### Unit Test Example

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

#### API Test Example

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

### Test Configuration

The pytest configuration is in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["backend/tests"]
python_files = ["test_*.py"]
addopts = "-v --cov=backend/app --cov-report=term-missing"
```

## Frontend Testing

### Setup

```bash
cd frontend
npm install
```

### Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

### Writing Component Tests

```tsx
import { render, screen } from '@testing-library/react'
import HomePage from '../pages/HomePage'

describe('HomePage', () => {
  it('renders the main title', () => {
    render(<HomePage />)
    expect(screen.getByText('CheckPaper')).toBeInTheDocument()
  })

  it('shows the get started button', () => {
    render(<HomePage />)
    expect(screen.getByText('Start Verification')).toBeInTheDocument()
  })
})
```

## End-to-End Testing

### Setup

```bash
npm install -g playwright
npx playwright install
```

### Running E2E Tests

```bash
# Run all E2E tests
npx playwright test

# Run specific test
npx playwright test tests/upload.spec.ts

# Run with headed browser
npx playwright test --headed

# Show test report
npx playwright show-report
```

### E2E Test Example

```typescript
import { test, expect } from '@playwright/test'

test('upload and verify paper', async ({ page }) => {
  // Navigate to upload page
  await page.goto('http://localhost:9032/upload')

  // Upload a file
  const fileInput = page.locator('input[type="file"]')
  await fileInput.setInputFiles('test-paper.pdf')

  // Select validation types
  await page.check('input[value="format"]')
  await page.check('input[value="citation"]')

  // Start validation
  await page.click('button:has-text("Start Verification")')

  // Wait for validation to complete
  await page.waitForURL(/\/validation\//)
  await page.waitForSelector('text=Completed', { timeout: 300000 })

  // View report
  await page.click('button:has-text("View Report")')
  await expect(page.locator('text=Verification Report')).toBeVisible()
})
```

## Linting and Code Quality

### Python

```bash
# Lint with Ruff
ruff check .
ruff check . --fix  # Auto-fix issues

# Format with Black
black .

# Type check with mypy
mypy .
```

### TypeScript / React

```bash
cd frontend

# Lint
npm run lint

# Format
npm run format
```

## Coverage Reports

### Backend Coverage

```bash
pytest --cov=backend/app --cov-report=html
# Open htmlcov/index.html in browser
```

### Coverage Targets

| Module | Target Coverage |
|--------|----------------|
| `services/` | > 80% |
| `api/` | > 70% |
| `schemas/` | > 90% |
| `core/` | > 80% |
| Overall | > 75% |

## CI/CD Integration

Tests run automatically via GitHub Actions on:

- Every push to `main` or `develop`
- Every pull request
- Scheduled nightly runs

```yaml
# .github/workflows/test.yml (example)
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
