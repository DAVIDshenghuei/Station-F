"""
FastAPI 后端 - 播客上传和管理 API
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional, List
import os
from datetime import datetime

from backend.db import init_db, get_db_connection
from backend.models import EpisodeResponse
from backend.storage import save_file, validate_file

# 创建 FastAPI 应用
app = FastAPI(
    title="播客 API",
    description="用于上传和管理播客的 RESTful API",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    init_db()
    print("✅ 数据库已初始化")

# 挂载静态文件目录
if os.path.exists("./storage"):
    app.mount("/storage", StaticFiles(directory="storage"), name="storage")

@app.get("/")
async def root():
    """健康检查端点"""
    return {
        "message": "播客 API 正在运行",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.post("/api/episodes", response_model=EpisodeResponse)
async def create_episode(
    audio_file: UploadFile = File(..., description="音频文件 (mp3, wav, m4a)"),
    image_file: UploadFile = File(..., description="封面图片 (jpg, png, jpeg)"),
    title: str = Form(..., description="播客标题"),
    description: str = Form(..., description="播客描述")
):
    """
    创建新的播客集
    
    接收多部分表单数据：
    - audio_file: 音频文件 (最大 50MB)
    - image_file: 封面图片 (最大 10MB)
    - title: 播客标题
    - description: 播客描述
    """
    try:
        # 验证音频文件
        audio_valid, audio_error = validate_file(
            audio_file,
            allowed_types=["audio/mpeg", "audio/wav", "audio/mp4", "audio/x-m4a"],
            max_size_mb=50
        )
        if not audio_valid:
            raise HTTPException(status_code=400, detail=f"音频文件无效: {audio_error}")
        
        # 验证图片文件
        image_valid, image_error = validate_file(
            image_file,
            allowed_types=["image/jpeg", "image/png", "image/jpg"],
            max_size_mb=10
        )
        if not image_valid:
            raise HTTPException(status_code=400, detail=f"图片文件无效: {image_error}")
        
        # 验证元数据
        if not title or len(title.strip()) == 0:
            raise HTTPException(status_code=400, detail="标题不能为空")
        if not description or len(description.strip()) == 0:
            raise HTTPException(status_code=400, detail="描述不能为空")
        
        # 保存音频文件
        audio_path = await save_file(audio_file, "audio")
        
        # 保存图片文件
        image_path = await save_file(image_file, "images")
        
        # 保存到数据库
        conn = get_db_connection()
        cursor = conn.cursor()
        
        created_at = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO episodes (title, description, audio_path, image_path, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (title, description, audio_path, image_path, created_at))
        
        episode_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # 返回创建的播客信息
        return EpisodeResponse(
            id=episode_id,
            title=title,
            description=description,
            audio_url=f"/storage/{audio_path}",
            image_url=f"/storage/{image_path}",
            created_at=created_at
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

@app.get("/api/episodes", response_model=List[EpisodeResponse])
async def list_episodes():
    """
    获取所有播客列表
    
    返回所有播客的元数据，按创建时间倒序排列
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, description, audio_path, image_path, created_at
            FROM episodes
            ORDER BY created_at DESC
        """)
        
        episodes = []
        for row in cursor.fetchall():
            episodes.append(EpisodeResponse(
                id=row[0],
                title=row[1],
                description=row[2],
                audio_url=f"/storage/{row[3]}",
                image_url=f"/storage/{row[4]}",
                created_at=row[5]
            ))
        
        conn.close()
        
        return episodes
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

@app.get("/api/episodes/{episode_id}", response_model=EpisodeResponse)
async def get_episode(episode_id: int):
    """
    获取单个播客详情
    
    参数:
    - episode_id: 播客 ID
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, description, audio_path, image_path, created_at
            FROM episodes
            WHERE id = ?
        """, (episode_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="播客未找到")
        
        return EpisodeResponse(
            id=row[0],
            title=row[1],
            description=row[2],
            audio_url=f"/storage/{row[3]}",
            image_url=f"/storage/{row[4]}",
            created_at=row[5]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

@app.delete("/api/episodes/{episode_id}")
async def delete_episode(episode_id: int):
    """
    删除播客
    
    参数:
    - episode_id: 播客 ID
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取文件路径
        cursor.execute("""
            SELECT audio_path, image_path
            FROM episodes
            WHERE id = ?
        """, (episode_id,))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise HTTPException(status_code=404, detail="播客未找到")
        
        audio_path, image_path = row
        
        # 从数据库删除
        cursor.execute("DELETE FROM episodes WHERE id = ?", (episode_id,))
        conn.commit()
        conn.close()
        
        # 删除文件
        try:
            if os.path.exists(f"./storage/{audio_path}"):
                os.remove(f"./storage/{audio_path}")
            if os.path.exists(f"./storage/{image_path}"):
                os.remove(f"./storage/{image_path}")
        except Exception as e:
            print(f"⚠️ 警告: 无法删除文件: {str(e)}")
        
        return {"message": "播客已删除", "id": episode_id}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

