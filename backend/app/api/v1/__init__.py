"""
CheckPaper API v1 路由模块
"""
from fastapi import APIRouter

from .endpoints import documents, health, reports, validation

# 创建 API 路由器
api_router = APIRouter()

# 包含各个端点路由
api_router.include_router(
    documents.router,
    prefix="/documents",
    tags=["文档管理"],
    responses={404: {"description": "未找到"}}
)

api_router.include_router(
    validation.router,
    prefix="/validation",
    tags=["论文验证"],
    responses={404: {"description": "未找到"}}
)

api_router.include_router(
    reports.router,
    prefix="/reports",
    tags=["报告管理"],
    responses={404: {"description": "未找到"}}
)

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["健康检查"]
)
