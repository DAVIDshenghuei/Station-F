"""
最简单的 AI Agent 上传示例
3 行代码完成上传
"""
from podcast_api_client import quick_upload_bytes

# ==================== 方式 1: 最简单的使用 ====================

def simplest_example():
    """
    最简单的例子：假设您的 AI 已经生成了字节数据
    """
    # 您的 AI 生成的数据
    audio_bytes = your_ai_generate_audio()  # 替换为您的 AI 函数
    image_bytes = your_ai_generate_image()  # 替换为您的 AI 函数
    
    # 一行代码上传
    result = quick_upload_bytes(
        audio_bytes=audio_bytes,
        image_bytes=image_bytes,
        title="AI 播客",
        description="AI 生成的内容"
    )
    
    # 处理结果
    if result["success"]:
        print(f"✅ 成功！播客 ID: {result['data']['id']}")
    else:
        print(f"❌ 失败: {result['error']}")


# ==================== 方式 2: 从文件上传 ====================

def upload_from_files_example():
    """
    如果您的 AI 已经生成了文件
    """
    from podcast_api_client import quick_upload
    
    result = quick_upload(
        audio_path="path/to/ai_generated_audio.mp3",
        image_path="path/to/ai_generated_cover.jpg",
        title="我的播客",
        description="描述"
    )
    
    print(result)


# ==================== 方式 3: 实际可运行的例子 ====================

def working_example():
    """
    实际可运行的例子（需要真实文件）
    """
    import os
    
    # 输入您的文件路径
    print("🤖 AI Agent 上传工具\n")
    
    audio_path = input("音频文件路径: ").strip('"')
    image_path = input("图片文件路径: ").strip('"')
    
    # 检查文件
    if not os.path.exists(audio_path):
        print(f"❌ 音频文件不存在: {audio_path}")
        return
    
    if not os.path.exists(image_path):
        print(f"❌ 图片文件不存在: {image_path}")
        return
    
    # 读取文件
    with open(audio_path, 'rb') as f:
        audio_bytes = f.read()
    
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    # 上传
    print("\n📤 上传中...")
    result = quick_upload_bytes(
        audio_bytes=audio_bytes,
        image_bytes=image_bytes,
        title=input("标题: "),
        description=input("描述: ")
    )
    
    # 结果
    if result["success"]:
        data = result["data"]
        print(f"""
    ╔════════════════════════════════════════════════════════╗
    ║                   ✅ 上传成功！                        ║
    ╚════════════════════════════════════════════════════════╝
    
    播客 ID: {data['id']}
    标题: {data['title']}
    
    🎵 音频: http://localhost:8000{data['audio_url']}
    🖼️  封面: http://localhost:8000{data['image_url']}
    
    🌐 查看播客: http://localhost:8501
        """)
    else:
        print(f"\n❌ 上传失败: {result['error']}")


# ==================== 实际集成示例 ====================

class SimpleAIAgent:
    """
    简单的 AI Agent 封装
    将这个类集成到您的 AI 系统中
    """
    
    def __init__(self, api_url="http://localhost:8000"):
        from podcast_api_client import PodcastAPIClient
        self.client = PodcastAPIClient(api_url)
    
    def publish(self, audio_bytes: bytes, image_bytes: bytes, title: str, description: str):
        """
        发布播客的唯一方法
        
        参数:
            audio_bytes: AI 生成的音频字节数据
            image_bytes: AI 生成的图片字节数据
            title: 播客标题
            description: 播客描述
        
        返回:
            播客 ID (成功) 或 None (失败)
        """
        result = self.client.upload_from_bytes(
            audio_bytes=audio_bytes,
            image_bytes=image_bytes,
            title=title,
            description=description
        )
        
        if result["success"]:
            return result["data"]["id"]
        else:
            print(f"错误: {result['error']}")
            return None


# ==================== 使用示例 ====================

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║            🤖 AI Agent 最简单上传示例                     ║
    ╚═══════════════════════════════════════════════════════════╝
    
    选择模式:
    1. 实际上传（需要文件路径）
    2. 查看代码示例
    3. 使用 SimpleAIAgent 类
    """)
    
    choice = input("请选择 (1-3): ")
    
    if choice == "1":
        working_example()
    
    elif choice == "2":
        print("""
    代码示例:
    
    # 最简单的方式
    from podcast_api_client import quick_upload_bytes
    
    result = quick_upload_bytes(
        audio_bytes=your_ai_audio,
        image_bytes=your_ai_image,
        title="标题",
        description="描述"
    )
    
    if result["success"]:
        print(f"成功！ID: {result['data']['id']}")
        """)
    
    elif choice == "3":
        print("""
    使用 SimpleAIAgent 类:
    
    # 1. 创建实例
    agent = SimpleAIAgent()
    
    # 2. 发布（一行代码）
    episode_id = agent.publish(
        audio_bytes=your_audio,
        image_bytes=your_image,
        title="标题",
        description="描述"
    )
    
    # 3. 检查结果
    if episode_id:
        print(f"✅ 播客 ID: {episode_id}")
    else:
        print("❌ 上传失败")
        """)
    
    else:
        print("无效选择")


# ==================== 您的 AI 生成函数（示例） ====================

def your_ai_generate_audio():
    """
    TODO: 替换为您实际的 AI 音频生成函数
    
    示例:
    - 使用 11 Labs TTS
    - 使用 Azure TTS
    - 使用自定义模型
    
    返回: bytes (音频数据)
    """
    # return elevenlabs.generate(text="...")
    # return azure_tts.synthesize(text="...")
    # return your_custom_model.generate(text="...")
    pass


def your_ai_generate_image():
    """
    TODO: 替换为您实际的 AI 图像生成函数
    
    示例:
    - 使用 DALL-E
    - 使用 Stable Diffusion
    - 使用自定义模型
    
    返回: bytes (图片数据)
    """
    # return dalle.generate(prompt="...")
    # return stable_diffusion.generate(prompt="...")
    # return your_custom_model.generate(prompt="...")
    pass

