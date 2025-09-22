# 根据您的项目结构，我为您提供 GitHub 上传的完整方案

## .gitignore 文件内容
```bash
在项目根目录创建 .gitignore 文件：
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Database
*.db
*.sqlite
*.sqlite3

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Test
.coverage
htmlcov/
.pytest_cache/

# Build
/build/
/dist/
```
---
## Git Commit规范
规定格式如下：
type用于说明 commit 的类别:
<type>(<scope>): <subject> #issue_number
<description>

- type(必须)取值说明
  - feat: (feature)增加新功能
  - fix: 修补bug
  - docs: 文档（documentation）， 只改动了文档相关的内容
  - style: 不影响代码含义的改动，例如去掉空格、改变缩进、增删分号
  - build: 构造工具的或者外部依赖的改动，例如webpack，npm
  - refactor: 代码重构时使用
  - revert：回滚到上一个版本,执行git revert打印的message
  - test: 添加测试或者修改现有测试
  - pref: 提高性能的改动
  - chore: 不修改src或者test的其余修改，例如构建过程或辅助工具的变动
  - merge：代码合并
  - sync：同步主线或分支的Bug
  - ci: 与CI（持续集成服务）有关的改动
  
- scope(可选)取值说明
  - scope用于说明 commit影响的范围，比如数据层、控制层、视图层等等，视项目不同而不同
```commandline
fix(DAO):用户查询缺少username属性 
feat(Controller):用户查询接口开发
```
---
## 创建 GitHub 仓库并上传项目
### 步骤 1：初始化 Git 仓库
```bash
# 进入项目根目录
cd /path/to/your/project

# 初始化 Git
git init

# 添加 .gitignore 文件
# 将上面的内容保存为 .gitignore 文件
```
### 步骤 2：添加文件到暂存区
```bash
# 添加所有文件（除了 .gitignore 中忽略的）
git add .

# 或者逐个添加重要文件
git add backend/
git add *.md
git add .gitignore
```
### 步骤 3：提交更改
```bash
# 首次提交
git commit -m "Initial commit: FastAPI backend project setup"

# 或者更详细的提交信息
git commit -m "feat: initial project setup
- Add FastAPI backend with database models
- Include requirements and documentation
- Add proper gitignore for Python projects"
```
### 步骤 4：在 GitHub 创建仓库
1. 登录 GitHub
1. 点击 "New repository"
1. 仓库名：employee-management-system
1. 选择 Public 或 Private
1. 不要初始化 README、.gitignore 或 license（因为我们已经有了）

### 步骤 5：连接远程仓库并推送
```bash
# 添加远程仓库（替换 YOUR_USERNAME 和 YOUR_REPO_NAME）
git remote add origin https://github.com/kele5215/employee-management-system.git
# 推送代码到 main 分支
git branch -M main
git push -u origin main
```
### 步骤 6：文件有修改时再提交并推送
命令如下
```bash
git status
git add git_command_first.md
git commit -m "update git_command_first.md"
git push
```
或者使用桌面工具

### 步骤 7：从main或者master 创建新的分支
```bash
git checkout -b new_branch
git checkout -b feature_20250922_issues001 origin/feature_20250922_issues001
# 确认 分支切换
git status
git branch
```