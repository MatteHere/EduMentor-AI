# EduMentor AI v1.0 Blueprint

## Vision

EduMentor AI is an AI-powered study platform for Indian university students.

It helps students upload notes, understand difficult topics, revise faster, generate exam practice, prepare for viva, and later access university-specific resources.

## Core Modules

### 1. Dashboard
- Study overview
- Recent uploads
- Suggested next actions
- Progress summary

### 2. Workspace
- Semester-wise organization
- Subject-wise organization
- Unit-wise notes
- Uploaded documents
- Saved AI outputs

### 3. Learn Hub
- Explain notes
- Generate summaries
- Create MCQs
- Create flashcards
- Generate viva questions
- Explain with examples
- Placement-oriented questions

### 4. Study Planner
- Daily study plan
- Weekly revision plan
- Exam countdown
- Topic priority

### 5. Progress
- Completed topics
- Weak topics
- Quiz scores
- Revision streak

### 6. University Hub
- SPPU syllabus
- Previous year papers
- Lab manuals
- Recommended books
- YouTube resources
- Trusted websites

### 7. Career Hub
- Mini project ideas
- Interview questions
- Resume skills
- GitHub project suggestions
- Certification roadmap

## Technical Architecture

### Entry Point
- `run.py`

### UI Layer
- `ui/dashboard.py`
- `ui/upload.py`
- `ui/learn.py`
- `ui/settings.py`

### Service Layer
- `services/document_service.py`
- `services/ai_service.py`
- `services/groq_service.py`
- `services/gemini_service.py`
- `services/provider_manager.py`
- `services/prompt_service.py`

### Data Layer
- `data/uploads/`
- Future: SQLite/PostgreSQL
- Future: Vector database for RAG

## AI Architecture

### Current
- Groq as primary provider
- Gemini as fallback
- Provider selection in Settings

### Future
- OpenAI optional
- Provider auto-routing
- AI response caching
- RAG with university knowledge base
- Multi-document memory

## Roadmap

### v0.5 Completed
- Premium UI
- Upload system
- PDF/DOCX/PPTX/TXT processing
- Text cleaning
- Groq/Gemini AI engine
- Refactored services and UI

### v1.0 Next
- Workspace system
- Learn Hub improvement
- Save generated outputs
- Basic study history

### v1.5
- Study Planner
- Progress dashboard
- Quiz mode

### v2.0
- University Knowledge Base
- RAG
- AI memory
- Career Hub

## Product Goal

EduMentor AI should become a complete AI study operating system for Indian university students, starting with SPPU and AI & DS students, then expanding to other streams and universities.