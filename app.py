from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import google.generativeai as genai
import json
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import BaseModel
import os
import uuid

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="ff6e4cfb09b5c8a19cd29223040a82b779737e41674b789684efa6300b2d48a5")

# Configure templates
templates = Jinja2Templates(directory="templates")

# Configure Gemini
GENAI_KEY = "AIzaSyApq6H8qvGtVFol9ROILTa8CehZcHJ5GnE"  # Replace with your valid Google Gemini API key
genai.configure(api_key=GENAI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Load and initialize the sentence transformer model
sentence_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

# Load course and instructor data from JSON files
with open("data/courses.json", "r") as f:
    courses = json.load(f)

with open("data/instructors.json", "r") as f:
    instructors = json.load(f)

# Pre-compute embeddings for courses and instructors
course_embeddings = {course['name']: sentence_model.encode(course['name'] + " " + course['description']) for course in courses}
instructor_embeddings = {instructor['name']: sentence_model.encode(instructor['name'] + " " + instructor['bio']) for instructor in instructors}

def retrieve_relevant_info(query):
    """Retrieve relevant courses and instructors based on the query."""
    query_embedding = sentence_model.encode(query)
    
    # Find relevant courses
    course_scores = []
    for name, embedding in course_embeddings.items():
        similarity = cosine_similarity([query_embedding], [embedding])[0][0]
        course_scores.append((similarity, name))
    
    # Find relevant instructors
    instructor_scores = []
    for name, embedding in instructor_embeddings.items():
        similarity = cosine_similarity([query_embedding], [embedding])[0][0]
        instructor_scores.append((similarity, name))
    
    # Sort by similarity and get top 3
    relevant_courses = [name for score, name in sorted(course_scores, reverse=True)[:3]]
    relevant_instructors = [name for score, name in sorted(instructor_scores, reverse=True)[:3]]
    
    # Get full course and instructor details
    matched_courses = [course for course in courses if course['name'] in relevant_courses]
    matched_instructors = [instructor for instructor in instructors if instructor['name'] in relevant_instructors]
    
    return matched_courses, matched_instructors

def format_context(courses, instructors):
    """Format the context for the prompt."""
    context = ""
    
    if courses:
        context += "Relevant Courses:\n"
        for course in courses:
            context += f"- {course['name']}: {course['description']} (Instructor: {course['instructor']}, Duration: {course['duration']})\n"
    
    if instructors:
        context += "\nRelevant Instructors:\n"
        for instructor in instructors:
            context += f"- {instructor['name']}: {instructor['bio']}\n"
    
    return context.strip()

def build_prompt_with_context(question, context, conversation_history):
    """Build the prompt with context and conversation history."""
    prompt = f"""
    Context information:
    {context}

    Conversation history:
    """
    
    for msg in conversation_history[1:]:  # Skip system message
        prompt += f"{msg['role']}: {msg['content']}\n"
    
    prompt += f"""
    Current question: {question}
    
    Please provide a helpful response based on the context and conversation history.
    """
    
    return prompt

class QueryRequest(BaseModel):
    query: str
    conversationId: str | None = None

class TranslateRequest(BaseModel):
    text: str
    target_lang: str = "es"
    conversationId: str | None = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/query")
async def query(request: Request, data: QueryRequest):
    try:
        question = data.query.strip()
        conversation_id = data.conversationId or str(uuid.uuid4())
        
        if not question:
            return {"response": "Please enter a valid question."}

        # Initialize or retrieve conversation history
        if 'conversations' not in request.session:
            request.session['conversations'] = {}
            
        if conversation_id not in request.session['conversations']:
            request.session['conversations'][conversation_id] = [
                {"role": "system", "content": "You are a helpful course enquiry assistant."}
            ]

        # Add user question to conversation history
        request.session['conversations'][conversation_id].append({"role": "user", "content": question})
        
        # Retrieve relevant information
        courses, instructors = retrieve_relevant_info(question)
        context = format_context(courses, instructors)

        # Construct prompt
        prompt = build_prompt_with_context(question, context, request.session['conversations'][conversation_id])

        try:
            gemini_response = model.generate_content(prompt)
            response = gemini_response.text.strip()
            
            # Add assistant response to conversation history
            request.session['conversations'][conversation_id].append({"role": "assistant", "content": response})
            
        except Exception as e:
            response = f"I couldn't process that request. Please try again. (Error: {str(e)})"

        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/api/translate")
async def translate(request: Request, data: TranslateRequest):
    try:
        text = data.text.strip()
        target_lang = data.target_lang
        conversation_id = data.conversationId or str(uuid.uuid4())
        
        if not text:
            return {"translation": "No text to translate"}
        
        # Create a translation prompt
        prompt = f"""
        Translate the following English text to {target_lang}. 
        Keep the meaning accurate but make the translation sound natural in the target language.
        
        Text to translate: {text}
        """
        
        try:
            gemini_response = model.generate_content(prompt)
            translation = gemini_response.text.strip()
            
            # Store translation in session
            if 'translations' not in request.session:
                request.session['translations'] = {}
                
            if conversation_id not in request.session['translations']:
                request.session['translations'][conversation_id] = []
                
            request.session['translations'][conversation_id].append({
                "original": text,
                "translation": translation,
                "language": target_lang
            })
            
            return {"translation": translation}
        
        except Exception as e:
            return {"translation": f"Translation failed: {str(e)}"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)