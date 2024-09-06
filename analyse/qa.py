from .completion import get_completion
from .chatWithAiSeach import chatwithAISearch

def isQuestion(text):
  res = get_completion([
    {
        "role":"system",
        "content":""" Hey you are supposed to detect whether a text has question or not that's it.Output format shall be json {question:true/false}"""
    },
    {
        "role":"user",
        "content":text
    }
])
  
  return res.get('question')==True





def answerOnAnalysis(title,data,text):

  return  chatwithAISearch(
      f"""You are given a JSON data analysed from a legal case, the analysis was done by you.  You are supposed to answer the questions asked by the user. Don't make the answer too big, but it should explain everything. Use legal terms and be concise. When the user refersc to a case, it means the case mentioned in the data.

        title : {title}
        data : {data}
        """,
      f"""{text}"""
  )