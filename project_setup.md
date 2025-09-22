# 员工信息管理系统 - 项目搭建指南

## 项目结构

```
employee-management-system/
├── backend/                 # FastAPI 后端
│   ├── main.py             # 主应用文件
│   ├── requirements.txt    # Python 依赖
│   └── employees.db        # SQLite 数据库（自动生成）
├── frontend/               # React 前端
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
└── README.md
```
---
## 第一阶段：快速启动指南

### 1. 后端 (FastAPI) 搭建

#### 创建后端目录和虚拟环境

```bash
mkdir employee-management-system
cd employee-management-system
mkdir backend
cd backend

# 创建 Python 虚拟环境
python3 -m venv tmmt

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 列出此環境安裝了哪些套件
pip list

# 將目前環境的所有套件連同版本，輸出到一個檔案
# 當開發完成要把程式連同環境 deploy 到雲端 (我是用 azure) 時需要用到此檔案，很重要
pip freeze > requirements.txt

# 離開環境
deactivate

# 砍掉環境：
rm -rf .venv

```

#### 安装依赖 (requirements.txt)

# touch requirements.txt

```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-multipart==0.0.6
```

安装命令：

```bash
pip install -r requirements.txt
```

#### 启动后端服务

```bash
# 将 main.py 代码复制到 backend/main.py
python main.py

# 使用 uvicorn 直接运行 或者代码有修改时 重新装载运行
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端服务将在 http://localhost:8000 启动

- API 文档: http://localhost:8000/docs
- 初始化数据: POST http://localhost:8000/api/init-data

#### Debug启动 用于调试
✅ PyCharm Debug 配置清单
1. 打开菜单 Run → Edit Configurations…
2. 点击左上角 ➕ → 选择 Python
3. 配置项填写：
   - Name: FastAPI Debug （随便取）
     - Script path:
     ```commandline
     /Users/gegedl5215/.pyenv/versions/fastapi-env/bin/uvicorn
     ```
     - Parameters:
     ```commandline
     main:app --reload --host 127.0.0.1 --port 8000
     ```
     - Working directory:
     ```commandline
     /Users/gegedl5215/Documents/Developer/python_study/employee-management-system/backend
     ```
     - Python interpreter:
     ```commandline
     选择 fastapi-env 虚拟环境（路径大概是 /Users/gegedl5215/.pyenv/versions/fastapi-env/bin/python）
     ```
4. 点 Apply → Debug 🐞
---

### 2. 前端 (Vite + React) 搭建

#### 创建 React 项目

```bash
cd ..  # 回到根目录
npm create vite@latest frontend -- --template react
cd frontend
npm install
```

#### 安装额外依赖

```bash
npm install lucide-react
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

#### 配置 Tailwind CSS

**tailwind.config.js:**

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

**src/index.css:**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto",
    sans-serif;
  background-color: #f9fafb;
}
```

#### 替换 App.jsx

将提供的 React 组件代码替换到 `src/App.jsx`

#### 启动前端服务

```bash
npm run dev
```

前端服务将在 http://localhost:5173 启动

## 3. 快速验证

### 启动流程：

1. **启动后端**: `cd backend && python main.py`
2. **启动前端**: `cd frontend && npm run dev`
3. **访问系统**: http://localhost:5173
4. **初始化数据**: 系统会自动调用初始化 API

### 功能验证清单：

- ✅ 首页加载正常，显示企业风格界面
- ✅ 仪表盘数据显示（员工总数、在职员工等）
- ✅ 功能导航卡片显示完整
- ✅ 通知区域显示最新公告
- ✅ 部门统计显示正常
- ✅ 响应式设计在不同屏幕尺寸下正常

## 4. API 接口说明

### 主要 API 端点：

```
GET  /api/dashboard/stats     # 仪表盘统计数据
GET  /api/employees          # 员工列表
POST /api/employees          # 创建员工
GET  /api/employees/{id}     # 获取员工详情
PUT  /api/employees/{id}     # 更新员工
DELETE /api/employees/{id}   # 删除员工
GET  /api/notifications      # 通知列表
GET  /api/departments/stats  # 部门统计
POST /api/init-data         # 初始化示例数据
```

### 测试 API 示例：

```bash
# 获取员工列表
curl http://localhost:8000/api/employees

# 创建新员工
curl -X POST http://localhost:8000/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "EMP005",
    "name": "测试员工",
    "department": "测试部",
    "position": "测试工程师",
    "phone": "13800138000",
    "email": "test@company.com",
    "hire_date": "2024-01-01T00:00:00",
    "status": "active"
  }'
```

## 5. 开发建议

### 学习路径：

1. **熟悉基础功能**: 先运行起来，了解整体架构
2. **学习 API 设计**: 研究 FastAPI 的路由和数据模型
3. **学习前端组件**: 理解 React 组件的状态管理
4. **逐步扩展**: 按模块添加新功能

### 下一步开发计划：

- **员工管理页面**: 员工列表、添加、编辑、删除
- **考勤模块**: 考勤记录、统计分析
- **部门管理**: 部门 CRUD 操作
- **通知系统**: 通知的增删改查
- **用户认证**: JWT 登录认证

### 代码组织建议：

```
backend/
├── main.py           # 主应用
├── models/          # 数据模型
├── routers/         # API 路由
├── database.py      # 数据库配置
└── schemas.py       # Pydantic 模型

frontend/
├── src/
│   ├── components/  # 可复用组件
│   ├── pages/       # 页面组件
│   ├── hooks/       # 自定义 Hooks
│   ├── services/    # API 服务
│   └── utils/       # 工具函数
```

## 6. 常见问题

### 后端问题：

- **CORS 错误**: 确保 FastAPI 的 CORS 配置包含前端地址
- **数据库连接**: SQLite 文件会自动创建，确保有写入权限
- **端口占用**: 修改 main.py 中的端口配置

### 前端问题：

- **API 调用失败**: 检查后端服务是否正常启动
- **样式问题**: 确保 Tailwind CSS 正确配置
- **热重载**: Vite 支持热重载，保存后自动更新

### 开发提示：

- 使用浏览器开发者工具查看网络请求
- 后端 API 文档: http://localhost:8000/docs
- 可以通过 `/docs` 直接测试 API 接口

这个第一阶段的系统已经具备：

- ✨ 专业的企业级 UI 设计
- 🔧 完整的前后端分离架构
- 📊 实时数据展示和统计
- 🎯 模块化的代码结构
- 🚀 易于扩展的设计模式

按照这个指南，你可以快速搭建起一个功能完整的员工管理系统基础版本，然后逐步学习和扩展功能！
