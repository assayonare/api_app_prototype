import os
from pathlib import Path
from dotenv import load_dotenv
import json
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

from ai.model import Model

def load_system_prompt():
    try:
        with open("prompts/system_prompt.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        return None
    
def save_recipe_response(response_data: dict, prompt: str):

    save_dir = Path("responses")
    save_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        if isinstance(response_data, dict) and "name" in response_data:
            safe_name = "".join(c for c in response_data["name"] if c.isalnum() or c in " _-").rstrip()
            safe_name = safe_name.replace(" ", "_").lower()
            filename = f"{timestamp}_{safe_name}.json"
        else:
            filename = f"{timestamp}_response.json"
    except:
        filename = f"{timestamp}_response.json"
    
    filepath = save_dir / filename
    
    save_data = {
        "timestamp": datetime.now().isoformat(),
        "temperature": 0.7,
        "prompt": prompt,
        "response": response_data
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)

    return str(filepath)

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str 


load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY is not set in the environment variables.")


system_prompt = load_system_prompt()
agent_model = Model(api_key=API_KEY, system_prompt=system_prompt)
# print(system_prompt)
app = FastAPI()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    print(request.prompt)
    response = agent_model.generate_response(request.prompt)

    try:
        response_data = json.loads(response)
        saved_path = save_recipe_response(response_data, request.prompt)
        print(f"The file is saved in {saved_path}")

    except json.JSONDecodeError:
        saved_path = save_recipe_response({"text": response}, request.prompt)
        print(f"The file is saved in {saved_path}")

    except Exception as e:
        print(f"Error saving: {e}")

    return ChatResponse(response=response)

@app.get("/")
async def root():
    return {"message": "API is running"}
