"""
CheckPaper 健康检查端点
"""
import platform
from datetime import datetime

import psutil
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    """
    基础健康检查
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0"
    }


@router.get("/detailed")
async def detailed_health_check():
    """
    详细健康检查
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0",
        "system": {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "memory_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
            "disk_usage_percent": psutil.disk_usage('/').percent if platform.system() != 'Windows' else psutil.disk_usage('C:').percent
        }
    }
