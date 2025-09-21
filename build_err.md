# Build err  整理

## 1.环境设定Err

### 1-1. PyCharm 报 Unresolved reference 'FastAPI'，这种情况不是 FastAPI 没装，而是 PyCharm 没有正确识别你的虚拟环境解释器

🔹解决步骤（PyCharm 配置虚拟环境）
1. 打开 PyCharm → Preferences（偏好设置，快捷键 ⌘ + ,）
1. 左侧选择：
Project: backend → Python Interpreter
1. 右上角齿轮 ⚙ → Add Interpreter → Add Local Interpreter
1. 选择 Existing environment（已有环境）
1. 路径选择你的 pyenv 虚拟环境里的 Python：

```bash
/Users/gegedl5215/.pyenv/versions/fastapi-env/bin/python
```
1.确认 → 等待 PyCharm 重新索引库

---
## 2. 运行 Err
### 2-1. AttributeError: '_AsyncGeneratorContextManager' object has no attribute 'add'
这里的 session 实际上是一个 async generator，需要通过 Depends 正确解析，或者写法有点问题。
你应该在依赖里 yield 出 session，并且在路由里加上类型标注：
-> AsyncSession: 是关键
```bash
# db.py
from sqlalchemy.ext.asyncio import AsyncSession
from .database import async_session

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

```
---
## 2. 运行 Err

---
## 2. 运行 Err

---
## 2. 运行 Err

---
## 2. 运行 Err