"""
CheckPaper 文档管理端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlmodel import Session
import os
import uuid
from datetime import datetime

from ....core.config import settings
from ....core.db import get_session
from ....schemas.document import (
    DocumentResponse,
    DocumentListResponse,
    DocumentUploadResponse,
    DocumentTypeEnum
)
from ....services.document import DocumentService
from ....api.deps import (
    get_document_service,
    validate_file_size,
    validate_file_extension,
    get_pagination_params
)


router = APIRouter()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_type: Optional[DocumentTypeEnum] = Form(None),
    title: Optional[str] = Form(None),
    session: Session = Depends(get_session),
    document_service: DocumentService = Depends(get_document_service)
):
    """
    上传论文文档
    
    - **file**: 论文文件（支持 PDF、Word、LaTeX 格式）
    - **document_type**: 文档类型（可选，自动检测）
    - **title**: 文档标题（可选，从文件提取）
    """
    # 验证文件
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")
    
    # 验证文件扩展名
    validate_file_extension(file.filename, settings.allowed_extensions)
    
    # 读取文件内容
    content = await file.read()
    file_size = len(content)
    
    # 验证文件大小
    validate_file_size(file_size, settings.max_upload_size_mb)
    
    # 生成唯一文件名
    file_id = str(uuid.uuid4())
    file_extension = file.filename.rsplit(".", 1)[-1].lower()
    saved_filename = f"{file_id}.{file_extension}"
    file_path = os.path.join(settings.upload_dir, saved_filename)
    
    # 保存文件
    os.makedirs(settings.upload_dir, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(content)
    
    # 获取文档类型
    if document_type is None:
        document_type = _detect_document_type(file_extension)
    
    # 创建文档记录
    document_data = {
        "id": file_id,
        "filename": file.filename,
        "saved_filename": saved_filename,
        "file_path": file_path,
        "file_size": file_size,
        "file_type": document_type,
        "title": title or file.filename,
        "upload_time": datetime.utcnow(),
        "status": "uploaded"
    }
    
    # 保存到数据库
    document = document_service.create_document(session, document_data)
    
    return DocumentUploadResponse(
        id=document.id,
        filename=document.filename,
        file_type=document.file_type,
        file_size=document.file_size,
        upload_time=document.upload_time,
        message="文档上传成功"
    )


@router.get("/", response_model=DocumentListResponse)
async def list_documents(
    session: Session = Depends(get_session),
    document_service: DocumentService = Depends(get_document_service),
    pagination: dict = Depends(get_pagination_params),
    status: Optional[str] = None,
    document_type: Optional[DocumentTypeEnum] = None
):
    """
    获取文档列表
    """
    # 查询文档
    documents = document_service.get_documents(
        session,
        offset=pagination["offset"],
        limit=pagination["page_size"],
        status=status,
        document_type=document_type
    )
    
    # 获取总数
    total = document_service.get_documents_count(
        session,
        status=status,
        document_type=document_type
    )
    
    return DocumentListResponse(
        documents=documents,
        total=total,
        page=pagination["page"],
        page_size=pagination["page_size"]
    )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    session: Session = Depends(get_session),
    document_service: DocumentService = Depends(get_document_service)
):
    """
    获取文档详情
    """
    document = document_service.get_document(session, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="文档未找到")
    
    return document


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    session: Session = Depends(get_session),
    document_service: DocumentService = Depends(get_document_service)
):
    """
    删除文档
    """
    document = document_service.get_document(session, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="文档未找到")
    
    # 删除文件
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    # 删除数据库记录
    document_service.delete_document(session, document_id)
    
    return {"message": "文档删除成功"}


@router.get("/{document_id}/download")
async def download_document(
    document_id: str,
    session: Session = Depends(get_session),
    document_service: DocumentService = Depends(get_document_service)
):
    """
    下载文档
    """
    document = document_service.get_document(session, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="文档未找到")
    
    if not os.path.exists(document.file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        path=document.file_path,
        filename=document.filename,
        media_type="application/octet-stream"
    )


@router.post("/{document_id}/parse")
async def parse_document(
    document_id: str,
    session: Session = Depends(get_session),
    document_service: DocumentService = Depends(get_document_service)
):
    """
    解析文档
    """
    document = document_service.get_document(session, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="文档未找到")
    
    # 解析文档
    parsed_content = document_service.parse_document(session, document_id)
    
    return {
        "document_id": document_id,
        "parsed_content": parsed_content,
        "message": "文档解析完成"
    }


def _detect_document_type(file_extension: str) -> DocumentTypeEnum:
    """
    检测文档类型
    """
    extension_map = {
        "pdf": DocumentTypeEnum.PDF,
        "docx": DocumentTypeEnum.WORD,
        "doc": DocumentTypeEnum.WORD,
        "tex": DocumentTypeEnum.LATEX,
        "latex": DocumentTypeEnum.LATEX,
        "bib": DocumentTypeEnum.BIBTEX
    }
    return extension_map.get(file_extension, DocumentTypeEnum.PDF)
