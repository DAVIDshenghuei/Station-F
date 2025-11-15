# 🎙️ AI Podcast Platform

A modern, minimalist podcast broadcasting platform built with Streamlit and FastAPI. Features a sleek dark interface inspired by contemporary design systems.

## ✨ Features

- **Modern UI**: Clean, minimal interface with pure black theme
- **Fast Performance**: Built on FastAPI for high-performance backend operations
- **Simple Architecture**: SQLite database with local file storage
- **RESTful API**: Well-documented API endpoints for easy integration
- **Responsive Design**: Optimized viewing experience across devices
- **Real-time Updates**: Automatic content refresh and dynamic episode loading

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd "Station F"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

#### Start Backend Server
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

Or use the provided script:
```bash
# Windows
start_backend.bat

# Linux/Mac
./start_backend.sh
```

#### Start Frontend Application
```bash
streamlit run app.py
```

Or use the provided script:
```bash
# Windows
start_frontend.bat

# Linux/Mac
./start_frontend.sh
```

### Access the Platform

- **Frontend**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Alternative Docs**: http://localhost:8000/redoc

## 📁 Project Structure

```
Station F/
├── app.py                 # Streamlit frontend application
├── backend/
│   ├── __init__.py
│   ├── main.py           # FastAPI application & routes
│   ├── models.py         # Pydantic data models
│   ├── db.py             # SQLite database management
│   └── storage.py        # File storage handling
├── storage/              # Local file storage (auto-created)
│   ├── audio/           # Audio files
│   └── images/          # Cover images
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── start_backend.bat    # Windows backend launcher
├── start_backend.sh     # Unix backend launcher
├── start_frontend.bat   # Windows frontend launcher
└── start_frontend.sh    # Unix frontend launcher
```

## 🔧 API Reference

### Endpoints

#### `POST /api/episodes`
Upload a new podcast episode with audio and cover image.

**Request**: `multipart/form-data`
- `audio_file`: Audio file (MP3, WAV, M4A) - Max 50MB
- `image_file`: Cover image (JPG, PNG) - Max 10MB
- `title`: Episode title (string)
- `description`: Episode description (string)

**Response**: `200 OK`
```json
{
  "id": 1,
  "title": "Episode Title",
  "description": "Episode description",
  "audio_url": "/storage/audio/xxx.mp3",
  "image_url": "/storage/images/xxx.jpg",
  "created_at": "2024-11-15T12:00:00"
}
```

#### `GET /api/episodes`
Retrieve all podcast episodes.

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "title": "Episode Title",
    "description": "Episode description",
    "audio_url": "/storage/audio/xxx.mp3",
    "image_url": "/storage/images/xxx.jpg",
    "created_at": "2024-11-15T12:00:00"
  }
]
```

#### `GET /api/episodes/{id}`
Retrieve a specific episode by ID.

#### `DELETE /api/episodes/{id}`
Delete an episode by ID.

## 🛠️ Technology Stack

- **Frontend**: Streamlit 1.31.0
- **Backend**: FastAPI 0.109.0
- **Server**: Uvicorn
- **Database**: SQLite 3
- **File Upload**: Python Multipart
- **Data Validation**: Pydantic 2.5.3

## 📊 Database Schema

### Episodes Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| title | TEXT | Episode title |
| description | TEXT | Episode description |
| audio_path | TEXT | Relative path to audio file |
| image_path | TEXT | Relative path to cover image |
| created_at | TEXT | ISO format timestamp |

## 🔐 Configuration

### Environment Variables

- `API_BASE_URL`: Backend API URL (default: `http://localhost:8000`)
- `STORAGE_BACKEND`: Storage backend type (default: `local`)

### Storage Configuration

The platform uses local file storage by default. Files are stored in:
- Audio: `./storage/audio/`
- Images: `./storage/images/`

Cloud storage integration placeholders are available in `backend/storage.py` for:
- AWS S3
- Supabase Storage
- GitHub Repository
- Google Cloud Storage

## 🎨 Design Philosophy

The platform features a minimalist design inspired by modern developer tools:
- **Pure Black Background** (#000000)
- **Subtle Borders** (#1a1a1a)
- **High Contrast Text** (#ffffff, #888, #555)
- **Large Typography** (Inter font family)
- **Smooth Animations** (0.4s cubic-bezier transitions)
- **Generous Spacing** (Enhanced readability)

## 📝 Development

### Adding New Features

1. **Backend**: Add routes in `backend/main.py`
2. **Models**: Define data schemas in `backend/models.py`
3. **Frontend**: Update UI in `app.py`
4. **Database**: Modify schema in `backend/db.py`

### Code Style

- Follow PEP 8 for Python code
- Use type hints for better code documentation
- Write descriptive docstrings for functions
- Keep functions focused and modular

## 🐛 Troubleshooting

### Backend Connection Error

**Issue**: Frontend cannot connect to backend

**Solution**: 
1. Ensure backend is running on port 8000
2. Check firewall settings
3. Verify `API_BASE_URL` in `app.py`

### File Upload Fails

**Issue**: Files not uploading successfully

**Solution**:
1. Check file size limits (50MB audio, 10MB images)
2. Verify supported formats (MP3/WAV/M4A, JPG/PNG)
3. Ensure `storage/` directory has write permissions

### Database Errors

**Issue**: SQLite database errors

**Solution**:
1. Delete `podcasts.db` to reset database
2. Restart backend to recreate schema
3. Check file permissions in project directory

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on the repository.

---

**Built with ❤️ using Streamlit & FastAPI**
