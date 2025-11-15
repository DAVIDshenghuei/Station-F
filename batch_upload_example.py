"""
批量上传播客示例
展示如何将多个 11 Labs 生成的音频文件批量上传到系统
"""
from upload_audio import upload_podcast
import os
import time

def batch_upload(episodes_list):
    """
    批量上传播客
    
    参数:
        episodes_list: 播客列表，每个元素包含 audio_path, image_path, title, description
    """
    print(f"📦 准备批量上传 {len(episodes_list)} 个播客\n")
    
    success_count = 0
    failed_count = 0
    
    for i, episode in enumerate(episodes_list, 1):
        print(f"{'='*60}")
        print(f"处理 [{i}/{len(episodes_list)}]: {episode['title']}")
        print(f"{'='*60}")
        
        result = upload_podcast(
            audio_path=episode['audio_path'],
            image_path=episode['image_path'],
            title=episode['title'],
            description=episode['description']
        )
        
        if result['success']:
            success_count += 1
            print(f"✅ 成功: {episode['title']}")
            print(f"   ID: {result['data']['id']}")
            print(f"   音频: http://localhost:8000{result['data']['audio_url']}")
        else:
            failed_count += 1
            print(f"❌ 失败: {episode['title']}")
            print(f"   错误: {result['error']}")
        
        print()
        
        # 添加延迟以避免过载
        if i < len(episodes_list):
            time.sleep(1)
    
    # 汇总
    print(f"\n{'='*60}")
    print(f"📊 上传完成!")
    print(f"{'='*60}")
    print(f"✅ 成功: {success_count}")
    print(f"❌ 失败: {failed_count}")
    print(f"📝 总计: {len(episodes_list)}")
    print(f"\n可以在前端查看: http://localhost:8501")

# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 示例 1: 批量上传已有的音频文件
    episodes = [
        {
            "audio_path": "audio/episode1.mp3",
            "image_path": "images/cover1.jpg",
            "title": "第一集：人工智能简介",
            "description": "在这一集中，我们将介绍人工智能的基本概念..."
        },
        {
            "audio_path": "audio/episode2.mp3",
            "image_path": "images/cover2.jpg",
            "title": "第二集：机器学习基础",
            "description": "深入探讨机器学习的基本原理和应用..."
        },
        {
            "audio_path": "audio/episode3.mp3",
            "image_path": "images/cover3.jpg",
            "title": "第三集：深度学习革命",
            "description": "了解深度学习如何改变世界..."
        }
    ]
    
    print("""
    ⚠️  注意: 这是一个示例脚本
    
    使用前请:
    1. 修改 episodes 列表中的文件路径
    2. 确保所有文件都存在
    3. 确保后端服务正在运行 (http://localhost:8000)
    
    按 Enter 继续，或 Ctrl+C 取消...
    """)
    
    try:
        input()
        
        # 验证文件
        all_files_exist = True
        for ep in episodes:
            if not os.path.exists(ep['audio_path']):
                print(f"❌ 音频文件不存在: {ep['audio_path']}")
                all_files_exist = False
            if not os.path.exists(ep['image_path']):
                print(f"❌ 图片文件不存在: {ep['image_path']}")
                all_files_exist = False
        
        if all_files_exist:
            batch_upload(episodes)
        else:
            print("\n❌ 部分文件不存在，请检查路径")
            print("\n💡 提示: 请修改 episodes 列表中的路径为实际文件路径")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  上传已取消")

