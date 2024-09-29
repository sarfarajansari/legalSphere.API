
from analyse.utils import new_chat, user_message, display_message, save_output
from analyse.qa import isQuestion, answerOnAnalysis
import json
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import DBClient
from random import randint
from fastapi import FastAPI, WebSocket
from analyse.chat_analysis import analyse_chat
from dotenv import load_dotenv
from fastapi.responses import FileResponse
from pdf import generate_pdf
import os
load_dotenv()
from fastapi import  BackgroundTasks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/new-chat")
def new_chat_endpoint(data: dict):
    case = data.get('case')
    if not case:
        return {"error": "case is required"}
    chat = new_chat()
    user_message(chat, case)

    db = DBClient()

    id = db.get_sphere_chat_id()
    analysis = analyse_chat(chat)
    db.save_analysis(analysis, id)

    return {"chat_id": id}


@app.get("/analysis/{chat_id}")
def get_analysis(chat_id: str):

    print(chat_id)
    db = DBClient()
    try:
        analysis = db.get_analysis(chat_id)
    except:
        return JSONResponse(status_code=404, content={"error": "chat not found"})
    return analysis


@app.post("/chat/{chat_id}")
def chat_endpoint(chat_id: str, data: dict):
    db = DBClient()
    analysis = db.get_analysis(chat_id)
    chat = analysis['chat']

    message = data.get('message')

    isPOI = isQuestion(message)

    print(isPOI)
    print(message)
    if isPOI:
        print("Answering a question")
        answer = answerOnAnalysis(
            analysis['title'], json.dumps(analysis['tree']), message)
        analysis['chat'].append(['user', message, message])
        analysis['chat'].append(['assistant', answer, answer])
        db.save_analysis(analysis, chat_id)
        del analysis['_id']
        return analysis

    if not message:
        return {"error": "message is required"}

    user_message(chat, message)
    new_analysis = analyse_chat(chat)
    new_analysis['title'] = analysis['title']
    db.save_analysis(new_analysis, chat_id)
    del new_analysis['_id']

    return new_analysis




def delete_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)


@app.get("/pdf/{chat_id}")
async def pdfView(chat_id:str, background_tasks: BackgroundTasks):
    db = DBClient()
    analysis = db.get_analysis(chat_id)
    if not analysis:
        return JSONResponse(status_code=404, content={"error": "chat not found"})
    
    tree = analysis.get('tree')
    title = analysis.get('title')

    if not tree or not title:
        return JSONResponse(status_code=404, content={"error": "analysis not found"})
    
    filepath = generate_pdf(tree, title)

    response = FileResponse(path=filepath, media_type='application/pdf')
    
    background_tasks.add_task(delete_file,filepath)
    return response

