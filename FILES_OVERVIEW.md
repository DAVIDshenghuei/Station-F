# 📚 项目文件总览

## 核心应用文件

### 前端
- **`app.py`** - Streamlit 前端应用
  - Web UI 界面
  - 文件上传功能
  - 播客列表展示和播放

### 后端
- **`backend/main.py`** - FastAPI 主应用
  - REST API 端点
  - 文件处理和验证
  - 数据库交互

- **`backend/models.py`** - Pydantic 数据模型
  - 请求/响应验证
  - 类型定义

- **`backend/db.py`** - 数据库管理
  - SQLite 连接
  - 表结构初始化

- **`backend/storage.py`** - 文件存储管理
  - 本地存储实现
  - 云存储占位符 (S3, Supabase, GitHub, GCP)

## 📤 上传工具（新增）

### 基础上传工具
- **`upload_audio.py`** - Python 脚本上传工具
  - ✅ 交互式上传界面
  - ✅ 可编程调用
  - ✅ 适合单个文件上传
  - 📖 使用方式: `python upload_audio.py`

### 11 Labs 集成工具
- **`upload_from_elevenlabs.py`** - 11 Labs API 集成
  - ✅ 文本转语音 (TTS)
  - ✅ 自动生成音频
  - ✅ 自动上传到系统
  - ✅ 完整工作流自动化
  - 📖 需要: ELEVENLABS_API_KEY 环境变量

### 批量上传工具
- **`batch_upload_example.py`** - 批量上传示例
  - ✅ 批量处理多个文件
  - ✅ 进度显示
  - ✅ 错误处理和汇总
  - 📖 适合批量导入播客

### 快速演示工具
- **`demo_quick_upload.py`** - 快速演示脚本
  - ✅ 简化的上传流程
  - ✅ 步骤指引
  - ✅ 连接测试
  - 📖 使用方式: `python demo_quick_upload.py`

## 📖 文档文件

### 主要文档
- **`README.md`** - 项目主文档
  - 完整功能介绍
  - 安装和配置说明
  - API 文档

- **`QUICKSTART.md`** - 快速启动指南
  - 快速安装步骤
  - 启动命令
  - 常见问题

- **`UPLOAD_GUIDE.md`** - 上传指南（新增）⭐
  - 5 种上传方法详解
  - 11 Labs 集成教程
  - 代码示例
  - 故障排除

- **`PROJECT_STRUCTURE.md`** - 项目结构说明
  - 文件组织说明
  - 技术栈介绍
  - 扩展指南

- **`FILES_OVERVIEW.md`** - 本文件
  - 所有文件总览
  - 快速参考

## 🚀 启动脚本

### Windows
- **`start_backend.bat`** - 启动 FastAPI 后端
- **`start_frontend.bat`** - 启动 Streamlit 前端

### Linux/Mac
- **`start_backend.sh`** - 启动 FastAPI 后端
- **`start_frontend.sh`** - 启动 Streamlit 前端

## ⚙️ 配置文件

- **`requirements.txt`** - Python 依赖列表
  - FastAPI + Streamlit
  - 可选云存储 SDK
  - 可选 11 Labs SDK

- **`.gitignore`** - Git 忽略规则

## 📁 数据和存储

### 自动生成的目录
- **`storage/`** - 本地文件存储
  - `storage/audio/` - 音频文件
  - `storage/images/` - 封面图片

### 数据库文件
- **`podcasts.db`** - SQLite 数据库（运行时自动创建）

## 🎯 使用场景和文件选择

### 场景 1: 首次安装和运行
```
1. 查看 README.md 或 QUICKSTART.md
2. 安装依赖: pip install -r requirements.txt
3. 启动后端: start_backend.bat 或 python -m uvicorn backend.main:app --reload
4. 启动前端: start_frontend.bat 或 streamlit run app.py
5. 打开浏览器: http://localhost:8501
```

### 场景 2: 使用前端上传文件
```
1. 确保后端和前端都在运行
2. 访问 http://localhost:8501
3. 在侧边栏上传文件
```

### 场景 3: 使用脚本上传 11 Labs 音频
```
方式 A: 已有音频文件
  - 运行 upload_audio.py
  - 或 demo_quick_upload.py (有引导界面)

方式 B: 从文本生成音频
  - 配置 ELEVENLABS_API_KEY
  - 运行 upload_from_elevenlabs.py
```

### 场景 4: 批量上传多个文件
```
1. 修改 batch_upload_example.py 中的文件列表
2. 运行脚本: python batch_upload_example.py
```

### 场景 5: 集成到现有系统
```
- 查看 UPLOAD_GUIDE.md 的 API 调用示例
- 使用 curl、Postman 或其他工具调用 API
- 或导入 upload_audio.py 中的函数到您的代码
```

## 📊 文件依赖关系

```
app.py
  └── requests 调用 backend/main.py API

backend/main.py
  ├── backend/models.py (数据模型)
  ├── backend/db.py (数据库)
  └── backend/storage.py (文件存储)

upload_audio.py
  └── 调用 backend/main.py API

upload_from_elevenlabs.py
  ├── 调用 11 Labs API (生成音频)
  └── 调用 backend/main.py API (上传)

batch_upload_example.py
  └── 使用 upload_audio.py

demo_quick_upload.py
  └── 调用 backend/main.py API
```

## 🔧 开发和扩展

### 修改前端 UI
- 编辑 `app.py`

### 修改后端 API
- 编辑 `backend/main.py`
- 修改数据模型: `backend/models.py`

### 添加云存储支持
- 编辑 `backend/storage.py`
- 取消注释相应的占位符函数
- 添加 SDK 到 `requirements.txt`

### 添加新的上传方式
- 参考 `upload_audio.py` 的实现
- 或查看 `UPLOAD_GUIDE.md` 的 API 文档

## 📦 最小运行要求

只需要这些文件就能运行基础系统：

```
必需文件:
├── app.py
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── db.py
│   └── storage.py
└── requirements.txt

可选文件（用于特殊功能）:
├── upload_audio.py (脚本上传)
├── upload_from_elevenlabs.py (11 Labs 集成)
├── batch_upload_example.py (批量上传)
└── demo_quick_upload.py (演示工具)
```

## 🆕 最近更新

### 2024-11-15
- ✅ 添加 5 种上传方式支持
- ✅ 集成 11 Labs TTS API
- ✅ 添加批量上传工具
- ✅ 创建详细的上传指南
- ✅ 修复 Pydantic v2 兼容性问题

## 💡 快速参考

| 需求 | 使用文件 |
|------|---------|
| 了解项目 | README.md |
| 快速开始 | QUICKSTART.md |
| 上传文件 | UPLOAD_GUIDE.md |
| 网页上传 | app.py (访问 http://localhost:8501) |
| 脚本上传 | upload_audio.py 或 demo_quick_upload.py |
| 11 Labs 集成 | upload_from_elevenlabs.py |
| 批量上传 | batch_upload_example.py |
| API 文档 | http://localhost:8000/docs (运行后端后) |

---

**需要帮助？** 查看对应的文档文件或运行 `python demo_quick_upload.py test` 测试连接

