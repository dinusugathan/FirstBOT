# Developer Guide - EduChat Course Enquiry Assistant

## Table of Contents

1. [Quick Start](#quick-start)
2. [Development Environment Setup](#development-environment-setup)
3. [Project Architecture](#project-architecture)
4. [Development Workflow](#development-workflow)
5. [Testing Strategy](#testing-strategy)
6. [Deployment Guide](#deployment-guide)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)
9. [Contributing Guidelines](#contributing-guidelines)

## Quick Start

### Prerequisites

- Python 3.8+ installed
- pip package manager
- Git for version control
- Google Gemini API key

### 5-Minute Setup

```bash
# Clone the repository
git clone <repository-url>
cd educhat

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (replace with your API key)
export GENAI_KEY="your-google-gemini-api-key"
export PORT=10000

# Run the application
python app.py
```

Visit `http://localhost:10000` to see the application running.

## Development Environment Setup

### Recommended IDE Setup

**Visual Studio Code Extensions**:
- Python
- Pylance
- FastAPI snippets
- Tailwind CSS IntelliSense
- REST Client (for API testing)

**PyCharm Setup**:
- Configure Python interpreter to use virtual environment
- Enable FastAPI support
- Set up code style to follow PEP 8

### Virtual Environment Management

```bash
# Create environment
python -m venv venv

# Activate environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy  # Additional dev tools

# Deactivate when done
deactivate
```

### Environment Variables

Create a `.env` file in the project root:

```bash
# .env file
GENAI_KEY=your-google-gemini-api-key
PORT=10000
DEBUG=True
LOG_LEVEL=INFO
```

**Loading Environment Variables**:
```python
# Add to app.py if using python-dotenv
from dotenv import load_dotenv
load_dotenv()

GENAI_KEY = os.getenv("GENAI_KEY")
```

### Development Dependencies

```bash
# Install additional development tools
pip install pytest pytest-asyncio pytest-cov
pip install black isort flake8 mypy
pip install httpx  # For testing FastAPI endpoints
pip install pre-commit  # For git hooks
```

## Project Architecture

### Directory Structure

```
educhat/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version for deployment
├── data/
│   ├── courses.json      # Course catalog data
│   └── instructors.json  # Instructor information
├── templates/
│   └── index.html        # Frontend chat interface
├── tests/                # Test files (to be created)
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_data.py
│   └── test_embeddings.py
├── docs/                 # Documentation
│   ├── API_DOCUMENTATION.md
│   ├── FRONTEND_DOCUMENTATION.md
│   ├── DATA_SCHEMAS.md
│   └── DEVELOPER_GUIDE.md
└── .gitignore
```

### Application Layers

1. **API Layer** (`app.py` - Routes)
   - FastAPI route handlers
   - Request/response models
   - Error handling

2. **Business Logic Layer** (`app.py` - Functions)
   - Semantic similarity search
   - Context formatting
   - Prompt construction

3. **Data Layer** (`data/` directory)
   - JSON data files
   - Pre-computed embeddings
   - Session storage

4. **Presentation Layer** (`templates/`)
   - HTML templates
   - CSS styling
   - JavaScript functionality

### Key Components

```python
# Core Application Components
app = FastAPI()           # Main FastAPI application
sentence_model = ...      # Sentence transformer model
courses = [...]           # Course data
instructors = [...]       # Instructor data
course_embeddings = {...} # Pre-computed course embeddings
instructor_embeddings = {...} # Pre-computed instructor embeddings
```

## Development Workflow

### 1. Feature Development Process

```bash
# 1. Create feature branch
git checkout -b feature/new-feature-name

# 2. Make changes
# Edit code, add tests, update documentation

# 3. Run tests
pytest tests/

# 4. Code formatting
black app.py
isort app.py

# 5. Lint code
flake8 app.py
mypy app.py

# 6. Commit changes
git add .
git commit -m "feat: add new feature description"

# 7. Push and create pull request
git push origin feature/new-feature-name
```

### 2. Code Style Guidelines

**Python Code Style**:
```python
# Use Black formatter settings
line-length = 88
target-version = ['py38']

# Import organization (isort)
from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import json

# Function documentation
def retrieve_relevant_info(query: str) -> tuple[list, list]:
    """
    Retrieve relevant courses and instructors based on query.
    
    Args:
        query: User's search query string
        
    Returns:
        tuple: (matched_courses, matched_instructors)
    """
    pass
```

**Frontend Code Style**:
```javascript
// Use consistent indentation (2 spaces)
// Use camelCase for variables
// Add comments for complex logic

async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Rest of function...
}
```

### 3. Testing Workflow

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_query"
```

### 4. Documentation Updates

When adding new features:

1. **Update API Documentation**: Add new endpoints to `API_DOCUMENTATION.md`
2. **Update Data Schemas**: Document new data structures in `DATA_SCHEMAS.md`
3. **Update Frontend Docs**: Document UI changes in `FRONTEND_DOCUMENTATION.md`
4. **Update Developer Guide**: Add setup or workflow changes

## Testing Strategy

### Test Structure

```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_home_endpoint():
    """Test the home page endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_query_endpoint():
    """Test the course query endpoint."""
    response = client.post(
        "/api/query",
        json={"query": "Python courses", "conversationId": "test-id"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], str)

def test_translate_endpoint():
    """Test the translation endpoint."""
    response = client.post(
        "/api/translate",
        json={
            "text": "Hello world",
            "target_lang": "es",
            "conversationId": "test-id"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "translation" in data
```

### Data Testing

```python
# tests/test_data.py
import json
import pytest

def test_courses_data_structure():
    """Test courses.json has correct structure."""
    with open("data/courses.json", "r") as f:
        courses = json.load(f)
    
    assert isinstance(courses, list)
    for course in courses:
        assert "name" in course
        assert "description" in course
        assert "instructor" in course
        assert "duration" in course

def test_data_consistency():
    """Test consistency between courses and instructors."""
    with open("data/courses.json", "r") as f:
        courses = json.load(f)
    with open("data/instructors.json", "r") as f:
        instructors = json.load(f)
    
    instructor_names = {inst["name"] for inst in instructors}
    
    for course in courses:
        assert course["instructor"] in instructor_names
```

### Embedding Testing

```python
# tests/test_embeddings.py
import numpy as np
from sentence_transformers import SentenceTransformer

def test_embedding_generation():
    """Test sentence transformer model."""
    model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
    text = "Python programming course"
    embedding = model.encode(text)
    
    assert isinstance(embedding, np.ndarray)
    assert embedding.shape == (384,)
    assert not np.isnan(embedding).any()

def test_similarity_calculation():
    """Test cosine similarity calculation."""
    from sklearn.metrics.pairwise import cosine_similarity
    
    vec1 = np.array([[1, 0, 1]])
    vec2 = np.array([[1, 1, 0]])
    
    similarity = cosine_similarity(vec1, vec2)[0][0]
    assert 0 <= similarity <= 1
```

### Frontend Testing

```javascript
// tests/frontend.test.js (if using Jest)
describe('Chat Interface', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <div id="messages"></div>
            <input id="userInput" />
        `;
    });

    test('should add message to chat', () => {
        addMessage('Test message', 'user');
        
        const messages = document.getElementById('messages');
        expect(messages.children.length).toBe(1);
        expect(messages.textContent).toContain('Test message');
    });

    test('should clear input after sending', () => {
        const input = document.getElementById('userInput');
        input.value = 'Test input';
        
        // Simulate send message
        sendMessage();
        
        expect(input.value).toBe('');
    });
});
```

## Deployment Guide

### Local Deployment

```bash
# Production-like local deployment
export GENAI_KEY="your-api-key"
export PORT=8000
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

EXPOSE 10000

CMD ["python", "app.py"]
```

```bash
# Build and run Docker container
docker build -t educhat .
docker run -p 10000:10000 -e GENAI_KEY="your-api-key" educhat
```

### Cloud Deployment

#### Render.com

1. Connect GitHub repository
2. Set environment variables:
   - `GENAI_KEY`: Your Google Gemini API key
3. Deploy automatically on push to main branch

#### Heroku

```bash
# Heroku deployment
heroku create your-app-name
heroku config:set GENAI_KEY="your-api-key"
git push heroku main
```

#### Railway

```bash
# Railway deployment
railway login
railway init
railway add
railway deploy
```

### Environment-Specific Configuration

```python
# config.py (if implementing environment configs)
import os
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"

class Config:
    def __init__(self):
        self.env = Environment(os.getenv("ENVIRONMENT", "development"))
        self.genai_key = os.getenv("GENAI_KEY")
        self.port = int(os.getenv("PORT", 10000))
        self.debug = self.env == Environment.DEVELOPMENT
        
    @property
    def cors_origins(self):
        if self.env == Environment.PRODUCTION:
            return ["https://yourdomain.com"]
        return ["*"]
```

## Best Practices

### 1. Code Organization

```python
# Separate concerns into different modules
# models.py
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    conversationId: str | None = None

# services.py
class EmbeddingService:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)
    
    def generate_embeddings(self, texts: list[str]) -> dict:
        # Implementation
        pass

# routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/api")

@router.post("/query")
async def query_endpoint(request: QueryRequest):
    # Implementation
    pass
```

### 2. Error Handling

```python
# Custom exception classes
class EduChatException(Exception):
    """Base exception for EduChat application."""
    pass

class EmbeddingError(EduChatException):
    """Raised when embedding generation fails."""
    pass

class DataValidationError(EduChatException):
    """Raised when data validation fails."""
    pass

# Error handlers
@app.exception_handler(EduChatException)
async def educhat_exception_handler(request: Request, exc: EduChatException):
    return JSONResponse(
        status_code=500,
        content={"detail": f"EduChat error: {str(exc)}"}
    )
```

### 3. Logging

```python
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use logging in functions
def retrieve_relevant_info(query: str) -> tuple[list, list]:
    logger.info(f"Processing query: {query}")
    
    try:
        # Implementation
        logger.info(f"Found {len(courses)} relevant courses")
        return courses, instructors
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise
```

### 4. Performance Optimization

```python
# Cache embeddings for better performance
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_query_embedding(query: str) -> np.ndarray:
    """Cache frequently used query embeddings."""
    return sentence_model.encode(query)

# Async operations for better concurrency
import asyncio

async def process_multiple_queries(queries: list[str]) -> list[dict]:
    """Process multiple queries concurrently."""
    tasks = [process_single_query(query) for query in queries]
    return await asyncio.gather(*tasks)
```

### 5. Security Best Practices

```python
# Input validation and sanitization
from pydantic import validator

class QueryRequest(BaseModel):
    query: str
    conversationId: str | None = None
    
    @validator('query')
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError('Query cannot be empty')
        if len(v) > 1000:
            raise ValueError('Query too long')
        return v.strip()

# Rate limiting (if using slowapi)
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/query")
@limiter.limit("30/minute")
async def query(request: Request, data: QueryRequest):
    # Implementation
    pass
```

### 6. Monitoring and Health Checks

```python
# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Basic metrics for monitoring."""
    return {
        "total_requests": request_counter,
        "active_conversations": len(active_conversations),
        "model_loaded": sentence_model is not None
    }
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Model Loading Issues

**Problem**: Sentence transformer model fails to load
```
AttributeError: module 'sentence_transformers' has no attribute 'SentenceTransformer'
```

**Solution**:
```bash
# Reinstall sentence-transformers
pip uninstall sentence-transformers
pip install sentence-transformers==3.2.1

# Clear model cache if needed
rm -rf ~/.cache/huggingface/
```

#### 2. API Key Issues

**Problem**: Google Gemini API calls fail
```
google.api_core.exceptions.Unauthenticated: 401 Invalid API key
```

**Solution**:
```bash
# Verify API key is set
echo $GENAI_KEY

# Test API key with curl
curl -H "Authorization: Bearer $GENAI_KEY" \
     "https://generativelanguage.googleapis.com/v1/models"
```

#### 3. Memory Issues

**Problem**: Application runs out of memory
```
MemoryError: Unable to allocate array
```

**Solutions**:
```python
# Use CPU device for sentence transformer
sentence_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

# Reduce batch size for embeddings
def generate_embeddings_batch(texts: list[str], batch_size: int = 32):
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        batch_embeddings = sentence_model.encode(batch)
        embeddings.extend(batch_embeddings)
    return embeddings
```

#### 4. Port Conflicts

**Problem**: Port already in use
```
OSError: [Errno 48] Address already in use
```

**Solution**:
```bash
# Find and kill process using port
lsof -ti:10000 | xargs kill -9

# Or use different port
export PORT=8080
python app.py
```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug prints
@app.post("/api/query")
async def query(request: Request, data: QueryRequest):
    print(f"DEBUG: Received query: {data.query}")
    print(f"DEBUG: Conversation ID: {data.conversationId}")
    
    # Continue with implementation
```

### Performance Profiling

```python
# Profile critical functions
import cProfile
import pstats

def profile_similarity_search():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run similarity search
    result = retrieve_relevant_info("Python programming")
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats()
```

## Contributing Guidelines

### Getting Started

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes and add tests**
4. **Ensure all tests pass**: `pytest`
5. **Submit pull request**

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and pass
- [ ] Documentation is updated
- [ ] No hardcoded secrets or API keys
- [ ] Error handling is implemented
- [ ] Performance impact is considered

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

### Release Process

1. **Update version numbers**
2. **Update CHANGELOG.md**
3. **Create release branch**: `git checkout -b release/v1.1.0`
4. **Run full test suite**
5. **Create pull request to main**
6. **Tag release**: `git tag v1.1.0`
7. **Deploy to production**

---

## Additional Resources

### Useful Commands

```bash
# Development server with auto-reload
uvicorn app:app --reload --host 0.0.0.0 --port 10000

# Format code
black app.py templates/ tests/
isort app.py

# Type checking
mypy app.py

# Security scanning
bandit -r app.py

# Dependency vulnerability checking
safety check
```

### Helpful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [Google Generative AI](https://ai.google.dev/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Tailwind CSS](https://tailwindcss.com/)

### Community

- **Issues**: Report bugs and request features via GitHub issues
- **Discussions**: Join discussions in GitHub discussions
- **Discord**: Join our Discord server for real-time help
- **Stack Overflow**: Tag questions with `educhat`

---

*Happy coding! 🚀*