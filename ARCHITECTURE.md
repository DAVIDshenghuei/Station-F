# 🏗️ Architecture Overview

## System Design

The AI Podcast Platform follows a clean, modern architecture with clear separation of concerns.

### Architecture Diagram

```
┌─────────────────┐
│   Streamlit     │
│    Frontend     │  ← User Interface (Port 8501)
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│    FastAPI      │
│     Backend     │  ← REST API (Port 8000)
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────┐
│ SQLite │ │  Local   │
│   DB   │ │ Storage  │
└────────┘ └──────────┘
```

## Components

### Frontend (`app.py`)
- **Framework**: Streamlit 1.31.0
- **Purpose**: Display podcast episodes in a modern, minimal interface
- **Features**:
  - Hero section with animated title
  - Episode cards with cover images
  - Inline audio players
  - Responsive design
  - Auto-refresh functionality

### Backend (`backend/`)

#### `main.py` - API Server
- **Framework**: FastAPI 0.109.0
- **Endpoints**:
  - `POST /api/episodes` - Upload new episode
  - `GET /api/episodes` - List all episodes
  - `GET /api/episodes/{id}` - Get specific episode
  - `DELETE /api/episodes/{id}` - Delete episode
- **Features**:
  - File validation
  - CORS middleware
  - Static file serving
  - Error handling

#### `models.py` - Data Models
- **Framework**: Pydantic 2.5.3
- **Models**:
  - `EpisodeResponse` - Episode data structure
  - Automatic validation
  - JSON serialization

#### `db.py` - Database Layer
- **Database**: SQLite 3
- **Schema**: Episodes table
- **Operations**:
  - Auto-initialization
  - Connection management
  - CRUD operations

#### `storage.py` - File Management
- **Storage**: Local filesystem
- **Features**:
  - File validation (type, size)
  - Secure filename sanitization
  - Path management
  - Cloud storage placeholders

## Data Flow

### Episode Upload (API)
```
1. Client sends multipart/form-data
2. FastAPI receives and validates files
3. Files saved to ./storage/
4. Metadata saved to SQLite
5. Response with episode data
```

### Episode Display
```
1. Frontend requests episodes
2. Backend queries SQLite
3. Returns episode list with URLs
4. Frontend renders cards
5. Audio streams from static files
```

## File Structure

```
Station F/
├── app.py                      # Frontend application
├── backend/
│   ├── __init__.py
│   ├── main.py                # API routes & server
│   ├── models.py              # Data schemas
│   ├── db.py                  # Database layer
│   └── storage.py             # File handling
├── storage/                   # File storage (auto-created)
│   ├── audio/                # Audio files
│   └── images/               # Cover images
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
├── ARCHITECTURE.md          # This file
├── start_backend.bat/.sh    # Backend launchers
└── start_frontend.bat/.sh   # Frontend launchers
```

## Technology Choices

### Why Streamlit?
- Rapid UI development
- Python-native (no JavaScript required)
- Built-in components (audio player, image display)
- Auto-refresh capabilities
- Easy deployment

### Why FastAPI?
- High performance (async support)
- Automatic API documentation
- Type validation with Pydantic
- Modern Python features
- Easy to test and maintain

### Why SQLite?
- Zero configuration
- File-based (no server required)
- ACID compliance
- Sufficient for small to medium datasets
- Easy backup and migration

### Why Local Storage?
- Simple implementation
- No external dependencies
- Fast access
- Easy to backup
- Suitable for single-server deployments

## Security Considerations

### Implemented
- File type validation
- File size limits
- Filename sanitization
- Path traversal prevention
- CORS configuration
- Input validation

### Production Recommendations
- Add authentication/authorization
- Implement rate limiting
- Use HTTPS
- Add file content scanning
- Move to cloud storage
- Use production database (PostgreSQL)
- Add request logging
- Implement backup strategy

## Scalability

### Current Limitations
- Single server deployment
- Local file storage
- SQLite database
- No caching layer
- No CDN integration

### Scaling Path
1. **Phase 1** (Current)
   - Local storage
   - SQLite
   - Single server

2. **Phase 2** (Light traffic)
   - Cloud storage (S3/Supabase)
   - Keep SQLite
   - Add CDN

3. **Phase 3** (Medium traffic)
   - Cloud storage + CDN
   - PostgreSQL/MySQL
   - Redis caching
   - Load balancer

4. **Phase 4** (High traffic)
   - Microservices
   - Distributed storage
   - Database replication
   - Message queue
   - Auto-scaling

## API Design Principles

### RESTful
- Resources: `/api/episodes`
- Standard methods: GET, POST, DELETE
- Status codes: 200, 400, 404, 500
- JSON responses

### Consistency
- Uniform error format
- Predictable URLs
- Clear naming conventions

### Documentation
- OpenAPI/Swagger spec
- Auto-generated docs
- Example requests/responses

## Performance

### Current Metrics
- **API Response Time**: < 100ms (local)
- **File Upload**: Depends on file size and network
- **Page Load**: < 2s (without episodes)
- **Episode Render**: < 1s per episode

### Optimization Opportunities
- Lazy loading for episodes
- Image optimization/compression
- Audio file compression
- Response caching
- Database indexing
- CDN for static assets

## Monitoring & Debugging

### Development
- Browser DevTools (frontend)
- FastAPI /docs (API testing)
- SQLite browser (database inspection)
- Python debugger (backend)

### Production Recommendations
- Application monitoring (New Relic, DataDog)
- Error tracking (Sentry)
- Log aggregation (ELK stack)
- Uptime monitoring
- Performance metrics

## Deployment

### Local Development
```bash
# Terminal 1
python -m uvicorn backend.main:app --reload --port 8000

# Terminal 2
streamlit run app.py
```

### Production Options
1. **Docker**
   - Containerize both apps
   - Use docker-compose
   - Easy scaling

2. **Cloud Platforms**
   - Heroku
   - Railway
   - Render
   - DigitalOcean App Platform

3. **Traditional Server**
   - systemd services
   - nginx reverse proxy
   - Let's Encrypt SSL

## Future Enhancements

### Planned Features
- [ ] User authentication
- [ ] Episode categories/tags
- [ ] Search functionality
- [ ] Playlist creation
- [ ] RSS feed generation
- [ ] Analytics dashboard
- [ ] Comment system
- [ ] Like/favorite episodes

### Technical Improvements
- [ ] Add caching layer
- [ ] Implement CDN
- [ ] Add database migrations
- [ ] Create admin panel
- [ ] Add automated tests
- [ ] CI/CD pipeline
- [ ] Docker support
- [ ] Cloud storage integration

---

**Last Updated**: November 2024

