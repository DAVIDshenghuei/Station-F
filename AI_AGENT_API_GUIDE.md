# 🤖 AI Agent API 集成指南

本指南专为 AI Agent 开发者设计，展示如何将 AI 生成的音频和图片直接上传到播客系统。

## 📡 API 端点

### 基础信息
- **Base URL**: `http://localhost:8000`
- **上传端点**: `POST /api/episodes`
- **Content-Type**: `multipart/form-data`

## 🚀 快速开始（3 步集成）

### 方法 1: 使用 Python 客户端库（推荐）

```python
from podcast_api_client import quick_upload_bytes

# AI 生成音频和图片后
result = quick_upload_bytes(
    audio_bytes=ai_generated_audio_bytes,
    image_bytes=ai_generated_image_bytes,
    title="播客标题",
    description="播客描述"
)

if result["success"]:
    episode_id = result["data"]["id"]
    print(f"✅ 发布成功！ID: {episode_id}")
else:
    print(f"❌ 失败: {result['error']}")
```

### 方法 2: 直接使用 requests

```python
import requests

# AI 生成的字节数据
audio_bytes = your_ai_tts_model.generate(...)
image_bytes = your_ai_image_model.generate(...)

# 准备上传
files = {
    'audio_file': ('audio.mp3', audio_bytes, 'audio/mpeg'),
    'image_file': ('cover.jpg', image_bytes, 'image/jpeg')
}

data = {
    'title': '播客标题',
    'description': '播客描述'
}

# 发送请求
response = requests.post(
    'http://localhost:8000/api/episodes',
    files=files,
    data=data
)

if response.status_code == 200:
    result = response.json()
    print(f"成功！播客 ID: {result['id']}")
```

### 方法 3: 使用 cURL（测试用）

```bash
curl -X POST "http://localhost:8000/api/episodes" \
  -F "audio_file=@audio.mp3" \
  -F "image_file=@cover.jpg" \
  -F "title=我的播客" \
  -F "description=这是描述"
```

## 📋 API 详细说明

### POST /api/episodes - 上传播客

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `audio_file` | File | ✅ | 音频文件（MP3/WAV/M4A，最大 50MB）|
| `image_file` | File | ✅ | 封面图片（JPG/PNG，最大 10MB）|
| `title` | String | ✅ | 播客标题 |
| `description` | String | ✅ | 播客描述 |

**成功响应** (200 OK):
```json
{
  "id": 1,
  "title": "播客标题",
  "description": "播客描述",
  "audio_url": "/storage/audio/xxx.mp3",
  "image_url": "/storage/images/xxx.jpg",
  "created_at": "2024-11-15T12:00:00"
}
```

**错误响应** (400 Bad Request):
```json
{
  "detail": "音频文件无效: 文件大小超过限制"
}
```

### GET /api/episodes - 获取所有播客

**请求**:
```python
response = requests.get('http://localhost:8000/api/episodes')
episodes = response.json()
```

**响应**:
```json
[
  {
    "id": 1,
    "title": "播客标题",
    "description": "播客描述",
    "audio_url": "/storage/audio/xxx.mp3",
    "image_url": "/storage/images/xxx.jpg",
    "created_at": "2024-11-15T12:00:00"
  }
]
```

### GET /api/episodes/{id} - 获取单个播客

**请求**:
```python
response = requests.get('http://localhost:8000/api/episodes/1')
episode = response.json()
```

### DELETE /api/episodes/{id} - 删除播客

**请求**:
```python
response = requests.delete('http://localhost:8000/api/episodes/1')
```

## 💡 完整 AI Agent 集成示例

### 示例 1: 简单集成

```python
# 1. 导入客户端
from podcast_api_client import PodcastAPIClient

# 2. 创建客户端实例
client = PodcastAPIClient("http://localhost:8000")

# 3. AI 生成内容（这里用您的 AI 模型）
audio_bytes = your_tts_model.generate("播客文本内容...")
image_bytes = your_image_model.generate("播客封面，科技风格")

# 4. 上传
result = client.upload_from_bytes(
    audio_bytes=audio_bytes,
    image_bytes=image_bytes,
    title="AI 生成的播客",
    description="完全由 AI 自动生成"
)

# 5. 处理结果
if result["success"]:
    print(f"✅ 播客 ID: {result['data']['id']}")
    print(f"🎵 音频: http://localhost:8000{result['data']['audio_url']}")
    print(f"🌐 查看: http://localhost:8501")
```

### 示例 2: 使用 11 Labs TTS

```python
from podcast_api_client import quick_upload_bytes
from elevenlabs import generate

# 1. 使用 11 Labs 生成音频
audio_bytes = generate(
    text="欢迎来到 AI 播客...",
    voice="Rachel",
    model="eleven_monolingual_v1"
)

# 2. 生成封面（使用您的图像模型）
image_bytes = your_image_model.generate("播客封面")

# 3. 上传
result = quick_upload_bytes(
    audio_bytes=audio_bytes,
    image_bytes=image_bytes,
    title="11 Labs 播客",
    description="使用 11 Labs 生成的音频"
)
```

### 示例 3: 批量生成和发布

```python
from podcast_api_client import PodcastAPIClient

client = PodcastAPIClient()

# 播客内容列表
episodes = [
    {"text": "第一集内容...", "title": "第一集"},
    {"text": "第二集内容...", "title": "第二集"},
    {"text": "第三集内容...", "title": "第三集"},
]

# 批量处理
for episode in episodes:
    # AI 生成
    audio_bytes = your_tts_model.generate(episode["text"])
    image_bytes = your_image_model.generate(f"{episode['title']}封面")
    
    # 上传
    result = client.upload_from_bytes(
        audio_bytes=audio_bytes,
        image_bytes=image_bytes,
        title=episode["title"],
        description=f"{episode['title']}的内容"
    )
    
    if result["success"]:
        print(f"✅ {episode['title']} 发布成功")
```

## 🔧 集成您的 AI 模型

### 步骤 1: 创建 AI Agent 类

```python
from podcast_api_client import PodcastAPIClient

class MyPodcastAIAgent:
    def __init__(self):
        self.podcast_api = PodcastAPIClient("http://localhost:8000")
        # 初始化您的 AI 模型
        # self.tts_model = YourTTSModel()
        # self.image_model = YourImageModel()
    
    def create_podcast(self, text: str, title: str, description: str):
        """从文本创建完整播客"""
        
        # 1. 生成音频
        audio_bytes = self.tts_model.generate(text)
        
        # 2. 生成封面
        image_bytes = self.image_model.generate(f"{title} 播客封面")
        
        # 3. 上传
        result = self.podcast_api.upload_from_bytes(
            audio_bytes=audio_bytes,
            image_bytes=image_bytes,
            title=title,
            description=description
        )
        
        return result

# 使用
agent = MyPodcastAIAgent()
result = agent.create_podcast(
    text="播客内容...",
    title="我的播客",
    description="描述"
)
```

### 步骤 2: 处理不同的输入格式

#### 从文件读取（AI 已经生成了文件）

```python
from podcast_api_client import quick_upload

result = quick_upload(
    audio_path="ai_output/generated_audio.mp3",
    image_path="ai_output/generated_cover.jpg",
    title="标题",
    description="描述"
)
```

#### 从 Base64 编码

```python
import base64
from podcast_api_client import PodcastAPIClient

client = PodcastAPIClient()

# 如果您的 AI 返回 Base64 编码的数据
result = client.upload_from_base64(
    audio_base64=audio_base64_string,
    image_base64=image_base64_string,
    title="标题",
    description="描述"
)
```

#### 从 URL 下载后上传

```python
import requests
from podcast_api_client import quick_upload_bytes

# 下载 AI 生成的文件
audio_bytes = requests.get("https://your-ai-api.com/audio/xxx").content
image_bytes = requests.get("https://your-ai-api.com/image/xxx").content

# 上传
result = quick_upload_bytes(
    audio_bytes=audio_bytes,
    image_bytes=image_bytes,
    title="标题",
    description="描述"
)
```

## 🛡️ 错误处理

### 推荐的错误处理模式

```python
from podcast_api_client import PodcastAPIClient

client = PodcastAPIClient()

# 1. 检查服务是否可用
if not client.health_check():
    print("❌ 播客 API 服务不可用")
    # 处理：等待、重试或通知
    exit(1)

# 2. 上传时处理错误
result = client.upload_from_bytes(
    audio_bytes=audio_bytes,
    image_bytes=image_bytes,
    title=title,
    description=description
)

if result["success"]:
    # 成功
    episode_id = result["data"]["id"]
    print(f"✅ 成功！ID: {episode_id}")
else:
    # 失败
    error_msg = result["error"]
    print(f"❌ 失败: {error_msg}")
    
    # 根据错误类型处理
    if "连接" in error_msg:
        # 网络问题，可以重试
        pass
    elif "文件大小" in error_msg:
        # 文件太大，需要压缩
        pass
    elif "格式" in error_msg:
        # 格式问题，需要转换
        pass
```

## 📊 性能优化

### 1. 异步上传（高并发场景）

```python
import asyncio
import aiohttp

async def upload_podcast_async(audio_bytes, image_bytes, title, description):
    """异步上传播客"""
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('audio_file', audio_bytes, filename='audio.mp3')
        data.add_field('image_file', image_bytes, filename='cover.jpg')
        data.add_field('title', title)
        data.add_field('description', description)
        
        async with session.post(
            'http://localhost:8000/api/episodes',
            data=data
        ) as response:
            return await response.json()

# 并发上传多个播客
async def batch_upload_async(episodes):
    tasks = [
        upload_podcast_async(
            ep['audio_bytes'],
            ep['image_bytes'],
            ep['title'],
            ep['description']
        )
        for ep in episodes
    ]
    results = await asyncio.gather(*tasks)
    return results
```

### 2. 压缩音频（减小文件大小）

```python
from pydub import AudioSegment

def compress_audio(audio_bytes, target_bitrate='128k'):
    """压缩音频以减小文件大小"""
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
    output = io.BytesIO()
    audio.export(output, format='mp3', bitrate=target_bitrate)
    return output.getvalue()

# 使用
compressed_audio = compress_audio(ai_generated_audio, '96k')
result = quick_upload_bytes(compressed_audio, image_bytes, title, description)
```

## 🔍 调试和测试

### 测试连接

```python
from podcast_api_client import PodcastAPIClient

client = PodcastAPIClient()

if client.health_check():
    print("✅ API 服务正常")
else:
    print("❌ API 服务不可用")
    print("请运行: python -m uvicorn backend.main:app --reload --port 8000")
```

### 查看 API 文档

启动后端后，访问：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 测试上传

```python
# 创建测试数据
test_audio = b'\xff\xfb\x90\x00' * 1000  # 简单的 MP3 数据
test_image = b'\xff\xd8\xff\xe0' * 1000  # 简单的 JPEG 数据

result = quick_upload_bytes(
    audio_bytes=test_audio,
    image_bytes=test_image,
    title="测试播客",
    description="这是测试"
)
print(result)
```

## 📝 完整工作示例

```python
"""
完整的 AI Agent 工作流示例
"""
from podcast_api_client import PodcastAPIClient

# 1. 初始化
client = PodcastAPIClient("http://localhost:8000")

# 2. 检查服务
if not client.health_check():
    raise Exception("API 服务不可用")

# 3. AI 生成内容（替换为您的 AI 模型）
def generate_content(topic):
    # 您的 AI 模型
    text = f"关于 {topic} 的播客内容..."
    audio_bytes = your_tts_model.generate(text)
    image_bytes = your_image_model.generate(f"{topic} 封面")
    return audio_bytes, image_bytes

# 4. 生成并上传
topic = "人工智能的未来"
audio_bytes, image_bytes = generate_content(topic)

result = client.upload_from_bytes(
    audio_bytes=audio_bytes,
    image_bytes=image_bytes,
    title=f"播客：{topic}",
    description=f"探讨 {topic}"
)

# 5. 处理结果
if result["success"]:
    episode = result["data"]
    print(f"""
    ✅ 播客发布成功！
    
    ID: {episode['id']}
    标题: {episode['title']}
    音频: http://localhost:8000{episode['audio_url']}
    封面: http://localhost:8000{episode['image_url']}
    
    在线查看: http://localhost:8501
    """)
else:
    print(f"❌ 发布失败: {result['error']}")
```

## 🚀 开始使用

1. **安装依赖**
```bash
pip install requests
```

2. **启动后端服务**
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

3. **使用客户端库**
```python
from podcast_api_client import quick_upload_bytes

result = quick_upload_bytes(
    audio_bytes=your_audio_bytes,
    image_bytes=your_image_bytes,
    title="标题",
    description="描述"
)
```

## 📞 需要帮助？

- **API 文档**: http://localhost:8000/docs
- **示例代码**: `ai_agent_example.py`
- **客户端库**: `podcast_api_client.py`

---

**开始集成您的 AI Agent 吧！** 🎉

