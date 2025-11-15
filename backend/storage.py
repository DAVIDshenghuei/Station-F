"""
文件存储管理
包含本地存储实现和云存储占位符函数
"""
import os
import uuid
from fastapi import UploadFile
from typing import Tuple, Optional
import re

# 配置
STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local")  # local, s3, supabase, github, gcp
STORAGE_BASE_DIR = "./storage"

# 云存储配置（可选）
S3_BUCKET = os.getenv("S3_BUCKET", "")
S3_REGION = os.getenv("S3_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "podcasts")

GITHUB_REPO = os.getenv("GITHUB_REPO", "")  # 格式: username/repo
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")

GCP_BUCKET = os.getenv("GCP_BUCKET", "")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "")

def sanitize_filename(filename: str) -> str:
    """
    清理文件名，防止路径遍历攻击
    
    参数:
        filename: 原始文件名
    
    返回:
        清理后的文件名
    """
    # 移除路径分隔符
    filename = os.path.basename(filename)
    # 移除特殊字符，只保留字母、数字、点、下划线和连字符
    filename = re.sub(r'[^\w\.\-]', '_', filename)
    return filename

def validate_file(file: UploadFile, allowed_types: list, max_size_mb: int) -> Tuple[bool, Optional[str]]:
    """
    验证上传的文件
    
    参数:
        file: 上传的文件
        allowed_types: 允许的 MIME 类型列表
        max_size_mb: 最大文件大小（MB）
    
    返回:
        (是否有效, 错误信息)
    """
    # 检查文件类型
    if file.content_type not in allowed_types:
        return False, f"不支持的文件类型: {file.content_type}"
    
    # 检查文件大小
    file.file.seek(0, 2)  # 移动到文件末尾
    file_size = file.file.tell()  # 获取文件大小
    file.file.seek(0)  # 重置到开头
    
    max_size_bytes = max_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        return False, f"文件大小超过限制 ({max_size_mb}MB)"
    
    if file_size == 0:
        return False, "文件为空"
    
    return True, None

async def save_file(file: UploadFile, subfolder: str) -> str:
    """
    保存文件（根据配置选择存储后端）
    
    参数:
        file: 上传的文件
        subfolder: 子文件夹名称 (audio 或 images)
    
    返回:
        文件的相对路径
    """
    if STORAGE_BACKEND == "local":
        return await save_file_local(file, subfolder)
    elif STORAGE_BACKEND == "s3":
        return await save_file_s3(file, subfolder)
    elif STORAGE_BACKEND == "supabase":
        return await save_file_supabase(file, subfolder)
    elif STORAGE_BACKEND == "github":
        return await save_file_github(file, subfolder)
    elif STORAGE_BACKEND == "gcp":
        return await save_file_gcp(file, subfolder)
    else:
        return await save_file_local(file, subfolder)

async def save_file_local(file: UploadFile, subfolder: str) -> str:
    """
    本地存储实现
    
    参数:
        file: 上传的文件
        subfolder: 子文件夹名称
    
    返回:
        文件的相对路径
    """
    # 创建存储目录
    storage_dir = os.path.join(STORAGE_BASE_DIR, subfolder)
    os.makedirs(storage_dir, exist_ok=True)
    
    # 生成唯一文件名
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    unique_filename = sanitize_filename(unique_filename)
    
    # 保存文件
    file_path = os.path.join(storage_dir, unique_filename)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # 返回相对路径
    relative_path = f"{subfolder}/{unique_filename}"
    return relative_path

# ==================== 云存储占位符函数 ====================
# 以下函数是占位符，展示如何集成各种云存储服务
# 要使用这些函数，需要安装相应的 SDK 并配置环境变量

async def save_file_s3(file: UploadFile, subfolder: str) -> str:
    """
    AWS S3 存储占位符
    
    TODO: 实现 S3 上传
    
    步骤:
    1. 安装: pip install boto3
    2. 配置环境变量: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET
    3. 取消注释以下代码并根据需要修改
    
    示例代码:
    ```python
    import boto3
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=S3_REGION
    )
    
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    s3_key = f"{subfolder}/{unique_filename}"
    
    content = await file.read()
    
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=s3_key,
        Body=content,
        ContentType=file.content_type
    )
    
    return s3_key
    ```
    """
    # 暂时回退到本地存储
    print("⚠️  S3 存储未配置，使用本地存储")
    return await save_file_local(file, subfolder)

async def save_file_supabase(file: UploadFile, subfolder: str) -> str:
    """
    Supabase Storage 占位符
    
    TODO: 实现 Supabase Storage 上传
    
    步骤:
    1. 安装: pip install supabase
    2. 配置环境变量: SUPABASE_URL, SUPABASE_KEY, SUPABASE_BUCKET
    3. 取消注释以下代码并根据需要修改
    
    示例代码:
    ```python
    from supabase import create_client, Client
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    storage_path = f"{subfolder}/{unique_filename}"
    
    content = await file.read()
    
    response = supabase.storage.from_(SUPABASE_BUCKET).upload(
        path=storage_path,
        file=content,
        file_options={"content-type": file.content_type}
    )
    
    return storage_path
    ```
    """
    # 暂时回退到本地存储
    print("⚠️  Supabase 存储未配置，使用本地存储")
    return await save_file_local(file, subfolder)

async def save_file_github(file: UploadFile, subfolder: str) -> str:
    """
    GitHub Repository 存储占位符
    
    TODO: 实现 GitHub 文件上传
    
    步骤:
    1. 安装: pip install PyGithub
    2. 配置环境变量: GITHUB_REPO, GITHUB_TOKEN, GITHUB_BRANCH
    3. 取消注释以下代码并根据需要修改
    
    示例代码:
    ```python
    from github import Github
    import base64
    
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(GITHUB_REPO)
    
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = f"storage/{subfolder}/{unique_filename}"
    
    content = await file.read()
    content_b64 = base64.b64encode(content).decode()
    
    repo.create_file(
        path=file_path,
        message=f"Upload {subfolder} file",
        content=content_b64,
        branch=GITHUB_BRANCH
    )
    
    return f"{subfolder}/{unique_filename}"
    ```
    """
    # 暂时回退到本地存储
    print("⚠️  GitHub 存储未配置，使用本地存储")
    return await save_file_local(file, subfolder)

async def save_file_gcp(file: UploadFile, subfolder: str) -> str:
    """
    Google Cloud Storage 占位符
    
    TODO: 实现 GCP Cloud Storage 上传
    
    步骤:
    1. 安装: pip install google-cloud-storage
    2. 配置 GCP 认证和环境变量: GCP_BUCKET, GCP_PROJECT_ID
    3. 取消注释以下代码并根据需要修改
    
    示例代码:
    ```python
    from google.cloud import storage
    
    storage_client = storage.Client(project=GCP_PROJECT_ID)
    bucket = storage_client.bucket(GCP_BUCKET)
    
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    blob_name = f"{subfolder}/{unique_filename}"
    
    blob = bucket.blob(blob_name)
    content = await file.read()
    
    blob.upload_from_string(
        content,
        content_type=file.content_type
    )
    
    return blob_name
    ```
    """
    # 暂时回退到本地存储
    print("⚠️  GCP 存储未配置，使用本地存储")
    return await save_file_local(file, subfolder)

# ==================== 存储配置检查 ====================

def check_storage_config():
    """
    检查存储配置是否正确
    
    打印当前配置和警告信息
    """
    print(f"\n📦 存储配置:")
    print(f"  后端: {STORAGE_BACKEND}")
    
    if STORAGE_BACKEND == "local":
        print(f"  本地路径: {STORAGE_BASE_DIR}")
    elif STORAGE_BACKEND == "s3":
        if not S3_BUCKET:
            print("  ⚠️  警告: S3_BUCKET 未配置")
        else:
            print(f"  S3 存储桶: {S3_BUCKET}")
    elif STORAGE_BACKEND == "supabase":
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("  ⚠️  警告: Supabase 配置不完整")
        else:
            print(f"  Supabase 项目: {SUPABASE_URL}")
    elif STORAGE_BACKEND == "github":
        if not GITHUB_REPO or not GITHUB_TOKEN:
            print("  ⚠️  警告: GitHub 配置不完整")
        else:
            print(f"  GitHub 仓库: {GITHUB_REPO}")
    elif STORAGE_BACKEND == "gcp":
        if not GCP_BUCKET:
            print("  ⚠️  警告: GCP_BUCKET 未配置")
        else:
            print(f"  GCP 存储桶: {GCP_BUCKET}")
    
    print()

if __name__ == "__main__":
    check_storage_config()

