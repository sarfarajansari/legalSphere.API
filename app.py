
from dotenv import load_dotenv

load_dotenv()
from analyse.chat_analysis import analyse_chat
from analyse.qa import isQuestion,answerOnAnalysis

from analyse.utils import new_chat,user_message,display_message,save_output
from fastapi import FastAPI, WebSocket
from random import randint
from db import DBClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/new-chat")
def new_chat_endpoint(data:dict):
    case = data.get('case')
    if not case:
        return {"error":"case is required"}
    chat = new_chat()
    user_message(chat,case)


    db = DBClient()

    id = db.get_sphere_chat_id()
    analysis = analyse_chat(chat)
    db.save_analysis(analysis,id)

    return {"chat_id":id}

@app.get("/analysis/{chat_id}")
def get_analysis(chat_id:str):

    print(chat_id)
    db = DBClient()
    try:
        analysis = db.get_analysis(chat_id)
    except:
        return JSONResponse(status_code=404,content={"error":"chat not found"})
    return analysis


@app.post("/chat/{chat_id}")
def chat_endpoint(chat_id:str,data:dict):
    db = DBClient()
    analysis = db.get_analysis(chat_id)
    chat = analysis['chat']

    message = data.get('message')

    isPOI= isQuestion(message)

    print(isPOI)
    print(message)
    if isPOI:
        print("Answering a question")
        answer = answerOnAnalysis(analysis['title'],json.dumps(analysis['tree']),message)
        analysis['chat'].append(['user',message,message])
        analysis['chat'].append(['assistant',answer,answer])
        db.save_analysis(analysis,chat_id)
        del analysis['_id']
        return analysis
    
    if not message:
        return {"error":"message is required"}
    
    user_message(chat,message)
    new_analysis = analyse_chat(chat)
    new_analysis['title'] = analysis['title']
    db.save_analysis(new_analysis,chat_id)
    del new_analysis['_id']


    return new_analysis







    

    


