"""
CheckPaper API 依赖注入模块
定义所有 API 端点的共享依赖项
"""
from fastapi import HTTPException, status


# 依赖函数
def get_document_service():
    """获取文档服务实例"""
    from ..services.document import DocumentService
    return DocumentService()


def get_validation_service():
    """获取验证服务实例"""
    from ..services.validation import ValidationService
    return ValidationService()


def get_agent_service():
    """获取 Agent 服务实例"""
    from ..services.agent import AgentService
    return AgentService()


def get_report_service():
    """获取报告服务实例"""
    from ..services.report import ReportService
    return ReportService()


def validate_file_size(file_size: int, max_size_mb: int = 50) -> bool:
    """
    验证文件大小
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"文件大小超过限制。最大允许 {max_size_mb}MB"
        )
    return True


def validate_file_extension(filename: str, allowed_extensions: list | None = None) -> bool:
    """
    验证文件扩展名
    """
    if allowed_extensions is None:
        allowed_extensions = ["pdf", "docx", "doc", "tex", "latex", "bib"]

    if not filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件名不能为空"
        )

    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件类型。允许的类型: {', '.join(allowed_extensions)}"
        )

    return True


def get_pagination_params(
    page: int = 1,
    page_size: int = 20
) -> dict:
    """
    获取分页参数
    """
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 20
    if page_size > 100:
        page_size = 100

    return {
        "page": page,
        "page_size": page_size,
        "offset": (page - 1) * page_size
    }
