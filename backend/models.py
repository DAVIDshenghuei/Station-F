"""
Pydantic 模型 - 数据验证和序列化
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class EpisodeResponse(BaseModel):
    """播客响应模型"""
    id: int = Field(..., description="播客 ID")
    title: str = Field(..., description="播客标题")
    description: str = Field(..., description="播客描述")
    audio_url: str = Field(..., description="音频文件 URL")
    image_url: str = Field(..., description="封面图片 URL")
    created_at: str = Field(..., description="创建时间 (ISO 格式)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "第一集：欢迎来到我的播客",
                "description": "这是第一集的介绍...",
                "audio_url": "/storage/audio/episode_1.mp3",
                "image_url": "/storage/images/cover_1.jpg",
                "created_at": "2024-01-01T12:00:00"
            }
        }

class ErrorResponse(BaseModel):
    """错误响应模型"""
    detail: str = Field(..., description="错误详情")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "文件大小超过限制"
            }
        }

