"""
CheckPaper 安全模块
包含认证、授权和安全相关的功能
"""
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session

from .config import settings
from .db import get_session

# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer 认证
security = HTTPBearer()


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    """
    创建访问令牌

    Args:
        data: 令牌数据
        expires_delta: 过期时间间隔

    Returns:
        JWT 令牌字符串
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str) -> dict | None:
    """
    验证令牌

    Args:
        token: JWT 令牌

    Returns:
        令牌数据或 None
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return payload
    except JWTError:
        return None


def get_password_hash(password: str) -> str:
    """
    获取密码哈希

    Args:
        password: 原始密码

    Returns:
        哈希后的密码
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码

    Args:
        plain_password: 原始密码
        hashed_password: 哈希后的密码

    Returns:
        密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """
    获取当前认证用户（依赖注入）

    Args:
        credentials: HTTP 认证凭据
        session: 数据库会话

    Returns:
        当前用户对象

    Raises:
        HTTPException: 认证失败时抛出
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        payload = verify_token(token)
        if payload is None:
            raise credentials_exception

        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception from None

    # 这里可以添加从数据库获取用户的逻辑
    # user = get_user_by_id(session, user_id)
    # if user is None:
    #     raise credentials_exception
    # return user

    # 暂时返回用户ID
    return {"user_id": user_id}


def check_permissions(required_permissions: list):
    """
    权限检查装饰器

    Args:
        required_permissions: 需要的权限列表

    Returns:
        依赖函数
    """
    async def permission_checker(
        current_user: dict = Depends(get_current_user)
    ):
        # 这里可以添加权限检查逻辑
        # user_permissions = get_user_permissions(current_user["user_id"])
        # for permission in required_permissions:
        #     if permission not in user_permissions:
        #         raise HTTPException(
        #             status_code=status.HTTP_403_FORBIDDEN,
        #             detail="权限不足"
        #         )
        return current_user

    return permission_checker
