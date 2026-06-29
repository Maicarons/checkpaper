"""
CheckPaper 论文验证端点
"""

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session

from ....api.deps import (
    get_agent_service,
    get_pagination_params,
    get_validation_service,
)
from ....core.db import get_session
from ....schemas.validation import (
    ValidationRequest,
    ValidationResponse,
    ValidationStatus,
    ValidationTypeEnum,
)
from ....services.agent import AgentService
from ....services.validation import ValidationService

router = APIRouter()


@router.post("/start", response_model=ValidationResponse)
async def start_validation(
    request: ValidationRequest,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    validation_service: ValidationService = Depends(get_validation_service),
    agent_service: AgentService = Depends(get_agent_service)
):
    """
    开始论文验证

    - **document_id**: 文档ID
    - **validation_types**: 验证类型列表
    - **options**: 验证选项
    """
    # 检查文档是否存在
    document = validation_service.get_document(session, request.document_id)
    if not document:
        raise HTTPException(status_code=404, detail="文档未找到")

    # 创建验证任务
    validation_task = validation_service.create_validation_task(
        session,
        document_id=request.document_id,
        validation_types=request.validation_types,
        options=request.options
    )

    # 在后台执行验证
    background_tasks.add_task(
        _run_validation_background,
        task_id=validation_task.id,
        document_id=request.document_id,
        validation_types=request.validation_types,
        options=request.options or {}
    )

    return ValidationResponse(
        task_id=validation_task.id,
        document_id=request.document_id,
        status=validation_task.status,
        message="验证任务已创建，正在后台执行",
        created_at=validation_task.created_at
    )


@router.get("/tasks")
async def list_validation_tasks(
    session: Session = Depends(get_session),
    validation_service: ValidationService = Depends(get_validation_service),
    pagination: dict = Depends(get_pagination_params),
    document_id: str | None = None,
    status: ValidationStatus | None = None
):
    """
    获取验证任务列表
    """
    tasks = validation_service.get_validation_tasks(
        session,
        offset=pagination["offset"],
        limit=pagination["page_size"],
        document_id=document_id,
        status=status
    )

    # 转换为响应格式
    return [
        {
            "task_id": task.id,
            "document_id": task.document_id,
            "status": task.status,
            "message": "任务已完成" if task.status == ValidationStatus.COMPLETED else "任务进行中",
            "created_at": task.created_at,
            "started_at": task.started_at,
            "completed_at": task.completed_at
        }
        for task in tasks
    ]


@router.get("/tasks/{task_id}", response_model=ValidationResponse)
async def get_validation_task(
    task_id: str,
    session: Session = Depends(get_session),
    validation_service: ValidationService = Depends(get_validation_service)
):
    """
    获取验证任务详情
    """
    task = validation_service.get_validation_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="验证任务未找到")

    return task


@router.get("/tasks/{task_id}/results")
async def get_validation_results(
    task_id: str,
    session: Session = Depends(get_session),
    validation_service: ValidationService = Depends(get_validation_service)
):
    """
    获取验证结果
    """
    task = validation_service.get_validation_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="验证任务未找到")

    if task.status != ValidationStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail=f"验证任务尚未完成，当前状态: {task.status}"
        )

    results = validation_service.get_validation_results(session, task_id)
    return results


@router.post("/tasks/{task_id}/cancel")
async def cancel_validation_task(
    task_id: str,
    session: Session = Depends(get_session),
    validation_service: ValidationService = Depends(get_validation_service)
):
    """
    取消验证任务
    """
    task = validation_service.get_validation_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="验证任务未找到")

    if task.status in [ValidationStatus.COMPLETED, ValidationStatus.CANCELLED]:
        raise HTTPException(
            status_code=400,
            detail=f"无法取消当前状态的任务: {task.status}"
        )

    # 取消任务
    validation_service.cancel_validation_task(session, task_id)

    return {"message": "验证任务已取消"}


@router.post("/quick")
async def quick_validation(
    document_id: str,
    validation_types: list[ValidationTypeEnum] | None = None,
    session: Session = Depends(get_session),
    validation_service: ValidationService = Depends(get_validation_service),
    agent_service: AgentService = Depends(get_agent_service)
):
    """
    快速验证（同步执行）
    """
    # 检查文档是否存在
    document = validation_service.get_document(session, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="文档未找到")

    # 设置默认验证类型
    if validation_types is None:
        validation_types = list(ValidationTypeEnum)

    # 执行验证
    try:
        results = await agent_service.run_validation(
            document_id=document_id,
            validation_types=validation_types,
            options={}
        )

        return results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"验证执行失败: {str(e)}"
        ) from e


@router.get("/types", response_model=list[dict])
async def get_validation_types():
    """
    获取支持的验证类型列表
    """
    return [
        {
            "type": ValidationTypeEnum.FORMAT,
            "name": "格式检查",
            "description": "检查论文格式、结构、目录对应关系"
        },
        {
            "type": ValidationTypeEnum.FIGURE_TABLE,
            "name": "图表引用检查",
            "description": "检查图片、表格是否在文中被显式引用"
        },
        {
            "type": ValidationTypeEnum.CITATION,
            "name": "参考文献引用检查",
            "description": "检查参考文献是否在文中被引用"
        },
        {
            "type": ValidationTypeEnum.DATA_SOURCE,
            "name": "数据来源验证",
            "description": "验证论文中数据来源的真实性"
        },
        {
            "type": ValidationTypeEnum.DATA_PROCESSING,
            "name": "数据处理验证",
            "description": "验证论文数据处理的真实性"
        },
        {
            "type": ValidationTypeEnum.REFERENCE,
            "name": "参考文献验证",
            "description": "验证参考文献的真实性（联网搜索）"
        }
    ]


async def _run_validation_background(
    task_id: str,
    document_id: str,
    validation_types: list[ValidationTypeEnum],
    options: dict
):
    """
    后台执行验证任务
    """
    from ....core.db import SessionLocal

    session = SessionLocal()
    try:
        validation_service = ValidationService()
        agent_service = AgentService()

        # 更新任务状态为执行中
        validation_service.update_task_status(
            session, task_id, ValidationStatus.RUNNING
        )

        # 执行验证
        results = await agent_service.run_validation(
            document_id=document_id,
            validation_types=validation_types,
            options=options
        )

        # 保存结果
        validation_service.save_validation_results(
            session, task_id, results
        )

        # 更新任务状态为完成
        validation_service.update_task_status(
            session, task_id, ValidationStatus.COMPLETED
        )

    except Exception as e:
        # 更新任务状态为失败
        validation_service.update_task_status(
            session, task_id, ValidationStatus.FAILED,
            error_message=str(e)
        )
        raise
    finally:
        session.close()
