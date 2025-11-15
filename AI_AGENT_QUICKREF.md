# 🤖 AI Agent 快速参考卡片

## 📦 核心文件

| 文件 | 用途 |
|------|------|
| `podcast_api_client.py` | Python 客户端库（必需）|
| `simple_agent_upload.py` | 最简单的使用示例 |
| `ai_agent_example.py` | 完整的集成示例 |
| `AI_AGENT_API_GUIDE.md` | 详细文档 |
| `README_AI_AGENT.md` | 快速开始指南 |

## ⚡ 一行代码上传

```python
from podcast_api_client import quick_upload_bytes

result = quick_upload_bytes(audio_bytes, image_bytes, "标题", "描述")
```

## 🎯 三种使用方式

### 1️⃣ 最简单（推荐）

```python
from podcast_api_client import quick_upload_bytes

result = quick_upload_bytes(
    audio_bytes=ai_audio,
    image_bytes=ai_image,
    title="标题",
    description="描述"
)
```

### 2️⃣ 使用类

```python
from podcast_api_client import PodcastAPIClient

client = PodcastAPIClient("http://localhost:8000")
result = client.upload_from_bytes(audio_bytes, image_bytes, "标题", "描述")
```

### 3️⃣ 直接 API 调用

```python
import requests

files = {
    'audio_file': ('audio.mp3', audio_bytes, 'audio/mpeg'),
    'image_file': ('cover.jpg', image_bytes, 'image/jpeg')
}
data = {'title': '标题', 'description': '描述'}

response = requests.post('http://localhost:8000/api/episodes', files=files, data=data)
```

## 📋 API 端点

```
POST   /api/episodes      # 上传播客
GET    /api/episodes      # 获取所有
GET    /api/episodes/{id} # 获取单个
DELETE /api/episodes/{id} # 删除
```

## 🔧 必需参数

| 参数 | 类型 | 限制 |
|------|------|------|
| audio_file | bytes | MP3/WAV/M4A, ≤50MB |
| image_file | bytes | JPG/PNG, ≤10MB |
| title | string | 必填 |
| description | string | 必填 |

## 📝 响应格式

### 成功 (200)
```json
{
  "id": 1,
  "title": "标题",
  "description": "描述",
  "audio_url": "/storage/audio/xxx.mp3",
  "image_url": "/storage/images/xxx.jpg",
  "created_at": "2024-11-15T12:00:00"
}
```

### 失败 (400)
```json
{
  "detail": "错误信息"
}
```

## 🚀 启动后端

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

## ✅ 检查服务

```python
from podcast_api_client import PodcastAPIClient

client = PodcastAPIClient()
if client.health_check():
    print("✅ 服务正常")
```

## 🔍 测试 API

访问: http://localhost:8000/docs

## 💡 完整示例

```python
from podcast_api_client import PodcastAPIClient

# 1. 创建客户端
client = PodcastAPIClient()

# 2. 检查服务
if not client.health_check():
    print("服务不可用")
    exit(1)

# 3. AI 生成内容
audio_bytes = your_ai_tts("文本...")
image_bytes = your_ai_image("封面...")

# 4. 上传
result = client.upload_from_bytes(
    audio_bytes=audio_bytes,
    image_bytes=image_bytes,
    title="AI 播客",
    description="AI 生成"
)

# 5. 检查结果
if result["success"]:
    print(f"✅ ID: {result['data']['id']}")
    print(f"🌐 http://localhost:8501")
```

## 📞 常用函数

```python
# 从字节上传
quick_upload_bytes(audio_bytes, image_bytes, title, desc)

# 从文件上传
quick_upload(audio_path, image_path, title, desc)

# 从 Base64 上传
client.upload_from_base64(audio_b64, image_b64, title, desc)

# 获取所有播客
client.get_all_episodes()

# 获取单个
client.get_episode(episode_id)

# 删除
client.delete_episode(episode_id)

# 健康检查
client.health_check()
```

## 🎓 学习路径

1. **快速开始** → `README_AI_AGENT.md`
2. **简单示例** → `simple_agent_upload.py`
3. **完整示例** → `ai_agent_example.py`
4. **API 详细文档** → `AI_AGENT_API_GUIDE.md`
5. **API 在线文档** → http://localhost:8000/docs

## ⚠️ 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 无法连接 | 后端未启动 | 运行 uvicorn |
| 文件太大 | 超过限制 | 压缩文件 |
| 格式错误 | 格式不支持 | 转换为 MP3/JPG |

## 📦 依赖

```bash
pip install requests
```

可选:
```bash
pip install elevenlabs  # 11 Labs TTS
pip install pillow      # 图片处理
pip install pydub       # 音频处理
```

---

**快速开始**: `python simple_agent_upload.py`

