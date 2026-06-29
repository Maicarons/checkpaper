"""
CheckPaper 测试配置
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from backend.app.core.config import Settings
from backend.app.core.db import get_session
from backend.app.main import app


@pytest.fixture(name="session")
def session_fixture():
    """创建测试数据库会话"""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """创建测试客户端"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="settings")
def settings_fixture():
    """创建测试配置"""
    return Settings(
        openai_api_key="test-key",
        database_url="sqlite:///./test.db",
        debug=True,
        secret_key="test-secret-key",
    )
