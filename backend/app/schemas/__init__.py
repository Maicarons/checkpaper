"""
CheckPaper 数据模型模块
"""
from .document import (
    Document,
    DocumentTypeEnum,
    DocumentStatusEnum,
    DocumentCreate,
    DocumentResponse,
    DocumentListResponse,
    DocumentUploadResponse,
    ParsedContent
)
from .validation import (
    ValidationTask,
    ValidationResult,
    ValidationIssue,
    ValidationTypeEnum,
    ValidationStatus,
    IssueSeverity,
    ValidationRequest,
    ValidationResponse,
    IssueResponse,
    ValidationResultResponse,
    ValidationFullResult
)
from .report import (
    Report,
    ReportStatus,
    ReportFormat,
    ReportCreate,
    ReportResponse,
    ReportListResponse,
    ReportDetailResponse
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
