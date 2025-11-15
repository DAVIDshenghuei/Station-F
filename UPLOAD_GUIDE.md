# 📤 音频上传指南

## 方法 1: 使用前端界面上传（最简单）

1. 启动后端和前端服务
2. 打开浏览器访问 http://localhost:8501
3. 在侧边栏上传 11 Labs 生成的音频文件和封面图片
4. 填写标题和描述，点击发布

---

## 方法 2: 使用 Python 脚本上传

### 🎯 适用场景
- 已经有 11 Labs 生成的音频文件
- 想要批量上传
- 自动化工作流

### 使用步骤

1. **确保后端服务正在运行**
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

2. **运行上传脚本**
```bash
python upload_audio.py
```

3. **按提示输入信息**
```
请输入音频文件路径: C:\path\to\your\audio.mp3
请输入封面图片路径: C:\path\to\your\cover.jpg
请输入播客标题: 我的播客
请输入播客描述: 这是描述
```

### 快速上传（代码方式）

编辑 `upload_audio.py`，修改 `upload_example()` 函数：

```python
from upload_audio import upload_podcast

result = upload_podcast(
    audio_path="C:/Users/xxx/audio.mp3",
    image_path="C:/Users/xxx/cover.jpg",
    title="我的播客标题",
    description="播客描述"
)

if result["success"]:
    print(f"✅ 上传成功！")
    print(f"播客 ID: {result['data']['id']}")
```

---

## 方法 3: 集成 11 Labs API（自动化）

### 🎯 适用场景
- 想要从文本直接生成音频并上传
- 完全自动化流程
- 批量生成播客

### 配置步骤

1. **安装 11 Labs 依赖**
```bash
pip install elevenlabs
```

2. **设置 API 密钥**

Windows PowerShell:
```powershell
$env:ELEVENLABS_API_KEY="your_api_key_here"
```

Windows CMD:
```cmd
set ELEVENLABS_API_KEY=your_api_key_here
```

Linux/Mac:
```bash
export ELEVENLABS_API_KEY="your_api_key_here"
```

或者创建 `.env` 文件：
```
ELEVENLABS_API_KEY=your_api_key_here
```

3. **运行脚本**
```bash
python upload_from_elevenlabs.py
```

### 代码方式使用

```python
from upload_from_elevenlabs import generate_and_upload

# 从文本生成音频并自动上传
result = generate_and_upload(
    text="欢迎来到我的播客，今天我们讨论人工智能的未来...",
    image_path="cover.jpg",
    title="AI 播客第一集",
    description="探讨 AI 的未来发展",
    voice_id="21m00Tcm4TlvDq8ikWAM"  # Rachel 的声音
)
```

### 11 Labs 声音选项

| Voice ID | 名称 | 性别 | 特点 |
|----------|------|------|------|
| `21m00Tcm4TlvDq8ikWAM` | Rachel | 女性 | 清晰、专业 |
| `TxGEqnHWrfWFTfGW9XjX` | Josh | 男性 | 年轻、友好 |
| `ErXwobaYiN019PkySvjV` | Antoni | 男性 | 沉稳、权威 |
| `VR6AewLTigWG4xSOukaG` | Arnold | 男性 | 深沉、磁性 |

查看所有可用声音：https://api.elevenlabs.io/v1/voices

---

## 方法 4: 使用 cURL 上传

### 适用于命令行或脚本集成

```bash
curl -X POST "http://localhost:8000/api/episodes" \
  -F "audio_file=@/path/to/audio.mp3" \
  -F "image_file=@/path/to/cover.jpg" \
  -F "title=我的播客" \
  -F "description=这是描述"
```

Windows PowerShell:
```powershell
$audioPath = "C:\path\to\audio.mp3"
$imagePath = "C:\path\to\cover.jpg"

curl.exe -X POST "http://localhost:8000/api/episodes" `
  -F "audio_file=@$audioPath" `
  -F "image_file=@$imagePath" `
  -F "title=我的播客" `
  -F "description=这是描述"
```

---

## 方法 5: 使用 Postman 测试

1. 打开 Postman
2. 创建新的 POST 请求
3. URL: `http://localhost:8000/api/episodes`
4. Body 选择 `form-data`
5. 添加字段：
   - `audio_file` (File): 选择音频文件
   - `image_file` (File): 选择图片文件
   - `title` (Text): 输入标题
   - `description` (Text): 输入描述
6. 点击 Send

---

## 📝 文件要求

### 音频文件
- **格式**: MP3, WAV, M4A
- **大小**: 最大 50MB
- **内容类型**: audio/mpeg, audio/wav, audio/mp4

### 图片文件
- **格式**: JPG, JPEG, PNG
- **大小**: 最大 10MB
- **内容类型**: image/jpeg, image/png

---

## 🔧 故障排除

### 错误: 无法连接到后端

**解决方案**: 确保 FastAPI 服务正在运行
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

### 错误: 文件格式不支持

**解决方案**: 检查文件格式
- 音频: 使用 MP3 格式最兼容
- 图片: 使用 JPG 格式最兼容

### 错误: 文件太大

**解决方案**: 
- 压缩音频文件
- 使用在线工具: https://www.freeconvert.com/audio-compressor
- 或使用 FFmpeg:
```bash
ffmpeg -i input.mp3 -b:a 128k output.mp3
```

### 错误: 11 Labs API 密钥无效

**解决方案**: 
1. 访问 https://elevenlabs.io/
2. 登录账户
3. 获取 API 密钥
4. 设置环境变量

---

## 💡 完整工作流示例

### 场景: 自动化播客制作

```python
# 1. 准备内容
podcast_episodes = [
    {
        "text": "欢迎来到第一集...",
        "title": "第一集：AI 简介",
        "cover": "cover1.jpg"
    },
    {
        "text": "欢迎来到第二集...",
        "title": "第二集：机器学习",
        "cover": "cover2.jpg"
    }
]

# 2. 批量处理
from upload_from_elevenlabs import generate_and_upload

for episode in podcast_episodes:
    print(f"\n处理: {episode['title']}")
    
    result = generate_and_upload(
        text=episode['text'],
        image_path=episode['cover'],
        title=episode['title'],
        description=f"{episode['title']} 的内容",
        cleanup=True
    )
    
    if result:
        print(f"✅ {episode['title']} 上传成功！")
    else:
        print(f"❌ {episode['title']} 上传失败")

print("\n🎉 所有播客处理完成！")
```

---

## 🎬 视频教程（如需要）

1. **基础上传**: 使用前端界面上传
2. **脚本上传**: 使用 Python 脚本
3. **自动化**: 集成 11 Labs API

---

**需要帮助？** 查看 [README.md](README.md) 或 [QUICKSTART.md](QUICKSTART.md)

