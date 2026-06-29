"""
CheckPaper 验证相关数据模型
"""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


class ValidationTypeEnum(StrEnum):
    """验证类型枚举"""
    FORMAT = "format"  # 格式检查
    FIGURE_TABLE = "figure_table"  # 图表引用检查
    CITATION = "citation"  # 参考文献引用检查
    DATA_SOURCE = "data_source"  # 数据来源验证
    DATA_PROCESSING = "data_processing"  # 数据处理验证
    REFERENCE = "reference"  # 参考文献验证


class ValidationStatus(StrEnum):
    """验证状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class IssueSeverity(StrEnum):
    """问题严重程度枚举"""
    CRITICAL = "critical"  # 严重问题（数据造假等）
    WARNING = "warning"  # 警告（格式问题等）
    INFO = "info"  # 信息（建议改进）


# SQLModel 数据库模型
class ValidationTask(SQLModel, table=True):
    """验证任务数据库模型"""
    __tablename__ = "validation_tasks"

    id: str = Field(primary_key=True, max_length=36)
    document_id: str = Field(foreign_key="documents.id", max_length=36)
    validation_types: str  # JSON 序列化的验证类型列表
    options: str | None = None  # JSON 序列化的选项
    status: ValidationStatus = Field(default=ValidationStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None

    # 关系
    document: Document | None = Relationship(back_populates="validation_tasks")
    results: list[ValidationResult] = Relationship(back_populates="task")


class ValidationResult(SQLModel, table=True):
    """验证结果数据库模型"""
    __tablename__ = "validation_results"

    id: str = Field(primary_key=True, max_length=36)
    task_id: str = Field(foreign_key="validation_tasks.id", max_length=36)
    validation_type: ValidationTypeEnum
    status: ValidationStatus = Field(default=ValidationStatus.PENDING)
    issues_count: int = Field(default=0)
    critical_count: int = Field(default=0)
    warning_count: int = Field(default=0)
    info_count: int = Field(default=0)
    summary: str | None = None
    details: str | None = None  # JSON 序列化的详细结果
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # 关系
    task: ValidationTask | None = Relationship(back_populates="results")
    issues: list[ValidationIssue] = Relationship(back_populates="result")


class ValidationIssue(SQLModel, table=True):
    """验证问题数据库模型"""
    __tablename__ = "validation_issues"

    id: str = Field(primary_key=True, max_length=36)
    result_id: str = Field(foreign_key="validation_results.id", max_length=36)
    severity: IssueSeverity
    category: str  # 问题类别
    title: str  # 问题标题
    description: str  # 问题描述
    location: str | None = None  # 问题位置（页码、段落等）
    suggestion: str | None = None  # 解决建议
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # 关系
    result: ValidationResult | None = Relationship(back_populates="issues")


# Pydantic 请求/响应模型
class ValidationRequest(BaseModel):
    """验证请求"""
    document_id: str
    validation_types: list[ValidationTypeEnum] | None = None
    options: dict[str, Any] | None = None


class ValidationResponse(BaseModel):
    """验证响应"""
    task_id: str
    document_id: str
    status: ValidationStatus
    message: str
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None

    class Config:
        from_attributes = True


class IssueResponse(BaseModel):
    """问题响应"""
    id: str
    severity: IssueSeverity
    category: str
    title: str
    description: str
    location: str | None
    suggestion: str | None

    class Config:
        from_attributes = True


class ValidationResultResponse(BaseModel):
    """验证结果响应"""
    id: str
    validation_type: ValidationTypeEnum
    status: ValidationStatus
    issues_count: int
    critical_count: int
    warning_count: int
    info_count: int
    summary: str | None
    issues: list[IssueResponse] = []

    class Config:
        from_attributes = True


class ValidationFullResult(BaseModel):
    """完整验证结果"""
    task_id: str
    document_id: str
    status: ValidationStatus
    total_issues: int
    critical_issues: int
    warning_issues: int
    info_issues: int
    results: list[ValidationResultResponse] = []
    created_at: datetime
    completed_at: datetime | None

    class Config:
        from_attributes = True
