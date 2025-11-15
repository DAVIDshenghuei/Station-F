"""
AI Agent 集成示例
展示如何将 AI 生成的音频和图片上传到播客系统
"""
from podcast_api_client import PodcastAPIClient, quick_upload_bytes
import io
from PIL import Image

# ==================== AI Agent 模拟示例 ====================

def ai_agent_example_1():
    """
    示例 1: AI Agent 生成音频和图片后直接上传
    """
    print("🤖 AI Agent 示例 1: 基本工作流\n")
    
    # 第 1 步: AI 生成音频（这里模拟）
    print("📝 步骤 1: AI 生成音频...")
    # 实际使用时，这里是您的 AI TTS 模型
    # audio_bytes = your_ai_tts_model.generate("播客内容...")
    
    # 模拟：读取一个示例音频文件
    # audio_bytes = open("example_audio.mp3", "rb").read()
    audio_bytes = b"...audio data..."  # 占位符
    
    # 第 2 步: AI 生成封面图片（这里模拟）
    print("🎨 步骤 2: AI 生成封面图片...")
    # 实际使用时，这里是您的 AI 图像模型
    # image_bytes = your_ai_image_model.generate("播客封面，科技感...")
    
    # 模拟：创建一个简单的图片
    # img = Image.new('RGB', (800, 800), color='blue')
    # img_buffer = io.BytesIO()
    # img.save(img_buffer, format='JPEG')
    # image_bytes = img_buffer.getvalue()
    image_bytes = b"...image data..."  # 占位符
    
    # 第 3 步: 上传到播客系统
    print("📤 步骤 3: 上传到播客系统...")
    
    result = quick_upload_bytes(
        audio_bytes=audio_bytes,
        image_bytes=image_bytes,
        title="AI 生成的播客",
        description="这是由 AI 完全自动生成的播客内容",
        api_url="http://localhost:8000"
    )
    
    # 第 4 步: 处理结果
    if result["success"]:
        print("✅ 上传成功！")
        print(f"   播客 ID: {result['data']['id']}")
        print(f"   标题: {result['data']['title']}")
        print(f"   音频 URL: http://localhost:8000{result['data']['audio_url']}")
        print(f"   查看: http://localhost:8501")
    else:
        print(f"❌ 上传失败: {result['error']}")


def ai_agent_example_2_with_real_files():
    """
    示例 2: 从实际的 AI 生成文件上传
    """
    print("\n🤖 AI Agent 示例 2: 使用实际文件\n")
    
    # 假设您的 AI 已经生成了这些文件
    ai_generated_audio = "ai_output/generated_audio.mp3"
    ai_generated_image = "ai_output/generated_cover.jpg"
    
    # 读取 AI 生成的文件
    try:
        with open(ai_generated_audio, 'rb') as f:
            audio_bytes = f.read()
        
        with open(ai_generated_image, 'rb') as f:
            image_bytes = f.read()
        
        # 上传
        result = quick_upload_bytes(
            audio_bytes=audio_bytes,
            image_bytes=image_bytes,
            title="AI 播客第一集",
            description="由先进的 AI 模型生成的播客内容"
        )
        
        if result["success"]:
            print("✅ 上传成功！")
            print(f"   播客 ID: {result['data']['id']}")
        else:
            print(f"❌ 上传失败: {result['error']}")
    
    except FileNotFoundError as e:
        print(f"❌ 文件不存在: {e}")
        print("💡 请将文件路径替换为您实际的 AI 输出路径")


def ai_agent_example_3_class_based():
    """
    示例 3: 使用类的方式（推荐用于复杂系统）
    """
    print("\n🤖 AI Agent 示例 3: 面向对象方式\n")
    
    # 创建客户端
    client = PodcastAPIClient("http://localhost:8000")
    
    # 检查服务是否可用
    if not client.health_check():
        print("❌ 播客 API 服务不可用")
        return
    
    print("✅ 播客 API 服务可用")
    
    # 模拟 AI 生成内容
    print("🤖 AI 正在生成内容...")
    
    # 这里放入您的 AI 生成逻辑
    # audio_bytes = your_ai_model.generate_audio(...)
    # image_bytes = your_ai_model.generate_image(...)
    
    # 示例数据
    # audio_bytes = ...
    # image_bytes = ...
    
    # 上传
    # result = client.upload_from_bytes(
    #     audio_bytes=audio_bytes,
    #     image_bytes=image_bytes,
    #     title="AI 播客",
    #     description="AI 生成的内容",
    #     audio_filename="ai_generated.mp3",
    #     image_filename="ai_cover.jpg"
    # )
    
    print("💡 查看代码了解如何集成您的 AI 模型")


# ==================== 完整的 AI Agent 工作流 ====================

class PodcastAIAgent:
    """
    播客 AI Agent 封装类
    将您的 AI 模型与播客系统集成
    """
    
    def __init__(self, podcast_api_url: str = "http://localhost:8000"):
        """
        初始化 AI Agent
        
        参数:
            podcast_api_url: 播客 API 地址
        """
        self.podcast_client = PodcastAPIClient(podcast_api_url)
        self.api_url = podcast_api_url
    
    def generate_and_publish(
        self,
        text_content: str,
        title: str,
        description: str,
        cover_prompt: str = None
    ) -> dict:
        """
        完整工作流：生成内容并发布
        
        参数:
            text_content: 要转换成音频的文本
            title: 播客标题
            description: 播客描述
            cover_prompt: 封面图片生成提示词
        
        返回:
            {"success": bool, "data": {...} or "error": str}
        """
        print(f"🤖 开始处理: {title}")
        
        # 步骤 1: 生成音频
        print("  🎙️ 生成音频...")
        audio_bytes = self._generate_audio(text_content)
        if not audio_bytes:
            return {"success": False, "error": "音频生成失败"}
        
        # 步骤 2: 生成封面
        print("  🎨 生成封面...")
        image_bytes = self._generate_image(cover_prompt or title)
        if not image_bytes:
            return {"success": False, "error": "图片生成失败"}
        
        # 步骤 3: 上传
        print("  📤 上传到播客系统...")
        result = self.podcast_client.upload_from_bytes(
            audio_bytes=audio_bytes,
            image_bytes=image_bytes,
            title=title,
            description=description
        )
        
        if result["success"]:
            print(f"  ✅ 发布成功！ID: {result['data']['id']}")
        else:
            print(f"  ❌ 发布失败: {result['error']}")
        
        return result
    
    def _generate_audio(self, text: str) -> bytes:
        """
        生成音频（集成您的 TTS 模型）
        
        TODO: 在这里集成您的 AI TTS 模型
        例如: 11 Labs, Azure TTS, Google TTS, 或自定义模型
        """
        # 示例实现：
        # from elevenlabs import generate, save
        # audio = generate(text=text, voice="Rachel")
        # return audio
        
        # 暂时返回 None（需要您实现）
        return None
    
    def _generate_image(self, prompt: str) -> bytes:
        """
        生成图片（集成您的图像生成模型）
        
        TODO: 在这里集成您的 AI 图像模型
        例如: DALL-E, Stable Diffusion, Midjourney API, 或自定义模型
        """
        # 示例实现：
        # import openai
        # response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
        # image_url = response['data'][0]['url']
        # image_bytes = requests.get(image_url).content
        # return image_bytes
        
        # 暂时返回 None（需要您实现）
        return None
    
    def batch_publish(self, episodes: list) -> list:
        """
        批量发布播客
        
        参数:
            episodes: 播客列表，每个包含 text, title, description
        
        返回:
            结果列表
        """
        results = []
        for i, episode in enumerate(episodes, 1):
            print(f"\n处理 [{i}/{len(episodes)}]: {episode['title']}")
            result = self.generate_and_publish(
                text_content=episode['text'],
                title=episode['title'],
                description=episode['description']
            )
            results.append(result)
        
        return results


# ==================== 使用示例 ====================

def main():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║              🤖 AI Agent 播客集成示例                      ║
    ╚════════════════════════════════════════════════════════════╝
    
    本文件展示了如何将您的 AI Agent 与播客系统集成。
    
    集成步骤:
    1. 使用 PodcastAPIClient 类连接播客 API
    2. 将 AI 生成的音频和图片（bytes）传入 upload_from_bytes()
    3. 处理返回结果
    
    示例包括:
    - 基本工作流（示例 1）
    - 从文件上传（示例 2）
    - 面向对象方式（示例 3）
    - 完整的 AI Agent 封装类
    
    选择要运行的示例:
    """)
    
    print("1. 基本工作流示例")
    print("2. 从文件上传示例")
    print("3. 面向对象示例")
    print("4. 查看 AI Agent 类")
    
    choice = input("\n请选择 (1-4): ")
    
    if choice == "1":
        ai_agent_example_1()
    elif choice == "2":
        ai_agent_example_2_with_real_files()
    elif choice == "3":
        ai_agent_example_3_class_based()
    elif choice == "4":
        print("\n查看 PodcastAIAgent 类的源代码了解如何集成")
        print("您需要实现 _generate_audio() 和 _generate_image() 方法")
    else:
        print("无效选择")


if __name__ == "__main__":
    main()

