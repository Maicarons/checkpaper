"""
CheckPaper 报告管理端点
"""
import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Session

from ....api.deps import get_pagination_params, get_report_service
from ....core.db import get_session
from ....schemas.report import ReportListResponse, ReportResponse
from ....services.report import ReportService

router = APIRouter()


@router.get("/", response_model=ReportListResponse)
async def list_reports(
    session: Session = Depends(get_session),
    report_service: ReportService = Depends(get_report_service),
    pagination: dict = Depends(get_pagination_params),
    document_id: str | None = None
):
    """
    获取报告列表
    """
    reports = report_service.get_reports(
        session,
        offset=pagination["offset"],
        limit=pagination["page_size"],
        document_id=document_id
    )
    total = report_service.get_reports_count(session, document_id=document_id)

    return ReportListResponse(
        reports=reports,
        total=total,
        page=pagination["page"],
        page_size=pagination["page_size"]
    )


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    session: Session = Depends(get_session),
    report_service: ReportService = Depends(get_report_service)
):
    """
    获取报告详情
    """
    report = report_service.get_report(session, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="报告未找到")
    return report


@router.get("/{report_id}/download")
async def download_report(
    report_id: str,
    format: str = "md",
    session: Session = Depends(get_session),
    report_service: ReportService = Depends(get_report_service)
):
    """
    下载报告
    - **format**: 下载格式 (md, pdf, html)
    """
    report = report_service.get_report(session, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="报告未找到")

    # 根据格式生成报告文件
    file_path = report_service.export_report(session, report_id, format)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="报告文件不存在")

    media_types = {
        "md": "text/markdown",
        "pdf": "application/pdf",
        "html": "text/html"
    }

    return FileResponse(
        path=file_path,
        filename=f"report_{report_id}.{format}",
        media_type=media_types.get(format, "application/octet-stream")
    )


@router.delete("/{report_id}")
async def delete_report(
    report_id: str,
    session: Session = Depends(get_session),
    report_service: ReportService = Depends(get_report_service)
):
    """
    删除报告
    """
    report = report_service.get_report(session, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="报告未找到")

    report_service.delete_report(session, report_id)
    return {"message": "报告删除成功"}
