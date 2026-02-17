from chat_bot import ask_question
from fastapi import FastAPI
from pydantic import BaseModel
from model import generate_summary, get_transcript
from urllib.parse import urlparse, parse_qs
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Request body model
class YouTubeRequest(BaseModel):
    url: str
    
class SummaryRequest(BaseModel):
    transcript: str
    
class ChatRequest(BaseModel):
    transcript: str
    question: str  
    video_id: str
        
def extract_video_id(url: str):
    parsed_url = urlparse(url)

    # Case 1: youtube.com/watch?v=...
    if "youtube.com" in parsed_url.netloc:
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]
        
        # Case 2: /shorts/VIDEO_ID
        if parsed_url.path.startswith("/shorts/"):
            return parsed_url.path.split("/")[2]

    # Case 3: youtu.be/VIDEO_ID
    if "youtu.be" in parsed_url.netloc:
        return parsed_url.path.lstrip("/")

    return None

@app.post("/get-transcript")
async def get_video_id(data: YouTubeRequest):
    video_id = extract_video_id(data.url)

    if not video_id:
        return {"error": "Invalid YouTube URL"}

    return {"video_id": video_id, "transcript": get_transcript(video_id)}  

@app.post("/summary")
async def get_summary(data: SummaryRequest):
      
    return {"summary": generate_summary(data.transcript)}

@app.post("/chat")
async def chat_with_video(data: ChatRequest):
    return {"response": ask_question(data.video_id, data.transcript, data.question)}