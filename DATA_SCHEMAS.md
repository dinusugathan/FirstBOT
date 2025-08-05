# Data Schemas and Models Documentation

## Overview

This document describes all data structures, schemas, and models used in the EduChat Course Enquiry Assistant application. It includes both static data files and dynamic runtime models.

## Static Data Files

### Course Data Schema (`data/courses.json`)

**File Purpose**: Contains the catalog of available courses that the AI can reference for queries.

**Schema Definition**:
```json
[
  {
    "name": "string",           // Required: Course title
    "description": "string",    // Required: Course description
    "instructor": "string",     // Required: Name of course instructor
    "duration": "string"        // Required: Course duration (e.g., "4 weeks")
  }
]
```

**Example Data**:
```json
[
  {
    "name": "Introduction to Python",
    "description": "Learn Python programming basics",
    "instructor": "John Doe",
    "duration": "4 weeks"
  },
  {
    "name": "Advanced Machine Learning",
    "description": "Deep dive into ML algorithms",
    "instructor": "Jane Smith",
    "duration": "8 weeks"
  }
]
```

**Validation Rules**:
- `name`: Non-empty string, unique across all courses
- `description`: Non-empty string, used for semantic similarity matching
- `instructor`: Must match an instructor name from `instructors.json`
- `duration`: Free-form string describing course length

**Usage in Application**:
- Loaded at startup into global `courses` variable
- Used for semantic similarity matching via sentence transformers
- Pre-processed into embeddings for efficient similarity search

---

### Instructor Data Schema (`data/instructors.json`)

**File Purpose**: Contains information about course instructors for enhanced query responses.

**Schema Definition**:
```json
[
  {
    "name": "string",          // Required: Instructor full name
    "bio": "string",           // Required: Instructor biography/description
    "courses": ["string"]      // Required: Array of course names they teach
  }
]
```

**Example Data**:
```json
[
  {
    "name": "John Doe",
    "bio": "Python expert with 10 years experience",
    "courses": ["Introduction to Python"]
  },
  {
    "name": "Jane Smith",
    "bio": "ML researcher and educator",
    "courses": ["Advanced Machine Learning"]
  }
]
```

**Validation Rules**:
- `name`: Non-empty string, unique across all instructors
- `bio`: Non-empty string, used for semantic similarity matching
- `courses`: Array of strings that must match course names from `courses.json`

**Usage in Application**:
- Loaded at startup into global `instructors` variable
- Used for semantic similarity matching alongside courses
- Cross-referenced with course data for comprehensive responses

---

## API Request/Response Models

### QueryRequest (Pydantic Model)

**Purpose**: Validates incoming course query requests.

**Schema Definition**:
```python
class QueryRequest(BaseModel):
    query: str
    conversationId: str | None = None
```

**Field Specifications**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | `str` | Yes | The user's natural language question about courses/instructors |
| `conversationId` | `str \| None` | No | UUID for maintaining conversation context (generated if not provided) |

**Example Request Body**:
```json
{
  "query": "What Python courses do you offer?",
  "conversationId": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Validation Rules**:
- `query`: Must be non-empty string after stripping whitespace
- `conversationId`: If provided, should be valid UUID format (not enforced)

---

### TranslateRequest (Pydantic Model)

**Purpose**: Validates incoming translation requests.

**Schema Definition**:
```python
class TranslateRequest(BaseModel):
    text: str
    target_lang: str = "es"
    conversationId: str | None = None
```

**Field Specifications**:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `text` | `str` | Yes | - | English text to translate |
| `target_lang` | `str` | No | `"es"` | Target language code |
| `conversationId` | `str \| None` | No | `None` | UUID for maintaining translation history |

**Example Request Body**:
```json
{
  "text": "This is a comprehensive course on machine learning",
  "target_lang": "fr",
  "conversationId": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Supported Language Codes**:
- `es`: Spanish
- `fr`: French
- `de`: German
- `it`: Italian
- `pt`: Portuguese
- `ru`: Russian
- `ja`: Japanese
- `ko`: Korean
- `zh`: Chinese

---

## Response Models

### Query Response Schema

**Purpose**: Standard response format for course queries.

**Schema Definition**:
```json
{
  "response": "string"
}
```

**Example Response**:
```json
{
  "response": "I found several Python courses for you. The 'Introduction to Python' is a 4-week course taught by John Doe, a Python expert with 10 years of experience. This course covers Python programming basics and is perfect for beginners."
}
```

---

### Translation Response Schema

**Purpose**: Standard response format for translation requests.

**Schema Definition**:
```json
{
  "translation": "string"
}
```

**Example Response**:
```json
{
  "translation": "Il s'agit d'un cours complet sur l'apprentissage automatique"
}
```

---

## Runtime Data Structures

### Session Data Schema

**Purpose**: Maintains user state across requests using server-side sessions.

**Session Structure**:
```python
request.session = {
    "conversations": {
        "conversation_id": [
            {
                "role": "system" | "user" | "assistant",
                "content": "string"
            }
        ]
    },
    "translations": {
        "conversation_id": [
            {
                "original": "string",
                "translation": "string",
                "language": "string"
            }
        ]
    }
}
```

#### Conversations Schema

**Purpose**: Stores conversation history per conversation ID.

**Structure**:
```python
{
    "conversation_id": [
        {"role": "system", "content": "You are a helpful course enquiry assistant."},
        {"role": "user", "content": "Tell me about Python courses"},
        {"role": "assistant", "content": "Here are the Python courses available..."}
    ]
}
```

**Message Object Schema**:
| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `role` | `str` | `"system"`, `"user"`, `"assistant"` | Message sender type |
| `content` | `str` | Any string | Message content |

#### Translations Schema

**Purpose**: Stores translation history per conversation ID.

**Structure**:
```python
{
    "conversation_id": [
        {
            "original": "Hello world",
            "translation": "Hola mundo",
            "language": "es"
        }
    ]
}
```

**Translation Object Schema**:
| Field | Type | Description |
|-------|------|-------------|
| `original` | `str` | Original English text |
| `translation` | `str` | Translated text |
| `language` | `str` | Target language code |

---

## Internal Data Models

### Course Embedding Model

**Purpose**: Pre-computed vector embeddings for semantic similarity.

**Structure**:
```python
course_embeddings = {
    "course_name": numpy.ndarray  # 384-dimensional vector from sentence transformer
}
```

**Example**:
```python
{
    "Introduction to Python": array([0.1234, -0.5678, 0.9012, ...]),  # 384 dimensions
    "Advanced Machine Learning": array([0.2345, -0.6789, 0.0123, ...])  # 384 dimensions
}
```

### Instructor Embedding Model

**Purpose**: Pre-computed vector embeddings for instructor information.

**Structure**:
```python
instructor_embeddings = {
    "instructor_name": numpy.ndarray  # 384-dimensional vector from sentence transformer
}
```

**Example**:
```python
{
    "John Doe": array([0.3456, -0.7890, 0.1234, ...]),    # 384 dimensions
    "Jane Smith": array([0.4567, -0.8901, 0.2345, ...])   # 384 dimensions
}
```

---

## Error Response Schemas

### HTTP Error Response

**Purpose**: Standard error response format for API endpoints.

**Schema Definition**:
```json
{
  "detail": "string"
}
```

**Example Error Responses**:

**500 Internal Server Error**:
```json
{
  "detail": "An error occurred: Google AI API rate limit exceeded"
}
```

**Validation Error (422)**:
```json
{
  "detail": [
    {
      "loc": ["body", "query"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Data Processing Pipeline

### Embedding Generation Process

**Input**: Course/Instructor data
**Output**: Vector embeddings for similarity search

**Process Flow**:
1. **Data Loading**: Read JSON files at application startup
2. **Text Concatenation**: Combine relevant fields for embedding
   - Courses: `name + " " + description`
   - Instructors: `name + " " + bio`
3. **Embedding Generation**: Use sentence transformer model
4. **Storage**: Store in dictionary for fast lookup

**Code Example**:
```python
# Course embeddings
course_embeddings = {
    course['name']: sentence_model.encode(
        course['name'] + " " + course['description']
    ) for course in courses
}

# Instructor embeddings
instructor_embeddings = {
    instructor['name']: sentence_model.encode(
        instructor['name'] + " " + instructor['bio']
    ) for instructor in instructors
}
```

### Similarity Search Algorithm

**Input**: User query string
**Output**: Top 3 most relevant courses and instructors

**Process Flow**:
1. **Query Encoding**: Convert user query to vector embedding
2. **Similarity Computation**: Calculate cosine similarity with all stored embeddings
3. **Ranking**: Sort by similarity score (descending)
4. **Selection**: Return top 3 matches for each category

**Mathematical Formula**:
```
similarity(A, B) = (A · B) / (||A|| × ||B||)
```

Where:
- A = Query embedding vector
- B = Course/Instructor embedding vector
- · = Dot product
- ||·|| = Vector magnitude

---

## Data Validation and Constraints

### JSON Schema Validation

**Courses JSON Validation**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["name", "description", "instructor", "duration"],
    "properties": {
      "name": {"type": "string", "minLength": 1},
      "description": {"type": "string", "minLength": 1},
      "instructor": {"type": "string", "minLength": 1},
      "duration": {"type": "string", "minLength": 1}
    },
    "additionalProperties": false
  }
}
```

**Instructors JSON Validation**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["name", "bio", "courses"],
    "properties": {
      "name": {"type": "string", "minLength": 1},
      "bio": {"type": "string", "minLength": 1},
      "courses": {
        "type": "array",
        "items": {"type": "string", "minLength": 1},
        "minItems": 1
      }
    },
    "additionalProperties": false
  }
}
```

### Business Logic Constraints

1. **Data Consistency**:
   - Instructor names in courses must exist in instructors.json
   - Course names in instructor records must exist in courses.json

2. **Uniqueness Constraints**:
   - Course names must be unique
   - Instructor names must be unique

3. **Content Requirements**:
   - All text fields must be non-empty after trimming
   - Course descriptions should be meaningful for semantic search
   - Instructor bios should provide relevant context

---

## Data Migration and Updates

### Adding New Courses

**Steps**:
1. Update `data/courses.json` with new course object
2. Ensure instructor exists in `data/instructors.json`
3. Restart application to regenerate embeddings
4. Test semantic search functionality

**Example Addition**:
```json
{
  "name": "Web Development Fundamentals",
  "description": "Learn HTML, CSS, and JavaScript basics for web development",
  "instructor": "Alice Johnson",
  "duration": "6 weeks"
}
```

### Adding New Instructors

**Steps**:
1. Update `data/instructors.json` with new instructor object
2. Ensure course references are valid
3. Restart application to regenerate embeddings
4. Test query responses mention new instructor

**Example Addition**:
```json
{
  "name": "Alice Johnson",
  "bio": "Full-stack developer and web technologies instructor with 8 years experience",
  "courses": ["Web Development Fundamentals"]
}
```

### Data Backup and Recovery

**Backup Strategy**:
1. Regular backups of JSON files
2. Version control for data changes
3. Backup embedding computations for large datasets

**Recovery Process**:
1. Restore JSON files from backup
2. Restart application to regenerate embeddings
3. Validate data consistency
4. Test application functionality

---

## Performance Considerations

### Memory Usage

**Embedding Storage**:
- Each embedding: 384 dimensions × 4 bytes (float32) = 1.5 KB
- 100 courses: ~150 KB
- 100 instructors: ~150 KB
- Total: Minimal memory footprint for typical datasets

### Computational Complexity

**Similarity Search**:
- Time Complexity: O(n) where n = number of courses/instructors
- Space Complexity: O(1) for query processing
- Scalability: Linear scaling with dataset size

**Optimization Strategies**:
1. **Pre-computation**: Embeddings generated at startup, not per query
2. **Efficient Libraries**: NumPy for vectorized operations
3. **Caching**: Embeddings stored in memory for fast access

---

## Security Considerations

### Data Validation

1. **Input Sanitization**: Pydantic models validate all API inputs
2. **JSON Validation**: Static data files should be validated on updates
3. **Type Safety**: Strong typing prevents data corruption

### Sensitive Data

1. **No PII**: Current schema doesn't include personally identifiable information
2. **Public Data**: Course and instructor information assumed to be public
3. **Session Security**: Conversation history stored server-side only

---

## Testing Data Models

### Unit Test Examples

```python
# Test course data validation
def test_course_schema():
    valid_course = {
        "name": "Test Course",
        "description": "Test description",
        "instructor": "Test Instructor",
        "duration": "4 weeks"
    }
    # Validate course structure
    assert validate_course(valid_course) == True

# Test instructor data validation
def test_instructor_schema():
    valid_instructor = {
        "name": "Test Instructor",
        "bio": "Test biography",
        "courses": ["Test Course"]
    }
    # Validate instructor structure
    assert validate_instructor(valid_instructor) == True

# Test embedding generation
def test_embedding_generation():
    test_text = "Python programming course"
    embedding = sentence_model.encode(test_text)
    assert embedding.shape == (384,)
    assert isinstance(embedding, np.ndarray)
```

### Integration Test Examples

```python
# Test data consistency
def test_data_consistency():
    # Load data files
    courses = load_courses()
    instructors = load_instructors()
    
    # Check instructor references
    for course in courses:
        instructor_exists = any(
            inst['name'] == course['instructor'] 
            for inst in instructors
        )
        assert instructor_exists, f"Instructor {course['instructor']} not found"
    
    # Check course references
    for instructor in instructors:
        for course_name in instructor['courses']:
            course_exists = any(
                course['name'] == course_name 
                for course in courses
            )
            assert course_exists, f"Course {course_name} not found"
```

---

## Future Schema Enhancements

### Potential Additions

1. **Course Categories**: Add categorization for better organization
2. **Prerequisites**: Course dependency tracking
3. **Pricing**: Course cost information
4. **Ratings**: Student feedback and ratings
5. **Schedules**: Course start dates and availability
6. **Multimedia**: Support for images, videos, and documents

### Enhanced Instructor Model

```json
{
  "name": "string",
  "bio": "string",
  "courses": ["string"],
  "expertise": ["string"],      // New: Areas of expertise
  "education": "string",        // New: Educational background
  "certifications": ["string"], // New: Professional certifications
  "contact": {                  // New: Contact information
    "email": "string",
    "linkedin": "string"
  }
}
```

### Advanced Course Model

```json
{
  "name": "string",
  "description": "string",
  "instructor": "string",
  "duration": "string",
  "category": "string",         // New: Course category
  "level": "string",           // New: Beginner/Intermediate/Advanced
  "prerequisites": ["string"], // New: Required prior courses
  "learning_outcomes": ["string"], // New: What students will learn
  "price": "number",           // New: Course cost
  "schedule": {                // New: Course timing
    "start_date": "string",
    "end_date": "string",
    "time_slots": ["string"]
  }
}
```