from typing import Annotated
import os
from fastapi import FastAPI, File, UploadFile
import shutil
from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from vectordb import ingest_file
from llm_engine import llm_core
from langchain_community.chat_message_histories import FileChatMessageHistory
from pydantic import BaseModel



app = FastAPI()

history = {}
os.makedirs("history", exist_ok=True)
os.makedirs("uploads", exist_ok=True)

uploads  =  os.path.join(os.getcwd(), "uploads")



app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})





# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}




@app.post("/uploadfile/save/")
async def file_save( request: Request, file: Annotated[UploadFile, File()]):
    file_location = os.path.join(uploads, file.filename)
    with open(file_location, "wb") as file_object:
        shutil.copyfileobj(file.file, file_object)
        
        
    try:
        ingest_file(file_location, file.filename)
    except ValueError as e:
        os.remove(file_location)  
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )

    print("INGESTION DONE")


    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": f"File '{file.filename}' uploaded successfully!"
        }
    )


class ChatRequest(BaseModel):
    message: str
    filename: str | None = None


class ChatResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):

    key = request.filename 

    if not key:
        return {"answer": "Please select a document first."}

    if key not in history:
        
        history[key] = FileChatMessageHistory(
            file_path=os.path.join("history", f"{key}_history.json")
        )
    
    chat_history = history[key]

    query =  request.message.strip()
    chat_history.add_user_message(query)
    formatted_history = "\n".join(
        f"{msg.type.upper()}: {msg.content}"
        for msg in chat_history.messages
    )

    answer = llm_core(query, formatted_history, filename=request.filename)
    chat_history.add_ai_message(answer)

    return {"answer": answer}







@app.get("/files")
def list_uploaded_files():
    upload_dir = "uploads"
    files = []

    for f in os.listdir(upload_dir):
        if os.path.isfile(os.path.join(upload_dir, f)):
            files.append(f)

    return {"files": files}


@app.get("/history")
async def history_file(filename:str | None = None):

    key = filename

    if key not in history:
        return{"messages": []}
    
    chat_history = history[key]

    messages = [
        {
            "role": msg.type,
            "content": msg.content
        }
        for msg in chat_history.messages
    ]


    return{"messages":messages}



