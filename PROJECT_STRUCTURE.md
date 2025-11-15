# 📂 项目结构说明

## 文件清单

```
Station F/
│
├── app.py                          # Streamlit 前端应用主文件
│   └── 功能: 用户界面、文件上传、播客展示
│
├── backend/                        # FastAPI 后端目录
│   ├── __init__.py                # 包初始化文件
│   ├── main.py                    # FastAPI 主应用和路由
│   ├── models.py                  # Pydantic 数据模型
│   ├── db.py                      # SQLite 数据库管理
│   └── storage.py                 # 文件存储管理（本地+云存储占位符）
│
├── storage/                        # 文件存储目录（自动创建）
│   ├── audio/                     # 音频文件存储
│   │   └── .gitkeep
│   └── images/                    # 图片文件存储
│       └── .gitkeep
│
├── requirements.txt                # Python 依赖包列表
├── README.md                       # 项目主文档
├── QUICKSTART.md                   # 快速启动指南
├── PROJECT_STRUCTURE.md            # 本文件 - 项目结构说明
├── .gitignore                      # Git 忽略文件配置
│
├── start_backend.bat               # Windows 后端启动脚本
├── start_frontend.bat              # Windows 前端启动脚本
├── start_backend.sh                # Linux/Mac 后端启动脚本
└── start_frontend.sh               # Linux/Mac 前端启动脚本
```

## 核心文件详解

### 前端 (Frontend)

#### `app.py`
- **作用**: Streamlit Web 应用主入口
- **功能**:
  - 📤 文件上传界面（音频和封面图片）
  - 📝 播客元数据输入（标题、描述）
  - 👁️ 预览功能（图片和音频）
  - 🚀 发布到后端 API
  - 📚 展示所有播客列表
  - 🎵 在线播放音频

### 后端 (Backend)

#### `backend/main.py`
- **作用**: FastAPI 应用核心
- **功能**:
  - `POST /api/episodes` - 接收和处理上传
  - `GET /api/episodes` - 获取所有播客
  - `GET /api/episodes/{id}` - 获取单个播客
  - `DELETE /api/episodes/{id}` - 删除播客
  - CORS 配置
  - 静态文件服务

#### `backend/models.py`
- **作用**: 数据模型定义
- **内容**:
  - `EpisodeResponse` - 播客响应模型
  - `EpisodeListResponse` - 播客列表模型
  - `ErrorResponse` - 错误响应模型

#### `backend/db.py`
- **作用**: SQLite 数据库管理
- **功能**:
  - 数据库连接管理
  - 自动创建 `episodes` 表
  - 数据库初始化和重置

#### `backend/storage.py`
- **作用**: 文件存储管理
- **功能**:
  - 本地文件保存（默认）
  - 文件验证（类型、大小）
  - 文件名清理（安全性）
  - 云存储占位符:
    - `save_file_s3()` - AWS S3
    - `save_file_supabase()` - Supabase Storage
    - `save_file_github()` - GitHub Repository
    - `save_file_gcp()` - Google Cloud Storage

### 配置和文档

#### `requirements.txt`
- **作用**: Python 依赖包清单
- **内容**:
  - FastAPI 和相关库
  - Streamlit
  - 可选云存储 SDK（注释状态）

#### `README.md`
- **作用**: 项目主文档
- **内容**:
  - 项目介绍和特性
  - 完整安装和使用说明
  - API 文档
  - 配置选项
  - 故障排除

#### `QUICKSTART.md`
- **作用**: 快速启动指南
- **内容**: 简化的启动步骤和脚本使用说明

### 启动脚本

#### Windows 批处理文件
- `start_backend.bat` - 启动 FastAPI 后端
- `start_frontend.bat` - 启动 Streamlit 前端

#### Linux/Mac Shell 脚本
- `start_backend.sh` - 启动 FastAPI 后端
- `start_frontend.sh` - 启动 Streamlit 前端

## 运行时生成的文件

- `podcasts.db` - SQLite 数据库文件（首次运行时自动创建）
- `storage/audio/*` - 上传的音频文件
- `storage/images/*` - 上传的图片文件
- `__pycache__/` - Python 字节码缓存

## 数据流程

```
用户上传 (Streamlit)
    ↓
POST /api/episodes
    ↓
文件验证 (storage.py)
    ↓
保存文件 (本地/云存储)
    ↓
保存元数据 (SQLite)
    ↓
返回成功响应
    ↓
刷新播客列表
    ↓
展示新播客
```

## 扩展性

### 添加云存储支持

1. 在 `requirements.txt` 中取消注释相应的 SDK
2. 安装依赖: `pip install -r requirements.txt`
3. 配置环境变量（见 README.md）
4. 在 `backend/storage.py` 中取消注释实现代码
5. 设置 `STORAGE_BACKEND` 环境变量

### 添加新功能

- **用户认证**: 在 `backend/main.py` 添加 OAuth2/JWT
- **播客分类**: 在数据库添加 `category` 字段
- **搜索功能**: 在 API 添加搜索端点
- **评论系统**: 创建新的 `comments` 表和相关 API

## 技术栈

- **前端**: Streamlit 1.31.0
- **后端**: FastAPI 0.109.0
- **数据库**: SQLite 3
- **Web 服务器**: Uvicorn
- **HTTP 客户端**: Requests

## 安全性考虑

- ✅ 文件类型白名单验证
- ✅ 文件大小限制
- ✅ 文件名清理（防止路径遍历）
- ✅ CORS 配置
- ✅ 异常处理和错误消息

**生产环境需要**:
- 🔒 HTTPS/TLS
- 🔑 用户认证
- 📊 请求速率限制
- 🛡️ 文件内容扫描
- 🗄️ 生产级数据库（PostgreSQL）

---

**如有疑问，请参考 README.md 或 QUICKSTART.md** 📖

