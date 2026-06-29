"""
CheckPaper 数据模型模块
"""
from .document import (
    Document,
    DocumentCreate,
    DocumentListResponse,
    DocumentResponse,
    DocumentStatusEnum,
    DocumentTypeEnum,
    DocumentUploadResponse,
    ParsedContent,
)
from .report import (
    Report,
    ReportCreate,
    ReportDetailResponse,
    ReportFormat,
    ReportListResponse,
    ReportResponse,
    ReportStatus,
)
from .validation import (
    IssueResponse,
    IssueSeverity,
    ValidationFullResult,
    ValidationIssue,
    ValidationRequest,
    ValidationResponse,
    ValidationResult,
    ValidationResultResponse,
    ValidationStatus,
    ValidationTask,
    ValidationTypeEnum,
)

__all__ = [
    # Document
    "Document",
    "DocumentTypeEnum",
    "DocumentStatusEnum",
    "DocumentCreate",
    "DocumentResponse",
    "DocumentListResponse",
    "DocumentUploadResponse",
    "ParsedContent",
    # Validation
    "ValidationTask",
    "ValidationResult",
    "ValidationIssue",
    "ValidationTypeEnum",
    "ValidationStatus",
    "IssueSeverity",
    "ValidationRequest",
    "ValidationResponse",
    "IssueResponse",
    "ValidationResultResponse",
    "ValidationFullResult",
    # Report
    "Report",
    "ReportStatus",
    "ReportFormat",
    "ReportCreate",
    "ReportResponse",
    "ReportListResponse",
    "ReportDetailResponse",
]
