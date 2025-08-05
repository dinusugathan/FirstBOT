# EduChat - Course Enquiry Assistant API Documentation

## Overview

EduChat is a FastAPI-based Course Enquiry Assistant that provides AI-powered chatbot functionality for course inquiries and translation services. The application uses Google's Gemini AI model for natural language processing and sentence transformers for semantic similarity matching.

## Technology Stack

- **Backend Framework**: FastAPI 0.115.2
- **AI/ML Libraries**: 
  - Google Generative AI (Gemini 1.5 Flash)
  - Sentence Transformers (all-MiniLM-L6-v2)
  - Scikit-learn for similarity calculations
- **Frontend**: HTML/CSS/JavaScript with Tailwind CSS
- **Template Engine**: Jinja2
- **Session Management**: Starlette SessionMiddleware

## Base URL

```
http://localhost:10000
```

## Authentication

Currently, the application does not require authentication. All endpoints are publicly accessible.

---

## API Endpoints

### 1. Home Page

**Endpoint**: `GET /`

**Description**: Serves the main chat interface HTML page.

**Response**: HTML page with the chat interface

**Example Request**:
```bash
curl -X GET "http://localhost:10000/"
```

**Response**: Returns the HTML chat interface

---

### 2. Course Query API

**Endpoint**: `POST /api/query`

**Description**: Processes natural language queries about courses and instructors, providing AI-generated responses based on semantic similarity matching.

**Request Body**:
```json
{
  "query": "string",
  "conversationId": "string (optional)"
}
```

**Parameters**:
- `query` (required): The user's question about courses or instructors
- `conversationId` (optional): UUID for maintaining conversation context. If not provided, a new conversation ID is generated.

**Response**:
```json
{
  "response": "string"
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:10000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Tell me about Python courses",
    "conversationId": "123e4567-e89b-12d3-a456-426614174000"
  }'
```

**Example Response**:
```json
{
  "response": "Based on our course catalog, I found the 'Introduction to Python' course which covers Python programming basics. This 4-week course is taught by John Doe, a Python expert with 10 years of experience. The course is perfect for beginners looking to learn Python fundamentals."
}
```

**Error Responses**:
- `500 Internal Server Error`: When an unexpected error occurs
```json
{
  "detail": "An error occurred: [error message]"
}
```

---

### 3. Translation API

**Endpoint**: `POST /api/translate`

**Description**: Translates English text to specified target languages using Google's Gemini AI.

**Request Body**:
```json
{
  "text": "string",
  "target_lang": "string (default: 'es')",
  "conversationId": "string (optional)"
}
```

**Parameters**:
- `text` (required): The English text to translate
- `target_lang` (optional): Target language code (default: "es" for Spanish)
- `conversationId` (optional): UUID for maintaining translation history

**Response**:
```json
{
  "translation": "string"
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:10000/api/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, how are you?",
    "target_lang": "fr",
    "conversationId": "123e4567-e89b-12d3-a456-426614174000"
  }'
```

**Example Response**:
```json
{
  "translation": "Bonjour, comment allez-vous ?"
}
```

**Error Responses**:
- `500 Internal Server Error`: When translation fails
```json
{
  "detail": "An error occurred: [error message]"
}
```

---

## Data Models

### QueryRequest

Pydantic model for course query requests.

```python
class QueryRequest(BaseModel):
    query: str
    conversationId: str | None = None
```

**Fields**:
- `query`: The user's question (required)
- `conversationId`: Optional conversation identifier

### TranslateRequest

Pydantic model for translation requests.

```python
class TranslateRequest(BaseModel):
    text: str
    target_lang: str = "es"
    conversationId: str | None = None
```

**Fields**:
- `text`: Text to translate (required)
- `target_lang`: Target language code (default: "es")
- `conversationId`: Optional conversation identifier

---

## Core Functions

### retrieve_relevant_info(query)

**Purpose**: Retrieves relevant courses and instructors based on semantic similarity to the user's query.

**Parameters**:
- `query` (str): User's search query

**Returns**: 
- `tuple`: (matched_courses, matched_instructors)
  - `matched_courses`: List of top 3 most relevant course objects
  - `matched_instructors`: List of top 3 most relevant instructor objects

**Algorithm**:
1. Encodes the query using sentence transformer
2. Computes cosine similarity with pre-computed course and instructor embeddings
3. Returns top 3 matches for each category

**Example**:
```python
courses, instructors = retrieve_relevant_info("Python programming")
# Returns courses and instructors most relevant to Python
```

### format_context(courses, instructors)

**Purpose**: Formats retrieved courses and instructors into a readable context string for the AI model.

**Parameters**:
- `courses` (list): List of course objects
- `instructors` (list): List of instructor objects

**Returns**:
- `str`: Formatted context string

**Example Output**:
```
Relevant Courses:
- Introduction to Python: Learn Python programming basics (Instructor: John Doe, Duration: 4 weeks)

Relevant Instructors:
- John Doe: Python expert with 10 years experience
```

### build_prompt_with_context(question, context, conversation_history)

**Purpose**: Constructs the complete prompt for the AI model including context and conversation history.

**Parameters**:
- `question` (str): Current user question
- `context` (str): Formatted context from relevant courses/instructors
- `conversation_history` (list): List of previous messages in the conversation

**Returns**:
- `str`: Complete prompt for the AI model

**Usage**: Internal function used to prepare prompts for Gemini AI model.

---

## Data Structures

### Course Object

```json
{
  "name": "string",
  "description": "string", 
  "instructor": "string",
  "duration": "string"
}
```

**Example**:
```json
{
  "name": "Introduction to Python",
  "description": "Learn Python programming basics",
  "instructor": "John Doe", 
  "duration": "4 weeks"
}
```

### Instructor Object

```json
{
  "name": "string",
  "bio": "string",
  "courses": ["string"]
}
```

**Example**:
```json
{
  "name": "John Doe",
  "bio": "Python expert with 10 years experience",
  "courses": ["Introduction to Python"]
}
```

---

## Session Management

The application uses server-side sessions to maintain:

1. **Conversation History**: Stored per conversation ID
   - System message initialization
   - User questions and AI responses
   - Maintains context across multiple queries

2. **Translation History**: Stored per conversation ID
   - Original text, translation, and target language
   - Allows users to review past translations

**Session Structure**:
```python
request.session = {
    'conversations': {
        'conversation_id': [
            {"role": "system", "content": "You are a helpful course enquiry assistant."},
            {"role": "user", "content": "user question"},
            {"role": "assistant", "content": "AI response"}
        ]
    },
    'translations': {
        'conversation_id': [
            {
                "original": "original text",
                "translation": "translated text", 
                "language": "target_lang"
            }
        ]
    }
}
```

---

## Frontend Components

### Chat Interface

The main chat interface (`/templates/index.html`) provides:

- **Real-time Chat**: WebSocket-style interaction with the backend
- **Responsive Design**: Built with Tailwind CSS for mobile compatibility
- **Translation Feature**: Integrated translation functionality
- **Message History**: Visual conversation history with user and bot messages
- **Typing Indicators**: Visual feedback during AI processing

**Key Features**:
- Modern gradient background design
- Floating animations for visual appeal
- Message bubbles with distinct styling for user vs. bot
- Real-time response display
- Error handling with user feedback

---

## Environment Variables

### Required Configuration

```bash
PORT=10000  # Server port (default: 10000)
```

### API Keys

**Google Gemini API Key**: Currently hardcoded in `app.py` (line 33)
```python
GENAI_KEY = "AIzaSyApq6H8qvGtVFol9ROILTa8CehZcHJ5GnE"
```

⚠️ **Security Note**: The API key should be moved to environment variables for production use.

---

## Installation and Setup

### Prerequisites

- Python 3.8+
- pip package manager

### Installation Steps

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set Environment Variables**:
```bash
export GENAI_KEY="your-google-gemini-api-key"
export PORT=10000
```

3. **Run the Application**:
```bash
python app.py
```

Or using uvicorn directly:
```bash
uvicorn app:app --host 0.0.0.0 --port 10000
```

### Development Setup

For development, you can run with auto-reload:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 10000
```

---

## Usage Examples

### Basic Course Query

```javascript
// JavaScript fetch example
const response = await fetch('/api/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'What machine learning courses do you offer?',
    conversationId: 'unique-conversation-id'
  })
});

const data = await response.json();
console.log(data.response);
```

### Translation Request

```javascript
// JavaScript fetch example
const response = await fetch('/api/translate', {
  method: 'POST', 
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: 'This course covers advanced machine learning techniques',
    target_lang: 'es',
    conversationId: 'unique-conversation-id'
  })
});

const data = await response.json();
console.log(data.translation);
```

### Python Client Example

```python
import requests
import json

# Course query
def query_courses(question, conversation_id=None):
    url = "http://localhost:10000/api/query"
    payload = {
        "query": question,
        "conversationId": conversation_id
    }
    response = requests.post(url, json=payload)
    return response.json()

# Translation
def translate_text(text, target_lang="es", conversation_id=None):
    url = "http://localhost:10000/api/translate" 
    payload = {
        "text": text,
        "target_lang": target_lang,
        "conversationId": conversation_id
    }
    response = requests.post(url, json=payload)
    return response.json()

# Usage
result = query_courses("Tell me about Python courses")
print(result['response'])

translation = translate_text("Hello world", "fr")
print(translation['translation'])
```

---

## Error Handling

### Common Error Scenarios

1. **Empty Query**: Returns polite message asking for valid question
2. **AI Model Errors**: Graceful fallback with error message
3. **Translation Failures**: Returns error message with failure details
4. **Server Errors**: Returns HTTP 500 with error details

### Error Response Format

```json
{
  "detail": "An error occurred: [specific error message]"
}
```

---

## Performance Considerations

### Embeddings

- Course and instructor embeddings are pre-computed at startup
- Uses efficient sentence transformer model (all-MiniLM-L6-v2)
- CPU-optimized for cost-effective deployment

### Similarity Search

- Cosine similarity computation for semantic matching
- Top-3 results to balance relevance and response time
- Efficient numpy operations for vector computations

### Session Management

- Server-side sessions for security and reliability
- Conversation history maintained for context
- Translation history for user convenience

---

## Security Considerations

### Current Security Features

- CORS middleware enabled for cross-origin requests
- Session middleware with secret key for session integrity
- Input validation using Pydantic models

### Security Recommendations

1. **Environment Variables**: Move API keys to environment variables
2. **Rate Limiting**: Implement rate limiting to prevent abuse
3. **Input Sanitization**: Add additional input validation and sanitization
4. **HTTPS**: Use HTTPS in production environments
5. **Session Security**: Use secure session configuration for production

---

## Deployment

### Production Deployment

The application is configured for deployment on platforms like Render, Heroku, or similar:

```python
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### Docker Deployment

Example Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 10000

CMD ["python", "app.py"]
```

---

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed via `pip install -r requirements.txt`
2. **API Key Issues**: Verify Google Gemini API key is valid and properly configured
3. **Port Conflicts**: Change PORT environment variable if default port 10000 is in use
4. **Model Loading**: First run may take time to download sentence transformer model

### Debug Mode

For debugging, run with verbose logging:
```bash
uvicorn app:app --reload --log-level debug
```

---

## Contributing

### Code Structure

- `app.py`: Main application file with all routes and core logic
- `templates/`: HTML templates for frontend
- `data/`: JSON data files for courses and instructors
- `requirements.txt`: Python dependencies

### Adding New Features

1. Follow FastAPI conventions for new endpoints
2. Use Pydantic models for request/response validation
3. Maintain session management patterns for stateful features
4. Update this documentation for any new public APIs

---

## License

This project is provided as-is for educational and demonstration purposes.