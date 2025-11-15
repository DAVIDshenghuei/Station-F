"""
播客 API 客户端
专为 AI Agent 设计的简单接口
"""
import requests
import base64
from typing import Union, Optional, Dict
from pathlib import Path
import io

class PodcastAPIClient:
    """
    播客 API 客户端
    
    使用示例:
        client = PodcastAPIClient("http://localhost:8000")
        
        # 从文件路径上传
        result = client.upload_from_files(
            audio_path="audio.mp3",
            image_path="cover.jpg",
            title="标题",
            description="描述"
        )
        
        # 从字节数据上传
        result = client.upload_from_bytes(
            audio_bytes=audio_data,
            image_bytes=image_data,
            title="标题",
            description="描述"
        )
        
        # 从 Base64 上传
        result = client.upload_from_base64(
            audio_base64=audio_b64,
            image_base64=image_b64,
            title="标题",
            description="描述"
        )
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        初始化客户端
        
        参数:
            base_url: API 基础 URL
        """
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api/episodes"
    
    def upload_from_files(
        self,
        audio_path: Union[str, Path],
        image_path: Union[str, Path],
        title: str,
        description: str,
        audio_filename: Optional[str] = None,
        image_filename: Optional[str] = None
    ) -> Dict:
        """
        从文件路径上传播客
        
        参数:
            audio_path: 音频文件路径
            image_path: 图片文件路径
            title: 播客标题
            description: 播客描述
            audio_filename: 自定义音频文件名（可选）
            image_filename: 自定义图片文件名（可选）
        
        返回:
            {"success": bool, "data": {...} or "error": str}
        """
        try:
            with open(audio_path, 'rb') as audio_file, open(image_path, 'rb') as image_file:
                audio_bytes = audio_file.read()
                image_bytes = image_file.read()
                
                if not audio_filename:
                    audio_filename = Path(audio_path).name
                if not image_filename:
                    image_filename = Path(image_path).name
                
                return self.upload_from_bytes(
                    audio_bytes=audio_bytes,
                    image_bytes=image_bytes,
                    title=title,
                    description=description,
                    audio_filename=audio_filename,
                    image_filename=image_filename
                )
        
        except FileNotFoundError as e:
            return {"success": False, "error": f"文件不存在: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"读取文件错误: {str(e)}"}
    
    def upload_from_bytes(
        self,
        audio_bytes: bytes,
        image_bytes: bytes,
        title: str,
        description: str,
        audio_filename: str = "audio.mp3",
        image_filename: str = "cover.jpg"
    ) -> Dict:
        """
        从字节数据上传播客（适合 AI Agent 生成的内容）
        
        参数:
            audio_bytes: 音频文件字节数据
            image_bytes: 图片文件字节数据
            title: 播客标题
            description: 播客描述
            audio_filename: 音频文件名
            image_filename: 图片文件名
        
        返回:
            {"success": bool, "data": {...} or "error": str}
        """
        try:
            files = {
                'audio_file': (audio_filename, io.BytesIO(audio_bytes), 'audio/mpeg'),
                'image_file': (image_filename, io.BytesIO(image_bytes), 'image/jpeg')
            }
            
            data = {
                'title': title,
                'description': description
            }
            
            response = requests.post(
                self.api_url,
                files=files,
                data=data,
                timeout=60
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
        
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "无法连接到 API 服务器，请确保后端正在运行"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def upload_from_base64(
        self,
        audio_base64: str,
        image_base64: str,
        title: str,
        description: str,
        audio_filename: str = "audio.mp3",
        image_filename: str = "cover.jpg"
    ) -> Dict:
        """
        从 Base64 编码上传播客
        
        参数:
            audio_base64: Base64 编码的音频数据
            image_base64: Base64 编码的图片数据
            title: 播客标题
            description: 播客描述
            audio_filename: 音频文件名
            image_filename: 图片文件名
        
        返回:
            {"success": bool, "data": {...} or "error": str}
        """
        try:
            audio_bytes = base64.b64decode(audio_base64)
            image_bytes = base64.b64decode(image_base64)
            
            return self.upload_from_bytes(
                audio_bytes=audio_bytes,
                image_bytes=image_bytes,
                title=title,
                description=description,
                audio_filename=audio_filename,
                image_filename=image_filename
            )
        
        except Exception as e:
            return {"success": False, "error": f"Base64 解码错误: {str(e)}"}
    
    def get_all_episodes(self) -> Dict:
        """
        获取所有播客
        
        返回:
            {"success": bool, "data": [...] or "error": str}
        """
        try:
            response = requests.get(self.api_url, timeout=10)
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_episode(self, episode_id: int) -> Dict:
        """
        获取单个播客
        
        参数:
            episode_id: 播客 ID
        
        返回:
            {"success": bool, "data": {...} or "error": str}
        """
        try:
            response = requests.get(f"{self.api_url}/{episode_id}", timeout=10)
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete_episode(self, episode_id: int) -> Dict:
        """
        删除播客
        
        参数:
            episode_id: 播客 ID
        
        返回:
            {"success": bool, "message": str or "error": str}
        """
        try:
            response = requests.delete(f"{self.api_url}/{episode_id}", timeout=10)
            
            if response.status_code == 200:
                return {"success": True, "message": "删除成功"}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def health_check(self) -> bool:
        """
        检查 API 服务是否可用
        
        返回:
            True 如果服务可用，否则 False
        """
        try:
            response = requests.get(self.base_url, timeout=5)
            return response.status_code == 200
        except:
            return False


# ==================== 便捷函数 ====================

def quick_upload(
    audio_path: str,
    image_path: str,
    title: str,
    description: str,
    api_url: str = "http://localhost:8000"
) -> Dict:
    """
    快速上传函数（最简单的方式）
    
    使用示例:
        from podcast_api_client import quick_upload
        
        result = quick_upload(
            audio_path="audio.mp3",
            image_path="cover.jpg",
            title="我的播客",
            description="这是描述"
        )
        
        if result["success"]:
            print(f"上传成功！ID: {result['data']['id']}")
        else:
            print(f"上传失败: {result['error']}")
    """
    client = PodcastAPIClient(api_url)
    return client.upload_from_files(audio_path, image_path, title, description)


def quick_upload_bytes(
    audio_bytes: bytes,
    image_bytes: bytes,
    title: str,
    description: str,
    api_url: str = "http://localhost:8000"
) -> Dict:
    """
    快速上传字节数据（适合 AI Agent）
    
    使用示例:
        from podcast_api_client import quick_upload_bytes
        
        # 假设 AI 生成了音频和图片的字节数据
        result = quick_upload_bytes(
            audio_bytes=ai_generated_audio,
            image_bytes=ai_generated_image,
            title="AI 生成的播客",
            description="这是 AI 生成的内容"
        )
    """
    client = PodcastAPIClient(api_url)
    return client.upload_from_bytes(audio_bytes, image_bytes, title, description)


# ==================== 示例使用 ====================

if __name__ == "__main__":
    # 示例 1: 基本使用
    print("=" * 60)
    print("示例 1: 从文件路径上传")
    print("=" * 60)
    
    client = PodcastAPIClient()
    
    # 检查服务是否可用
    if not client.health_check():
        print("❌ API 服务不可用，请先启动后端服务")
        print("   运行: python -m uvicorn backend.main:app --reload --port 8000")
        exit(1)
    
    print("✅ API 服务可用")
    
    # 示例 2: 使用快捷函数
    print("\n" + "=" * 60)
    print("示例 2: 使用快捷函数")
    print("=" * 60)
    
    # result = quick_upload(
    #     audio_path="path/to/audio.mp3",
    #     image_path="path/to/cover.jpg",
    #     title="测试播客",
    #     description="这是测试"
    # )
    # print(result)
    
    # 示例 3: 模拟 AI Agent 使用字节数据
    print("\n" + "=" * 60)
    print("示例 3: 模拟 AI Agent 上传（字节数据）")
    print("=" * 60)
    print("""
    # AI Agent 伪代码:
    audio_bytes = ai_tts_model.generate("文本内容...")
    image_bytes = ai_image_model.generate("封面提示词...")
    
    result = quick_upload_bytes(
        audio_bytes=audio_bytes,
        image_bytes=image_bytes,
        title="AI 生成的播客",
        description="完全由 AI 生成"
    )
    
    if result["success"]:
        episode_id = result["data"]["id"]
        audio_url = result["data"]["audio_url"]
        print(f"播客已发布！ID: {episode_id}")
    """)

