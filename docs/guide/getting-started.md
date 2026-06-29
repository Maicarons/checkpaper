# Quick Start

This guide walks you through setting up CheckPaper on your local machine.

## Prerequisites

- **Python 3.11+**
- **Node.js 18+** (for frontend development)
- **Git**
- **Docker & Docker Compose** (optional, for containerized deployment)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Maicarons/checkpaper.git
cd checkpaper
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Required: OpenAI API configuration
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# Database (SQLite for local development)
DATABASE_URL=sqlite:///./checkpaper.db

# Application
DEBUG=true
SECRET_KEY=your-secret-key
```

### 3. Install Backend Dependencies

**Using uv (recommended):**

```bash
pip install uv
uv sync
```

**Using pip:**

```bash
pip install -e .
```

### 4. Start the Backend Server

```bash
uvicorn backend.app.main:app --reload --port 9031
```

The API will be available at `http://localhost:9031`. Interactive docs at:
- Swagger UI: `http://localhost:9031/docs`
- ReDoc: `http://localhost:9031/redoc`

### 5. Install and Start the Frontend

```bash
cd frontend
npm install
npm start
```

The frontend will be available at `http://localhost:9032`.

### 6. Upload and Verify Your First Paper

1. Open `http://localhost:9032` in your browser
2. Click **"Start Verification"** on the home page
3. Drag and drop your paper file (PDF, Word, or LaTeX)
4. Select the validation types you want to run
5. Click **"Start Verification"** and wait for results
6. View the detailed verification report

## Docker Deployment (Alternative)

For a one-command deployment:

```bash
# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start all services
docker-compose up -d

# For production with MySQL
docker-compose --profile production up -d
```

Services will be available at:
- Frontend: `http://localhost:9032`
- Backend API: `http://localhost:9031`
- MCP Server: port 8001

## Verifying the Installation

Check that the backend is running:

```bash
curl http://localhost:9031/health
```

Expected response:

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": 1704067200.0
}
```

## Next Steps

- [Features](/guide/features) — Learn about all validation capabilities
- [API Reference](/api/) — Explore the REST API endpoints
- [Deployment](/guide/deployment) — Production deployment guide
