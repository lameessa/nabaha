from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import process_text_message

app = FastAPI()

# Enable CORS for frontend testing (e.g., Lovable)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Replace with frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Nabaha API (text only) is running!"}

class TextInput(BaseModel):
    message: str

@app.post("/analyze-text")
async def analyze_text(data: TextInput):
    result = process_text_message(data.message)
    return result
