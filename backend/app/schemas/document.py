"""
CheckPaper 文档数据模型
"""
from typing import Optional, List
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel


class DocumentTypeEnum(str, Enum):
    """文档类型枚举"""
    PDF = "pdf"
    WORD = "word"
    LATEX = "latex"
    BIBTEX = "bibtex"


class DocumentStatusEnum(str, Enum):
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
    title: Optional[str] = Field(default=None, max_length=500)
    status: DocumentStatusEnum = Field(default=DocumentStatusEnum.UPLOADED)
    upload_time: datetime = Field(default_factory=datetime.utcnow)
    parsed_time: Optional[datetime] = None
    error_message: Optional[str] = None
    
    # 关系
    validation_tasks: List["ValidationTask"] = Relationship(back_populates="document")
    reports: List["Report"] = Relationship(back_populates="document")


# Pydantic 请求/响应模型
class DocumentCreate(BaseModel):
    """创建文档请求"""
    filename: str
    file_type: DocumentTypeEnum
    title: Optional[str] = None


class DocumentResponse(BaseModel):
    """文档响应"""
    id: str
    filename: str
    file_type: DocumentTypeEnum
    file_size: int
    title: Optional[str]
    status: DocumentStatusEnum
    upload_time: datetime
    parsed_time: Optional[datetime]
    
    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """文档列表响应"""
    documents: List[DocumentResponse]
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
    title: Optional[str] = None
    abstract: Optional[str] = None
    sections: List[dict] = []
    figures: List[dict] = []
    tables: List[dict] = []
    references: List[dict] = []
    citations: List[dict] = []
    raw_text: str = ""
    metadata: dict = {}
