"""
FastAPI 主应用模块
定义API端点和业务逻辑
"""

from fastapi import FastAPI, Depends, HTTPException
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


@app.get("/employees/{employees_id}")
async def get_employees(employees_id:int, session: AsyncSession=Depends(get_session)):
    """
    获取指定员工信息

    Args:
        employees_id (int): 员工ID
        session (AsyncSession): 数据库会话，通过依赖注入自动获取

    Returns:
        Employee: 指定员工对象，包含员工的ID、姓名和部门信息
    """
    result = await session.execute(text("SELECT * FROM employees WHERE id = :id"), {"id": employees_id})
    return result.mappings().first()

@app.post("/employees/{employees_id}")
async def update_employees(employees_id: int, name: str, department: str, session: AsyncSession = Depends(get_session)):
    """
    更新员工信息

    Args:
        employees_id (int): 员工ID
        name (str): 员工姓名
        department (str): 员工部门
        session (AsyncSession): 数据库会话，通过依赖注入自动获取

    Returns:
        Employee: 更新后的员工对象，包含员工的ID、姓名和部门信息
    """
    try:

        # 先确认员工是否存在
        check_result = await session.execute(
            text("SELECT id FROM employees WHERE id = :id"),
            {"id": employees_id}
        )
        # 如果没有找到要更新的记录，抛出404异常
        if not check_result.first():
            raise HTTPException(status_code=404, detail="Employee not found")

        # 更新员工信息
        await session.execute(
            text("UPDATE employees SET name = :name, department = :department WHERE id = :id"),
            {"id": employees_id, "name": name, "department": department}
        )

        # 提交事务
        await session.commit()
        
        # 获取更新后的员工信息
        updated_result = await session.execute(
            text("SELECT * FROM employees WHERE id = :id"),
            {"id": employees_id}
        )
        
        return updated_result.mappings().first()
    
    except Exception as e:
        # 出现错误时回滚事务
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating employee: {str(e)}")

@app.delete("/employees/{employees_id}")
async def delete_employees(employees_id: int, session: AsyncSession = Depends(get_session)):
    """
    删除员工信息

    Args:
        employees_id (int): 员工ID
        session (AsyncSession): 数据库会话，通过依赖注入自动获取

    Returns:
        dict: 删除结果信息，包含成功消息
        
    Raises:
        HTTPException: 当员工不存在或删除过程中发生错误时抛出异常
    """
    try:
        # 先确认员工是否存在
        check_result = await session.execute(
            text("SELECT id FROM employees WHERE id = :employees_id"),
            {"employees_id": employees_id}
        )

        # 如果查询结果为空，说明员工不存在，抛出404异常
        if not check_result.first():
            raise HTTPException(status_code=404, detail="Employee not found")

        # 执行删除操作
        delete_result = await session.execute(
            text("DELETE FROM employees WHERE id = :employees_id"),
            {"employees_id": employees_id}
        )
        # 提交事务以确保更改被保存到数据库
        await session.commit()
        
        # 返回删除成功的消息
        return {"message": "Employee deleted successfully"}
    except Exception as e:
        # 发生异常时回滚事务
        await session.rollback()
        # 抛出500异常，包含具体的错误信息
        raise HTTPException(status_code=500, detail=f"Error deleting employee: {str(e)}")
