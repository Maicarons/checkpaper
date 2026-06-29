"""
CheckPaper 报告相关数据模型
"""
from typing import Optional, List
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel


class ReportStatus(str, Enum):
    """报告状态枚举"""
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class ReportFormat(str, Enum):
    """报告格式枚举"""
    MARKDOWN = "md"
    PDF = "pdf"
    HTML = "html"


# SQLModel 数据库模型
class Report(SQLModel, table=True):
    """报告数据库模型"""
    __tablename__ = "reports"
    
    id: str = Field(primary_key=True, max_length=36)
    document_id: str = Field(foreign_key="documents.id", max_length=36)
    validation_task_id: Optional[str] = Field(default=None, max_length=36)
    title: str = Field(max_length=500)
    status: ReportStatus = Field(default=ReportStatus.GENERATING)
    file_path: Optional[str] = None
    content: Optional[str] = None  # Markdown 内容
    total_issues: int = Field(default=0)
    critical_issues: int = Field(default=0)
    warning_issues: int = Field(default=0)
    info_issues: int = Field(default=0)
    score: Optional[float] = None  # 论文质量评分 (0-100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    # 关系
    document: Optional["Document"] = Relationship(back_populates="reports")


# Pydantic 请求/响应模型
class ReportCreate(BaseModel):
    """创建报告请求"""
    document_id: str
    validation_task_id: Optional[str] = None
    title: Optional[str] = None


class ReportResponse(BaseModel):
    """报告响应"""
    id: str
    document_id: str
    title: str
    status: ReportStatus
    total_issues: int
    critical_issues: int
    warning_issues: int
    info_issues: int
    score: Optional[float]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ReportListResponse(BaseModel):
    """报告列表响应"""
    reports: List[ReportResponse]
    total: int
    page: int
    page_size: int


class ReportDetailResponse(BaseModel):
    """报告详情响应"""
    id: str
    document_id: str
    title: str
    status: ReportStatus
    content: Optional[str]  # Markdown 内容
    total_issues: int
    critical_issues: int
    warning_issues: int
    info_issues: int
    score: Optional[float]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True
