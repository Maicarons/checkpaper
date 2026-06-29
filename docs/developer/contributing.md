# Contributing Guide

Thank you for your interest in contributing to CheckPaper! This guide will help you get started.

## How to Contribute

### Report Bugs

1. Check [existing issues](https://github.com/Maicarons/checkpaper/issues) first
2. Create a new issue using the Bug Report template
3. Include: description, steps to reproduce, expected vs actual behavior
4. Attach screenshots or error logs if possible

### Request Features

1. Open an issue using the Feature Request template
2. Describe the feature, use case, and expected benefit
3. Explain why this feature would be valuable to the project

### Submit Code

#### 1. Fork and Clone

```bash
# Fork via GitHub UI, then:
git clone https://github.com/yourusername/checkpaper.git
cd checkpaper
```

#### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

#### 3. Set Up Development Environment

```bash
# Backend
pip install uv
uv sync

# Frontend
cd frontend
npm install
```

#### 4. Make Your Changes

- Follow the project's code style
- Add necessary tests
- Update related documentation

#### 5. Run Tests and Linting

```bash
# Backend tests
pytest

# Backend linting
ruff check .
mypy .

# Frontend tests
cd frontend
npm test

# Frontend linting
npm run lint
```

#### 6. Commit and Push

```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

#### 7. Create Pull Request

1. Visit your fork on GitHub
2. Click "New Pull Request"
3. Fill in the PR description with details about your changes
4. Wait for code review

## Code Style

### Python

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use [Ruff](https://github.com/astral-sh/ruff) for linting
- Use [Black](https://github.com/psf/black) for formatting
- Use [mypy](https://mypy-lang.org/) for type checking

```bash
ruff check . --fix
black .
mypy .
```

### TypeScript / React

- Use ESLint for linting
- Use Prettier for formatting
- Follow React Hooks best practices

```bash
npm run lint
npm run format
```

## Git Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation update |
| `style` | Code style (no logic change) |
| `refactor` | Code refactoring |
| `perf` | Performance improvement |
| `test` | Adding/updating tests |
| `chore` | Build or tooling changes |

### Examples

```
feat(validation): add data processing validation
fix(api): fix document upload timeout error
docs(readme): update installation guide
test(agent): add unit tests for AgentService
```

## Project Structure

```
checkpaper/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/   # API route handlers
│   │   ├── core/               # Configuration, security, DB
│   │   ├── services/           # Business logic
│   │   │   ├── document/       # Document parsing service
│   │   │   ├── validation/     # Validation orchestration
│   │   │   ├── agent/          # AI agent service
│   │   │   └── report/         # Report generation
│   │   ├── schemas/            # Pydantic data models
│   │   ├── prompts/            # LLM prompt templates
│   │   └── main.py             # FastAPI application entry
│   ├── mcp_server/             # MCP tool server
│   │   ├── tools/              # Tool implementations
│   │   └── server.py           # MCP server entry
│   └── tests/                  # Test files
├── frontend/
│   └── src/
│       ├── pages/              # Page components
│       ├── components/         # Reusable components
│       ├── services/           # API client
│       ├── hooks/              # Custom React hooks
│       └── utils/              # Utility functions
├── docs/                       # VitePress documentation
├── docker-compose.yml
└── pyproject.toml
```

## Development Guides

### Adding a New Validation Type

1. Add enum value in `backend/app/schemas/validation.py`
2. Implement validation logic in `backend/app/services/agent/__init__.py`
3. Add MCP tool in `backend/mcp_server/tools/__init__.py`
4. Update frontend validation type list in `frontend/src/pages/UploadPage.tsx`
5. Update documentation

### Adding a New API Endpoint

1. Create or modify route in `backend/app/api/v1/endpoints/`
2. Define request/response models in `backend/app/schemas/`
3. Implement business logic in `backend/app/services/`
4. Add tests
5. Update API documentation

### Adding a New Frontend Page

1. Create page component in `frontend/src/pages/`
2. Add route in `frontend/src/App.tsx`
3. Add menu item in `frontend/src/layouts/MainLayout.tsx`
4. Add API calls in `frontend/src/services/api.ts`

## Testing

### Backend Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend/app --cov-report=html

# Run specific test file
pytest backend/tests/test_validation.py

# Run async tests
pytest -xvs backend/tests/test_mcp_tools.py
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run end-to-end tests
npm run test:e2e
```

## Documentation

### Updating API Docs

API documentation is auto-generated by FastAPI:
- Swagger UI: `http://localhost:9031/docs`
- ReDoc: `http://localhost:9031/redoc`

### Updating User Guide

The user guide is in the `docs/` directory, built with VitePress:

```bash
cd docs
npm install
npm run dev    # Local development
npm run build  # Production build
```

## Release Process

1. Update version in `pyproject.toml` and `package.json`
2. Update `CHANGELOG.md`
3. Create a Git tag
4. Push tag: `git push origin v0.1.0`
5. GitHub Actions will handle build and release

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive experience for everyone. We pledge to:

- Respect all participants
- Accept constructive criticism
- Focus on what is best for the community
- Show empathy toward other community members

### Unacceptable Behavior

- Sexualized language or imagery
- Trolling, insulting comments, and personal attacks
- Public or private harassment
- Publishing others' private information without consent

## Getting Help

- **Issues:** [GitHub Issues](https://github.com/Maicarons/checkpaper/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Maicarons/checkpaper/discussions)
- **Email:** team@checkpaper.com

## License

By contributing, you agree that your contributions will be licensed under the [GNU Affero General Public License v3.0](https://github.com/Maicarons/checkpaper/blob/main/LICENSE).
