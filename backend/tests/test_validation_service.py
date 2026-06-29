"""
验证服务测试
"""
import pytest
from sqlmodel import Session

from backend.app.services.validation import ValidationService
from backend.app.schemas.validation import (
    ValidationTypeEnum,
    ValidationStatus,
    IssueSeverity,
)


@pytest.fixture
def validation_service():
    return ValidationService()


def test_create_validation_task(session: Session, validation_service: ValidationService):
    """测试创建验证任务"""
    task = validation_service.create_validation_task(
        session,
        document_id="test-doc-1",
        validation_types=[ValidationTypeEnum.FORMAT, ValidationTypeEnum.CITATION],
        options={"test": True}
    )
    
    assert task.id is not None
    assert task.document_id == "test-doc-1"
    assert task.status == ValidationStatus.PENDING


def test_get_validation_task(session: Session, validation_service: ValidationService):
    """测试获取验证任务"""
    # 先创建任务
    task = validation_service.create_validation_task(
        session,
        document_id="test-doc-2",
        validation_types=[ValidationTypeEnum.FORMAT],
    )
    
    # 获取任务
    retrieved_task = validation_service.get_validation_task(session, task.id)
    assert retrieved_task is not None
    assert retrieved_task.document_id == "test-doc-2"


def test_update_task_status(session: Session, validation_service: ValidationService):
    """测试更新任务状态"""
    # 先创建任务
    task = validation_service.create_validation_task(
        session,
        document_id="test-doc-3",
        validation_types=[ValidationTypeEnum.FORMAT],
    )
    
    # 更新状态为运行中
    updated_task = validation_service.update_task_status(
        session, task.id, ValidationStatus.RUNNING
    )
    assert updated_task is not None
    assert updated_task.status == ValidationStatus.RUNNING
    assert updated_task.started_at is not None
    
    # 更新状态为完成
    completed_task = validation_service.update_task_status(
        session, task.id, ValidationStatus.COMPLETED
    )
    assert completed_task.status == ValidationStatus.COMPLETED
    assert completed_task.completed_at is not None


def test_cancel_validation_task(session: Session, validation_service: ValidationService):
    """测试取消验证任务"""
    # 先创建任务
    task = validation_service.create_validation_task(
        session,
        document_id="test-doc-4",
        validation_types=[ValidationTypeEnum.FORMAT],
    )
    
    # 取消任务
    result = validation_service.cancel_validation_task(session, task.id)
    assert result is True
    
    # 确认已取消
    cancelled_task = validation_service.get_validation_task(session, task.id)
    assert cancelled_task.status == ValidationStatus.CANCELLED


def test_get_validation_tasks_list(session: Session, validation_service: ValidationService):
    """测试获取验证任务列表"""
    # 创建多个任务
    for i in range(3):
        validation_service.create_validation_task(
            session,
            document_id=f"test-doc-list-{i}",
            validation_types=[ValidationTypeEnum.FORMAT],
        )
    
    # 获取任务列表
    tasks = validation_service.get_validation_tasks(session, offset=0, limit=10)
    assert len(tasks) >= 3
