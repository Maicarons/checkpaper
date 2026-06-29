"""
CheckPaper FastAPI 应用入口
"""
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .api.v1 import api_router
from .core.config import settings
from .core.db import init_db

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    在应用启动和关闭时执行初始化和清理操作
    """
    # 启动时执行
    logger.info("正在启动 CheckPaper 应用...")

    # 初始化数据库
    try:
        init_db()
        logger.info("数据库初始化成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise

    # 创建必要的目录
    import os
    os.makedirs(settings.upload_dir, exist_ok=True)
    os.makedirs(settings.report_output_dir, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    logger.info("CheckPaper 应用启动完成")

    yield

    # 关闭时执行
    logger.info("正在关闭 CheckPaper 应用...")
    # 这里可以添加清理逻辑
    logger.info("CheckPaper 应用已关闭")


# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI论文验证智能体系统",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)


# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 请求处理时间中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """添加请求处理时间头"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# 全局异常处理器
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """HTTP 异常处理器"""
    logger.warning(f"HTTP 异常: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "http_error",
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """请求验证异常处理器"""
    logger.warning(f"验证错误: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "detail": exc.errors(),
            "body": exc.body
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器"""
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "detail": "服务器内部错误"
        }
    )


# 包含 API 路由
app.include_router(api_router, prefix=settings.api_v1_prefix)


# 根路由
@app.get("/")
async def root():
    """根路由"""
    return {
        "message": "欢迎使用 CheckPaper - AI论文验证智能体系统",
        "version": settings.app_version,
        "docs": "/docs"
    }


# 健康检查路由
@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "timestamp": time.time()
    }


# 应用信息路由
@app.get("/info")
async def app_info():
    """应用信息"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
        "database": settings.database_url.split("://")[0] if "://" in settings.database_url else "unknown"
    }
