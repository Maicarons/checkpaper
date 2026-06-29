"""
CheckPaper 数据库配置模块
使用 SQLModel 进行数据库 ORM 操作
支持本地 SQLite 和生产 MySQL
"""
from typing import Generator
from sqlmodel import SQLModel, Session, create_engine
from .config import settings


def get_engine():
    """
    根据数据库URL创建对应的引擎
    支持 SQLite (本地) 和 MySQL (生产)
    """
    database_url = settings.database_url
    
    # SQLite 配置
    if database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
        engine = create_engine(
            database_url,
            echo=settings.db_echo,
            connect_args=connect_args
        )
    # MySQL 配置
    elif database_url.startswith("mysql"):
        engine = create_engine(
            database_url,
            echo=settings.db_echo,
            pool_size=10,  # 连接池大小
            max_overflow=20,  # 最大溢出连接数
            pool_pre_ping=True,  # 连接前ping检测
            pool_recycle=3600,  # 连接回收时间(秒)
        )
    else:
        # 默认配置
        engine = create_engine(
            database_url,
            echo=settings.db_echo
        )
    
    return engine


# 创建数据库引擎
engine = get_engine()


def create_db_and_tables() -> None:
    """创建数据库表"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """获取数据库会话（用于依赖注入）"""
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


def init_db() -> None:
    """初始化数据库"""
    create_db_and_tables()
    print(f"数据库初始化完成 (类型: {'SQLite' if 'sqlite' in settings.database_url else 'MySQL'})")


# 用于后台任务的会话工厂
def SessionLocal():
    """创建新的数据库会话（用于后台任务）"""
    return Session(engine)
