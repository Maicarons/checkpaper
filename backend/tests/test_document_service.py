"""
文档服务测试
"""
import pytest
from sqlmodel import Session

from backend.app.schemas.document import DocumentStatusEnum, DocumentTypeEnum
from backend.app.services.document import DocumentService


@pytest.fixture
def document_service():
    return DocumentService()


def test_create_document(session: Session, document_service: DocumentService):
    """测试创建文档"""
    doc_data = {
        "id": "test-doc-1",
        "filename": "test.pdf",
        "saved_filename": "test-doc-1.pdf",
        "file_path": "/uploads/test-doc-1.pdf",
        "file_size": 1024,
        "file_type": DocumentTypeEnum.PDF,
        "title": "Test Document",
        "status": DocumentStatusEnum.UPLOADED,
    }

    document = document_service.create_document(session, doc_data)
    assert document.id == "test-doc-1"
    assert document.filename == "test.pdf"
    assert document.file_type == DocumentTypeEnum.PDF


def test_get_document(session: Session, document_service: DocumentService):
    """测试获取文档"""
    # 先创建文档
    doc_data = {
        "id": "test-doc-2",
        "filename": "test2.pdf",
        "saved_filename": "test-doc-2.pdf",
        "file_path": "/uploads/test-doc-2.pdf",
        "file_size": 2048,
        "file_type": DocumentTypeEnum.PDF,
        "title": "Test Document 2",
    }
    document_service.create_document(session, doc_data)

    # 获取文档
    document = document_service.get_document(session, "test-doc-2")
    assert document is not None
    assert document.filename == "test2.pdf"


def test_get_document_not_found(session: Session, document_service: DocumentService):
    """测试获取不存在的文档"""
    document = document_service.get_document(session, "nonexistent")
    assert document is None


def test_get_documents_list(session: Session, document_service: DocumentService):
    """测试获取文档列表"""
    # 创建多个文档
    for i in range(3):
        doc_data = {
            "id": f"test-doc-list-{i}",
            "filename": f"test{i}.pdf",
            "saved_filename": f"test-doc-list-{i}.pdf",
            "file_path": f"/uploads/test-doc-list-{i}.pdf",
            "file_size": 1024 * (i + 1),
            "file_type": DocumentTypeEnum.PDF,
            "title": f"Test Document {i}",
        }
        document_service.create_document(session, doc_data)

    # 获取文档列表
    documents = document_service.get_documents(session, offset=0, limit=10)
    assert len(documents) >= 3


def test_update_document_status(session: Session, document_service: DocumentService):
    """测试更新文档状态"""
    # 先创建文档
    doc_data = {
        "id": "test-doc-status",
        "filename": "test-status.pdf",
        "saved_filename": "test-doc-status.pdf",
        "file_path": "/uploads/test-doc-status.pdf",
        "file_size": 1024,
        "file_type": DocumentTypeEnum.PDF,
        "title": "Test Status Document",
    }
    document_service.create_document(session, doc_data)

    # 更新状态
    document = document_service.update_document_status(
        session, "test-doc-status", DocumentStatusEnum.PARSED
    )
    assert document is not None
    assert document.status == DocumentStatusEnum.PARSED
    assert document.parsed_time is not None


def test_delete_document(session: Session, document_service: DocumentService):
    """测试删除文档"""
    # 先创建文档
    doc_data = {
        "id": "test-doc-delete",
        "filename": "test-delete.pdf",
        "saved_filename": "test-doc-delete.pdf",
        "file_path": "/uploads/test-doc-delete.pdf",
        "file_size": 1024,
        "file_type": DocumentTypeEnum.PDF,
        "title": "Test Delete Document",
    }
    document_service.create_document(session, doc_data)

    # 删除文档
    result = document_service.delete_document(session, "test-doc-delete")
    assert result is True

    # 确认已删除
    document = document_service.get_document(session, "test-doc-delete")
    assert document is None
