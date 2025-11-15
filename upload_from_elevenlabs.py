"""
集成 11 Labs API，生成音频后自动上传到播客系统
"""
import requests
import os
from pathlib import Path
from datetime import datetime

# 配置
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")  # 在环境变量中设置
PODCAST_API_URL = "http://localhost:8000"

def generate_audio_elevenlabs(
    text: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Rachel 声音 ID
    api_key: str = ELEVENLABS_API_KEY,
    output_path: str = None
):
    """
    使用 11 Labs API 生成音频
    
    参数:
        text: 要转换的文本
        voice_id: 声音 ID（默认 Rachel）
        api_key: 11 Labs API 密钥
        output_path: 保存路径（如果为 None，自动生成）
    
    返回:
        音频文件路径或 None（如果失败）
    """
    if not api_key:
        print("❌ 错误: 请设置 ELEVENLABS_API_KEY 环境变量")
        return None
    
    # 生成输出文件名
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"temp_audio_{timestamp}.mp3"
    
    # 11 Labs API 端点
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    try:
        print("🎙️ 正在使用 11 Labs 生成音频...")
        response = requests.post(url, json=data, headers=headers, timeout=60)
        
        if response.status_code == 200:
            # 保存音频文件
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ 音频生成成功: {output_path}")
            return output_path
        else:
            print(f"❌ 音频生成失败: {response.status_code} - {response.text}")
            return None
    
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        return None

def upload_to_podcast_system(
    audio_path: str,
    image_path: str,
    title: str,
    description: str
):
    """
    上传到播客系统
    
    参数:
        audio_path: 音频文件路径
        image_path: 封面图片路径
        title: 播客标题
        description: 播客描述
    
    返回:
        上传结果
    """
    try:
        with open(audio_path, 'rb') as audio_file, open(image_path, 'rb') as image_file:
            files = {
                'audio_file': (os.path.basename(audio_path), audio_file, 'audio/mpeg'),
                'image_file': (os.path.basename(image_path), image_file, 'image/jpeg')
            }
            
            data = {
                'title': title,
                'description': description
            }
            
            print("📤 正在上传到播客系统...")
            response = requests.post(
                f"{PODCAST_API_URL}/api/episodes",
                files=files,
                data=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 上传成功！")
                print(f"   播客 ID: {result['id']}")
                print(f"   音频 URL: {PODCAST_API_URL}{result['audio_url']}")
                print(f"   前端查看: http://localhost:8501")
                return result
            else:
                print(f"❌ 上传失败: {response.status_code} - {response.text}")
                return None
    
    except Exception as e:
        print(f"❌ 上传错误: {str(e)}")
        return None

def generate_and_upload(
    text: str,
    image_path: str,
    title: str,
    description: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",
    cleanup: bool = True
):
    """
    完整流程：生成音频 -> 上传到播客系统
    
    参数:
        text: 要转换成语音的文本
        image_path: 封面图片路径
        title: 播客标题
        description: 播客描述
        voice_id: 11 Labs 声音 ID
        cleanup: 是否删除临时音频文件
    """
    print(f"\n🎬 开始处理播客: {title}\n")
    
    # 步骤 1: 生成音频
    audio_path = generate_audio_elevenlabs(text, voice_id)
    
    if not audio_path:
        print("❌ 音频生成失败，流程终止")
        return None
    
    # 步骤 2: 上传到播客系统
    result = upload_to_podcast_system(audio_path, image_path, title, description)
    
    # 步骤 3: 清理临时文件（可选）
    if cleanup and audio_path and os.path.exists(audio_path):
        try:
            os.remove(audio_path)
            print(f"🗑️  临时文件已删除: {audio_path}")
        except Exception as e:
            print(f"⚠️  无法删除临时文件: {str(e)}")
    
    return result

# ==================== 使用示例 ====================

def example_usage():
    """使用示例"""
    
    # 示例 1: 仅生成音频
    print("=" * 60)
    print("示例 1: 使用 11 Labs 生成音频")
    print("=" * 60)
    
    audio_path = generate_audio_elevenlabs(
        text="欢迎来到我的播客。今天我们要讨论人工智能的未来。",
        output_path="my_podcast.mp3"
    )
    
    # 示例 2: 生成音频并自动上传
    print("\n" + "=" * 60)
    print("示例 2: 生成音频并上传到播客系统")
    print("=" * 60)
    
    result = generate_and_upload(
        text="这是使用 11 Labs 自动生成的播客内容。",
        image_path="path/to/cover.jpg",  # 修改为实际的图片路径
        title="AI 生成的播客",
        description="这是一个使用 11 Labs 和 FastAPI 自动生成的播客",
        cleanup=True  # 自动清理临时文件
    )

if __name__ == "__main__":
    print("""
    🎙️ 11 Labs + 播客系统集成工具
    
    使用前请确保:
    1. 设置环境变量: ELEVENLABS_API_KEY
    2. 后端服务正在运行 (http://localhost:8000)
    3. 准备好封面图片
    
    可用的声音 ID（11 Labs）:
    - 21m00Tcm4TlvDq8ikWAM: Rachel (女性)
    - TxGEqnHWrfWFTfGW9XjX: Josh (男性)
    - ErXwobaYiN019PkySvjV: Antoni (男性)
    
    更多声音: https://api.elevenlabs.io/v1/voices
    """)
    
    # 交互式使用
    choice = input("\n选择操作:\n1. 仅生成音频\n2. 生成并上传\n请输入 (1/2): ")
    
    if choice == "1":
        text = input("\n请输入要转换的文本: ")
        output_path = input("保存路径 (默认: audio.mp3): ").strip() or "audio.mp3"
        generate_audio_elevenlabs(text, output_path=output_path)
    
    elif choice == "2":
        text = input("\n请输入要转换的文本: ")
        image_path = input("封面图片路径: ").strip('"')
        title = input("播客标题: ")
        description = input("播客描述: ")
        
        generate_and_upload(text, image_path, title, description)
    
    else:
        print("无效选择")

