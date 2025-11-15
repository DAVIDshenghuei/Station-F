# 🤖 AI Agent 快速集成指南

> 如果您已经有 AI 系统可以生成音频和图片，这个指南帮您快速集成到播客系统。

## ⚡ 3 步快速集成

### 步骤 1: 启动播客后端服务

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

### 步骤 2: 安装依赖

```bash
pip install requests
```

### 步骤 3: 使用客户端上传

```python
from podcast_api_client import quick_upload_bytes

# 您的 AI 生成的数据
audio_bytes = your_ai_tts_model.generate("播客内容...")
image_bytes = your_ai_image_model.generate("播客封面")

# 上传到播客系统
result = quick_upload_bytes(
    audio_bytes=audio_bytes,
    image_bytes=image_bytes,
    title="AI 生成的播客",
    description="这是 AI 自动生成的播客"
)

# 检查结果
if result["success"]:
    episode_id = result["data"]["id"]
    print(f"✅ 成功！播客 ID: {episode_id}")
    print(f"🌐 查看: http://localhost:8501")
else:
    print(f"❌ 失败: {result['error']}")
```

## 📡 直接使用 API（不用客户端库）

```python
import requests

# 准备数据
files = {
    'audio_file': ('audio.mp3', audio_bytes, 'audio/mpeg'),
    'image_file': ('cover.jpg', image_bytes, 'image/jpeg')
}
data = {
    'title': '播客标题',
    'description': '播客描述'
}

# 上传
response = requests.post(
    'http://localhost:8000/api/episodes',
    files=files,
    data=data
)

if response.status_code == 200:
    result = response.json()
    print(f"成功！ID: {result['id']}")
```

## 🎯 API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/episodes` | POST | 上传新播客 |
| `/api/episodes` | GET | 获取所有播客 |
| `/api/episodes/{id}` | GET | 获取单个播客 |
| `/api/episodes/{id}` | DELETE | 删除播客 |

## 📝 上传参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `audio_file` | File | ✅ | 音频文件（MP3/WAV/M4A，≤50MB）|
| `image_file` | File | ✅ | 封面图片（JPG/PNG，≤10MB）|
| `title` | String | ✅ | 播客标题 |
| `description` | String | ✅ | 播客描述 |

## 💡 完整示例

### 示例 1: 简单集成

```python
from podcast_api_client import PodcastAPIClient

# 创建客户端
client = PodcastAPIClient("http://localhost:8000")

# 检查服务
if not client.health_check():
    print("❌ 服务不可用")
    exit(1)

# AI 生成内容
audio_bytes = your_ai_model.generate_audio("内容...")
image_bytes = your_ai_model.generate_image("封面...")

# 上传
result = client.upload_from_bytes(
    audio_bytes=audio_bytes,
    image_bytes=image_bytes,
    title="AI 播客",
    description="描述"
)

print(result)
```

### 示例 2: 批量上传

```python
from podcast_api_client import PodcastAPIClient

client = PodcastAPIClient()

episodes = [
    {"text": "第一集内容", "title": "第一集"},
    {"text": "第二集内容", "title": "第二集"},
]

for ep in episodes:
    audio = your_ai.generate_audio(ep["text"])
    image = your_ai.generate_image(ep["title"])
    
    result = client.upload_from_bytes(
        audio_bytes=audio,
        image_bytes=image,
        title=ep["title"],
        description=ep["text"][:100]
    )
    
    if result["success"]:
        print(f"✅ {ep['title']} 上传成功")
```

### 示例 3: 从文件上传

```python
from podcast_api_client import quick_upload

# 如果 AI 已经生成了文件
result = quick_upload(
    audio_path="ai_output/audio.mp3",
    image_path="ai_output/cover.jpg",
    title="标题",
    description="描述"
)
```

## 🔧 可用工具

### Python 客户端库
- **`podcast_api_client.py`** - 完整的 API 客户端
  - `quick_upload_bytes()` - 最简单的函数
  - `PodcastAPIClient` - 完整的客户端类

### 示例脚本
- **`simple_agent_upload.py`** - 最简单的使用示例
- **`ai_agent_example.py`** - 完整的集成示例

### 文档
- **`AI_AGENT_API_GUIDE.md`** - 详细的 API 文档

## 🚀 快速测试

```bash
# 运行简单示例
python simple_agent_upload.py

# 运行完整示例
python ai_agent_example.py
```

## 📞 API 文档

启动后端后访问:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## ❓ 常见问题

### Q: 如何知道后端是否在运行？

```python
from podcast_api_client import PodcastAPIClient

client = PodcastAPIClient()
if client.health_check():
    print("✅ 服务正常")
```

### Q: 支持哪些音频格式？

- MP3 (推荐)
- WAV
- M4A

### Q: 如何处理大文件？

音频最大 50MB，如果超过需要压缩：

```python
from pydub import AudioSegment
import io

# 压缩音频
audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
output = io.BytesIO()
audio.export(output, format='mp3', bitrate='128k')
compressed = output.getvalue()
```

### Q: 可以异步上传吗？

可以，参考 `AI_AGENT_API_GUIDE.md` 的异步上传部分。

## 🎉 开始集成

1. 启动后端: `python -m uvicorn backend.main:app --reload --port 8000`
2. 安装依赖: `pip install requests`
3. 使用客户端: `from podcast_api_client import quick_upload_bytes`
4. 上传数据: `result = quick_upload_bytes(...)`

---

**需要详细文档？** 查看 [AI_AGENT_API_GUIDE.md](AI_AGENT_API_GUIDE.md)

