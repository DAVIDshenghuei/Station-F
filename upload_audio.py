"""
上传音频文件到播客系统的脚本
支持直接上传本地音频文件（包括 11 Labs 生成的音频）
"""
import requests
import os
from pathlib import Path

# 配置
API_BASE_URL = "http://localhost:8000"

def upload_podcast(
    audio_path: str,
    image_path: str,
    title: str,
    description: str,
    api_url: str = API_BASE_URL
):
    """
    上传播客到后端 API
    
    参数:
        audio_path: 音频文件路径
        image_path: 封面图片路径
        title: 播客标题
        description: 播客描述
        api_url: API 基础 URL
    
    返回:
        上传结果（字典）
    """
    # 检查文件是否存在
    if not os.path.exists(audio_path):
        return {"success": False, "error": f"音频文件不存在: {audio_path}"}
    
    if not os.path.exists(image_path):
        return {"success": False, "error": f"图片文件不存在: {image_path}"}
    
    try:
        # 准备文件
        with open(audio_path, 'rb') as audio_file, open(image_path, 'rb') as image_file:
            files = {
                'audio_file': (os.path.basename(audio_path), audio_file, 'audio/mpeg'),
                'image_file': (os.path.basename(image_path), image_file, 'image/jpeg')
            }
            
            data = {
                'title': title,
                'description': description
            }
            
            # 发送 POST 请求
            response = requests.post(
                f"{api_url}/api/episodes",
                files=files,
                data=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "data": result,
                    "message": "✅ 上传成功！"
                }
            else:
                return {
                    "success": False,
                    "error": f"上传失败: {response.status_code} - {response.text}"
                }
    
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "无法连接到后端服务器。请确保 FastAPI 服务正在运行 (http://localhost:8000)"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"发生错误: {str(e)}"
        }

def main():
    """主函数 - 示例用法"""
    print("🎙️ 播客上传工具\n")
    
    # 方式 1: 手动输入信息
    audio_path = input("请输入音频文件路径: ").strip('"')
    image_path = input("请输入封面图片路径: ").strip('"')
    title = input("请输入播客标题: ")
    description = input("请输入播客描述: ")
    
    print("\n正在上传...")
    result = upload_podcast(audio_path, image_path, title, description)
    
    if result["success"]:
        print(f"\n{result['message']}")
        print(f"播客 ID: {result['data']['id']}")
        print(f"标题: {result['data']['title']}")
        print(f"音频 URL: {API_BASE_URL}{result['data']['audio_url']}")
        print(f"图片 URL: {API_BASE_URL}{result['data']['image_url']}")
        print(f"\n可以在前端查看: http://localhost:8501")
    else:
        print(f"\n❌ {result['error']}")

# 示例用法（取消注释下面的代码直接使用）
def upload_example():
    """
    快速上传示例 - 修改这里的路径和信息
    """
    result = upload_podcast(
        audio_path="path/to/your/audio.mp3",  # 修改为您的音频路径
        image_path="path/to/your/cover.jpg",  # 修改为您的图片路径
        title="我的播客标题",
        description="这是播客描述"
    )
    
    if result["success"]:
        print(f"✅ {result['message']}")
        print(f"音频 URL: {API_BASE_URL}{result['data']['audio_url']}")
    else:
        print(f"❌ {result['error']}")

if __name__ == "__main__":
    # 交互式上传
    main()
    
    # 或者使用快速上传（取消下面的注释）
    # upload_example()

