# 🚀 快速启动指南

## Windows 用户

### 方法 1: 使用批处理文件

1. **安装依赖**
```cmd
pip install -r requirements.txt
```

2. **启动后端** - 双击 `start_backend.bat`
   - 或在命令提示符中运行：`start_backend.bat`

3. **启动前端** - 双击 `start_frontend.bat`
   - 或在命令提示符中运行：`start_frontend.bat`

### 方法 2: 手动启动

1. 打开第一个命令提示符窗口，运行：
```cmd
python -m uvicorn backend.main:app --reload --port 8000
```

2. 打开第二个命令提示符窗口，运行：
```cmd
streamlit run app.py
```

## Linux/Mac 用户

### 方法 1: 使用 Shell 脚本

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **赋予脚本执行权限**
```bash
chmod +x start_backend.sh start_frontend.sh
```

3. **启动后端** - 在一个终端运行：
```bash
./start_backend.sh
```

4. **启动前端** - 在另一个终端运行：
```bash
./start_frontend.sh
```

### 方法 2: 手动启动

1. 打开第一个终端，运行：
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

2. 打开第二个终端，运行：
```bash
streamlit run app.py
```

## 访问应用

- **前端界面**: http://localhost:8501 （会自动打开浏览器）
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs

## 测试上传

1. 准备一个音频文件（MP3、WAV 或 M4A）
2. 准备一个封面图片（JPG 或 PNG）
3. 在前端侧边栏中上传文件
4. 填写标题和描述
5. 点击"发布播客"

## 故障排除

### 端口已被占用

如果端口 8000 或 8501 已被占用，可以修改端口：

**后端**:
```bash
python -m uvicorn backend.main:app --reload --port 8001
```

**前端**（需要同时修改 app.py 中的 API_BASE_URL）:
```bash
streamlit run app.py --server.port 8502
```

### 依赖安装失败

尝试升级 pip：
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 后端无法启动

确保在项目根目录下运行命令，且 backend 文件夹存在。

---

**祝您使用愉快！** 🎉

