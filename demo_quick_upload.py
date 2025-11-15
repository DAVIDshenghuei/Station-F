"""
快速演示：从 11 Labs 音频上传到播客系统
这是一个简化的演示脚本，展示完整工作流程
"""
import requests
import os
from pathlib import Path

def quick_upload_demo():
    """
    快速上传演示
    假设您已经有了 11 Labs 生成的音频文件
    """
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         🎙️  11 Labs 音频快速上传到播客系统               ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # 配置
    API_URL = "http://localhost:8000"
    
    # 步骤 1: 检查后端服务
    print("📡 步骤 1: 检查后端服务...")
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            print("   ✅ 后端服务运行正常")
        else:
            print("   ⚠️  后端服务响应异常")
            return
    except requests.exceptions.ConnectionError:
        print("   ❌ 无法连接到后端服务")
        print("   💡 请先运行: python -m uvicorn backend.main:app --reload --port 8000")
        return
    
    # 步骤 2: 获取文件路径
    print("\n📁 步骤 2: 选择文件")
    print("   请输入文件路径（拖动文件到此处，或输入完整路径）:\n")
    
    audio_path = input("   🎵 音频文件 (MP3/WAV/M4A): ").strip('"').strip()
    
    if not os.path.exists(audio_path):
        print(f"   ❌ 文件不存在: {audio_path}")
        return
    
    image_path = input("   🖼️  封面图片 (JPG/PNG): ").strip('"').strip()
    
    if not os.path.exists(image_path):
        print(f"   ❌ 文件不存在: {image_path}")
        return
    
    # 步骤 3: 输入元数据
    print("\n📝 步骤 3: 输入播客信息")
    title = input("   标题: ")
    description = input("   描述: ")
    
    if not title or not description:
        print("   ❌ 标题和描述不能为空")
        return
    
    # 步骤 4: 上传
    print("\n🚀 步骤 4: 上传中...")
    
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
            
            response = requests.post(
                f"{API_URL}/api/episodes",
                files=files,
                data=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                    ✅ 上传成功！                          ║
    ╚═══════════════════════════════════════════════════════════╝
                """)
                
                print(f"    📌 播客 ID: {result['id']}")
                print(f"    📝 标题: {result['title']}")
                print(f"    🎵 音频 URL: {API_URL}{result['audio_url']}")
                print(f"    🖼️  图片 URL: {API_URL}{result['image_url']}")
                print(f"    📅 创建时间: {result['created_at']}")
                
                print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║  🌐 前端查看                                              ║
    ║  打开浏览器访问: http://localhost:8501                    ║
    ╚═══════════════════════════════════════════════════════════╝
                """)
                
                # 自动测试播放 URL
                print("    🔗 测试直接访问:")
                print(f"       音频: {API_URL}{result['audio_url']}")
                print(f"       (可以在浏览器中打开此链接测试)")
                
            else:
                print(f"\n    ❌ 上传失败")
                print(f"    错误代码: {response.status_code}")
                print(f"    错误信息: {response.text}")
    
    except Exception as e:
        print(f"\n    ❌ 发生错误: {str(e)}")

def test_api_connection():
    """测试 API 连接"""
    API_URL = "http://localhost:8000"
    
    print("🔍 测试后端连接...")
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ 后端连接正常")
            
            # 获取现有播客
            response = requests.get(f"{API_URL}/api/episodes", timeout=5)
            if response.status_code == 200:
                episodes = response.json()
                print(f"📚 当前已有 {len(episodes)} 个播客")
                
                if episodes:
                    print("\n最近的播客:")
                    for ep in episodes[:3]:
                        print(f"   - {ep['title']} (ID: {ep['id']})")
            
            return True
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端")
        print("💡 请先运行: python -m uvicorn backend.main:app --reload --port 8000")
        return False
    
    return False

if __name__ == "__main__":
    import sys
    
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_api_connection()
    else:
        quick_upload_demo()

