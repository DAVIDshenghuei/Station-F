# 🎙️ 播客上传和展示平台

一个完整的播客管理系统，包含 Streamlit 前端和 FastAPI 后端。支持音频和封面图片上传、播客展示和播放。

## ✨ 功能特性

- 📤 **文件上传**: 支持 MP3、WAV、M4A 音频格式和 JPG、PNG 封面图片
- 🎵 **音频播放**: 内置播放器，直接在浏览器中播放
- 🖼️ **封面展示**: 精美的播客封面图片展示
- 💾 **数据持久化**: 使用 SQLite 数据库存储元数据
- 📁 **本地存储**: 默认使用本地文件系统存储（可扩展至云存储）
- 🔌 **云存储支持**: 预留 S3、Supabase、GitHub、GCP 集成接口
- ✅ **文件验证**: 自动验证文件类型和大小
- 🚀 **现代化 UI**: 美观的 Streamlit 界面设计

## 📁 项目结构

```
.
├── app.py                  # Streamlit 前端应用
├── backend/
│   ├── __init__.py
│   ├── main.py            # FastAPI 主应用
│   ├── models.py          # Pydantic 数据模型
│   ├── db.py              # SQLite 数据库管理
│   └── storage.py         # 文件存储管理
├── storage/               # 本地文件存储目录（自动创建）
│   ├── audio/            # 音频文件
│   └── images/           # 图片文件
├── requirements.txt       # Python 依赖
├── README.md             # 项目文档
└── podcasts.db           # SQLite 数据库（自动创建）
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动后端服务

在第一个终端窗口中运行：

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

后端服务将在 `http://localhost:8000` 启动。

可以访问 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. 启动前端应用

在第二个终端窗口中运行：

```bash
streamlit run app.py
```

前端应用将在 `http://localhost:8501` 启动（浏览器会自动打开）。

## 📖 使用指南

### 方式 1: 使用前端界面上传（推荐）

1. 在侧边栏中选择音频文件（MP3、WAV 或 M4A）
2. 选择封面图片（JPG 或 PNG）
3. 输入播客标题和描述
4. 预览上传的内容
5. 点击"发布播客"按钮

### 方式 2: 使用 Python 脚本上传

适合上传 11 Labs 生成的音频或批量上传：

```bash
# 交互式上传
python upload_audio.py

# 或编程方式上传
from upload_audio import upload_podcast

result = upload_podcast(
    audio_path="path/to/audio.mp3",
    image_path="path/to/cover.jpg",
    title="我的播客",
    description="描述"
)
```

### 方式 3: 集成 11 Labs API 自动生成

从文本直接生成音频并上传：

```bash
# 设置 API 密钥
export ELEVENLABS_API_KEY="your_key"

# 运行脚本
python upload_from_elevenlabs.py
```

**📚 详细上传指南**: 查看 [UPLOAD_GUIDE.md](UPLOAD_GUIDE.md)

### 方式 4: AI Agent 直接集成 ⭐

适合已有 AI 系统，需要程序化上传：

```python
from podcast_api_client import quick_upload_bytes

# AI 生成音频和图片后，直接上传
result = quick_upload_bytes(
    audio_bytes=ai_generated_audio,
    image_bytes=ai_generated_image,
    title="AI 播客",
    description="AI 生成的内容"
)

if result["success"]:
    print(f"✅ 播客 ID: {result['data']['id']}")
```

**🤖 AI Agent API 指南**: 查看 [AI_AGENT_API_GUIDE.md](AI_AGENT_API_GUIDE.md)

### 浏览播客

- 主页面会自动显示所有已上传的播客
- 每个播客显示封面、标题、描述和音频播放器
- 点击播放器即可收听

## ⚙️ 配置选项

### 存储后端配置

默认使用本地文件存储。如需使用云存储，请设置环境变量：

```bash
# 选择存储后端
export STORAGE_BACKEND=local  # 可选: local, s3, supabase, github, gcp

# AWS S3 配置
export S3_BUCKET=your-bucket-name
export S3_REGION=us-east-1
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key

# Supabase 配置
export SUPABASE_URL=https://your-project.supabase.co
export SUPABASE_KEY=your-anon-key
export SUPABASE_BUCKET=podcasts

# GitHub 配置
export GITHUB_REPO=username/repo
export GITHUB_TOKEN=your-github-token
export GITHUB_BRANCH=main

# Google Cloud Storage 配置
export GCP_BUCKET=your-bucket-name
export GCP_PROJECT_ID=your-project-id
```

### 文件大小限制

- 音频文件: 最大 50MB
- 图片文件: 最大 10MB

可以在 `backend/main.py` 中的 `validate_file()` 函数修改这些限制。

## 🔌 云存储集成

项目包含以下云存储服务的占位符函数（位于 `backend/storage.py`）：

- **AWS S3**: `save_file_s3()`
- **Supabase Storage**: `save_file_supabase()`
- **GitHub Repository**: `save_file_github()`
- **Google Cloud Storage**: `save_file_gcp()`

要启用云存储：

1. 安装相应的 SDK（在 `requirements.txt` 中取消注释）
2. 配置环境变量
3. 取消注释 `storage.py` 中的实现代码
4. 设置 `STORAGE_BACKEND` 环境变量

## 🛠️ API 端点

### `POST /api/episodes`
上传新播客

**请求体**: multipart/form-data
- `audio_file`: 音频文件
- `image_file`: 图片文件
- `title`: 播客标题
- `description`: 播客描述

### `GET /api/episodes`
获取所有播客列表

### `GET /api/episodes/{id}`
获取单个播客详情

### `DELETE /api/episodes/{id}`
删除播客

## 🔒 安全性

- ✅ 文件类型验证
- ✅ 文件大小限制
- ✅ 文件名清理（防止路径遍历）
- ✅ CORS 配置
- ✅ 错误处理

**生产环境建议**:
- 限制 CORS 允许的域名
- 添加用户认证和授权
- 使用 HTTPS
- 实施速率限制
- 添加文件内容扫描

## 📝 数据库架构

### episodes 表

| 列名 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键（自增）|
| title | TEXT | 播客标题 |
| description | TEXT | 播客描述 |
| audio_path | TEXT | 音频文件路径 |
| image_path | TEXT | 图片文件路径 |
| created_at | TEXT | 创建时间（ISO格式）|

## 🐛 故障排除

### 无法连接到后端

确保 FastAPI 服务正在运行：
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

### 文件上传失败

检查：
- 文件格式是否支持
- 文件大小是否超过限制
- `storage` 目录是否有写入权限

### 数据库错误

删除并重新创建数据库：
```bash
rm podcasts.db
# 重启后端，数据库会自动重新创建
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

播客展示平台 - 使用 Streamlit + FastAPI 构建

---

**享受您的播客创作之旅！** 🎉

