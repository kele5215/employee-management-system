"""
数据模型模块
定义数据库表结构和模型
"""

from sqlalchemy import Column, Integer, String
from database import Base


class Employee(Base):
    """
    员工数据模型
    对应数据库中的employees表
    
    Attributes:
        id (Integer): 员工唯一标识符，主键
        name (String): 员工姓名
        department (String): 员工所属部门
    """
    __tablename__ = "employees"

    # 员工ID，主键
    id = Column(Integer, primary_key=True, index=True)
    # 员工姓名
    name = Column(String, index=True)
    # 员工部门
    department = Column(String, index=True)
