"""
CheckPaper 验证服务模块
"""
import json
import uuid
from datetime import datetime
from typing import List, Optional

from sqlmodel import Session, select

from ...schemas.document import Document
from ...schemas.validation import (
    IssueResponse,
    IssueSeverity,
    ValidationFullResult,
    ValidationIssue,
    ValidationResult,
    ValidationResultResponse,
    ValidationStatus,
    ValidationTask,
    ValidationTypeEnum,
)


class ValidationService:
    """验证服务类"""

    def get_document(self, session: Session, document_id: str) -> Document | None:
        """获取文档"""
        statement = select(Document).where(Document.id == document_id)
        return session.exec(statement).first()

    def create_validation_task(
        self,
        session: Session,
        document_id: str,
        validation_types: list[ValidationTypeEnum],
        options: dict | None = None
    ) -> ValidationTask:
        """
        创建验证任务

        Args:
            session: 数据库会话
            document_id: 文档ID
            validation_types: 验证类型列表
            options: 验证选项

        Returns:
            创建的验证任务
        """
        task = ValidationTask(
            id=str(uuid.uuid4()),
            document_id=document_id,
            validation_types=json.dumps([vt.value for vt in validation_types]),
            options=json.dumps(options) if options else None,
            status=ValidationStatus.PENDING,
            created_at=datetime.utcnow()
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    def get_validation_task(self, session: Session, task_id: str) -> ValidationTask | None:
        """获取验证任务"""
        statement = select(ValidationTask).where(ValidationTask.id == task_id)
        return session.exec(statement).first()

    def get_validation_tasks(
        self,
        session: Session,
        offset: int = 0,
        limit: int = 20,
        document_id: str | None = None,
        status: ValidationStatus | None = None
    ) -> list[ValidationTask]:
        """获取验证任务列表"""
        statement = select(ValidationTask)

        if document_id:
            statement = statement.where(ValidationTask.document_id == document_id)
        if status:
            statement = statement.where(ValidationTask.status == status)

        statement = statement.offset(offset).limit(limit).order_by(ValidationTask.created_at.desc())
        return list(session.exec(statement).all())

    def update_task_status(
        self,
        session: Session,
        task_id: str,
        status: ValidationStatus,
        error_message: str | None = None
    ) -> ValidationTask | None:
        """更新任务状态"""
        task = self.get_validation_task(session, task_id)
        if not task:
            return None

        task.status = status
        if status == ValidationStatus.RUNNING:
            task.started_at = datetime.utcnow()
        elif status in [ValidationStatus.COMPLETED, ValidationStatus.FAILED, ValidationStatus.CANCELLED]:
            task.completed_at = datetime.utcnow()

        if error_message:
            task.error_message = error_message

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    def cancel_validation_task(self, session: Session, task_id: str) -> bool:
        """取消验证任务"""
        task = self.get_validation_task(session, task_id)
        if not task:
            return False

        task.status = ValidationStatus.CANCELLED
        task.completed_at = datetime.utcnow()
        session.add(task)
        session.commit()
        return True

    def get_validation_results(self, session: Session, task_id: str) -> ValidationFullResult:
        """获取验证结果"""
        task = self.get_validation_task(session, task_id)
        if not task:
            raise ValueError("验证任务不存在")

        # 获取所有结果
        statement = select(ValidationResult).where(ValidationResult.task_id == task_id)
        results = list(session.exec(statement).all())

        # 统计问题数量
        total_issues = 0
        critical_issues = 0
        warning_issues = 0
        info_issues = 0

        result_responses = []
        for result in results:
            # 获取问题列表
            issue_statement = select(ValidationIssue).where(ValidationIssue.result_id == result.id)
            issues = list(session.exec(issue_statement).all())

            issue_responses = [
                IssueResponse(
                    id=issue.id,
                    severity=issue.severity,
                    category=issue.category,
                    title=issue.title,
                    description=issue.description,
                    location=issue.location,
                    suggestion=issue.suggestion
                )
                for issue in issues
            ]

            result_response = ValidationResultResponse(
                id=result.id,
                validation_type=result.validation_type,
                status=result.status,
                issues_count=result.issues_count,
                critical_count=result.critical_count,
                warning_count=result.warning_count,
                info_count=result.info_count,
                summary=result.summary,
                issues=issue_responses
            )
            result_responses.append(result_response)

            total_issues += result.issues_count
            critical_issues += result.critical_count
            warning_issues += result.warning_count
            info_issues += result.info_count

        return ValidationFullResult(
            task_id=task.id,
            document_id=task.document_id,
            status=task.status,
            total_issues=total_issues,
            critical_issues=critical_issues,
            warning_issues=warning_issues,
            info_issues=info_issues,
            results=result_responses,
            created_at=task.created_at,
            completed_at=task.completed_at
        )

    def save_validation_results(
        self,
        session: Session,
        task_id: str,
        results: dict
    ) -> None:
        """保存验证结果"""
        for validation_type, result_data in results.items():
            # 创建结果记录
            result = ValidationResult(
                id=str(uuid.uuid4()),
                task_id=task_id,
                validation_type=validation_type,
                status=ValidationStatus.COMPLETED,
                issues_count=result_data.get("issues_count", 0),
                critical_count=result_data.get("critical_count", 0),
                warning_count=result_data.get("warning_count", 0),
                info_count=result_data.get("info_count", 0),
                summary=result_data.get("summary", ""),
                details=json.dumps(result_data.get("details", {})),
                created_at=datetime.utcnow()
            )
            session.add(result)
            session.flush()

            # 保存问题
            for issue_data in result_data.get("issues", []):
                issue = ValidationIssue(
                    id=str(uuid.uuid4()),
                    result_id=result.id,
                    severity=issue_data.get("severity", IssueSeverity.INFO),
                    category=issue_data.get("category", ""),
                    title=issue_data.get("title", ""),
                    description=issue_data.get("description", ""),
                    location=issue_data.get("location"),
                    suggestion=issue_data.get("suggestion"),
                    created_at=datetime.utcnow()
                )
                session.add(issue)

        session.commit()
