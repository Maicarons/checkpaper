"""
CheckPaper 配置管理模块
使用 pydantic-settings 进行类型安全的配置管理
"""
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """应用配置类"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # 应用基础配置
    app_name: str = "CheckPaper"
    app_version: str = "0.1.0"
    debug: bool = False
    secret_key: str = Field(default="change-me-in-production", alias="SECRET_KEY")
    
    # API 配置
    api_v1_prefix: str = "/api/v1"
    project_name: str = "CheckPaper"
    
    # CORS 配置
    backend_cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # 数据库配置
    # 本地开发: sqlite:///./checkpaper.db
    # 生产环境: mysql+pymysql://user:password@localhost:3306/checkpaper
    database_url: str = "sqlite:///./checkpaper.db"
    db_echo: bool = False  # 是否打印SQL语句
    openai_api_key: str = ""
    openai_base_url: str = "http://192.168.56.1:8990"  # 自定义API地址
    openai_model: str = "qwythos-9b-claude-mythos-5-1m"
    openai_max_tokens: int = 4096
    
    # GROBID 配置
    grobid_server_url: str = "http://localhost:8070"
    grobid_timeout: int = 30
    
    # 文件上传配置
    max_upload_size_mb: int = 50
    upload_dir: str = "./uploads"
    allowed_extensions: List[str] = ["pdf", "docx", "doc", "tex", "latex", "bib", "txt", "md"]
    
    # 参考文献验证 API 配置
    crossref_api_key: Optional[str] = None
    crossref_mailto: str = "user@example.com"
    semantic_scholar_api_key: Optional[str] = None
    
    # 报告生成配置
    report_output_dir: str = "./reports"
    report_template_dir: str = "./templates"
    
    # 日志配置
    log_level: str = "INFO"
    log_file: str = "./logs/checkpaper.log"
    
    # Agent 配置
    agent_max_turns: int = 15
    agent_sandbox_enabled: bool = True
    agent_code_execution_timeout: int = 60
    
    # MCP Server 配置
    mcp_server_host: str = "0.0.0.0"
    mcp_server_port: int = 8001
    
    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        """解析 CORS 配置"""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @property
    def database_url_sync(self) -> str:
        """同步数据库 URL"""
        return self.database_url.replace("sqlite+aiosqlite", "sqlite")
    
    @property
    def max_upload_size_bytes(self) -> int:
        """最大上传文件大小（字节）"""
        return self.max_upload_size_mb * 1024 * 1024


# 全局设置实例
settings = Settings()


def get_settings() -> Settings:
    """获取设置实例（用于依赖注入）"""
    return settings
