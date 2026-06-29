"""
CheckPaper 文档数据模型
"""
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .report import Report
    from .validation import ValidationTask


class DocumentTypeEnum(StrEnum):
    """文档类型枚举"""
    PDF = "pdf"
    WORD = "word"
    LATEX = "latex"
    BIBTEX = "bibtex"


class DocumentStatusEnum(StrEnum):
    """文档状态枚举"""
    UPLOADED = "uploaded"
    PARSING = "parsing"
    PARSED = "parsed"
    FAILED = "failed"


# SQLModel 数据库模型
class Document(SQLModel, table=True):
    """文档数据库模型"""
    __tablename__ = "documents"

    id: str = Field(primary_key=True, max_length=36)
    filename: str = Field(max_length=255)
    saved_filename: str = Field(max_length=255)
    file_path: str = Field(max_length=500)
    file_size: int
    file_type: DocumentTypeEnum
    title: str | None = Field(default=None, max_length=500)
    status: DocumentStatusEnum = Field(default=DocumentStatusEnum.UPLOADED)
    upload_time: datetime = Field(default_factory=datetime.utcnow)
    parsed_time: datetime | None = None
    error_message: str | None = None

    # 关系
    validation_tasks: list["ValidationTask"] = Relationship(back_populates="document")
    reports: list["Report"] = Relationship(back_populates="document")


# Pydantic 请求/响应模型
class DocumentCreate(BaseModel):
    """创建文档请求"""
    filename: str
    file_type: DocumentTypeEnum
    title: str | None = None


class DocumentResponse(BaseModel):
    """文档响应"""
    id: str
    filename: str
    file_type: DocumentTypeEnum
    file_size: int
    title: str | None
    status: DocumentStatusEnum
    upload_time: datetime
    parsed_time: datetime | None

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """文档列表响应"""
    documents: list[DocumentResponse]
    total: int
    page: int
    page_size: int


class DocumentUploadResponse(BaseModel):
    """文档上传响应"""
    id: str
    filename: str
    file_type: DocumentTypeEnum
    file_size: int
    upload_time: datetime
    message: str


class ParsedContent(BaseModel):
    """解析后的文档内容"""
    title: str | None = None
    abstract: str | None = None
    sections: list[dict] = []
    figures: list[dict] = []
    tables: list[dict] = []
    references: list[dict] = []
    citations: list[dict] = []
    raw_text: str = ""
    metadata: dict = {}
