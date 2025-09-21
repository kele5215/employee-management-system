"""
FastAPI 主应用模块
定义API端点和业务逻辑
"""

from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base, engine, get_session
from models import Employee

# 创建FastAPI应用实例，设置应用标题
app = FastAPI(title="FastAPI + SQLAlchemy (async) 示例")


# 初始化数据库（启动时自动建表）
@app.on_event("startup")
async def on_startup():
    """
    应用启动时的事件处理函数
    用于创建数据库表结构
    
    该函数在应用启动时执行一次，确保所有定义的表都已在数据库中创建。
    使用SQLAlchemy的metadata.create_all方法来创建表。
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    """
    根路径，返回欢迎信息
    
    Returns:
        dict: 包含欢迎信息的字典
    """
    return {"message": "Hello FastAPI with async SQLAlchemy!"}


@app.post("/employees")
async def create_employee(
        name: str,
        department: str = None,
        session: AsyncSession = Depends(get_session)
):
    """
    创建新员工记录
    
    Args:
        name (str): 员工姓名，必须提供且非空
        department (str, optional): 员工所属部门，可选参数
        session (AsyncSession): 数据库会话，通过依赖注入自动获取
        
    Returns:
        Employee: 创建的员工对象，包含员工的ID、姓名和部门信息
    """
    employee = Employee(name=name, department=department)
    session.add(employee)
    await session.commit()
    await session.refresh(employee)
    return employee


@app.get("/employees")
async def list_employees(session: AsyncSession = Depends(get_session)):
    """
    获取所有员工列表
    
    Args:
        session (AsyncSession): 数据库会话，通过依赖注入自动获取
        
    Returns:
        list: 员工信息列表，每个元素包含员工的ID和姓名
    """
    result = await session.execute(text("SELECT id, name FROM employees"))
    return result.mappings().all()
