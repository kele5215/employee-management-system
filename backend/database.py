"""
数据库配置模块
用于配置SQLAlchemy异步数据库连接
"""

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# 数据库连接URL，使用SQLite异步数据库
DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

# 创建异步数据库引擎，echo=True 表示输出 SQL 语句到控制台，future=True 表示使用 SQLAlchemy 2.0 特性
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# 创建声明式基类，用于模型继承
Base = declarative_base()

# 创建异步会话工厂
# bind: 绑定的引擎
# class_: 指定会话类为异步会话
# expire_on_commit: 提交后不使实例过期
# autoflush: 禁止自动刷新
# autocommit: 禁止自动提交
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)


# FastAPI 依赖：获取一个异步数据库会话
async def get_session() -> AsyncGenerator[AsyncSession | Any, Any]:
    """
    异步上下文管理器，用于获取数据库会话
    
    Yields:
        AsyncSession: 异步数据库会话对象
    """
    async with AsyncSessionLocal() as session:
        yield session
