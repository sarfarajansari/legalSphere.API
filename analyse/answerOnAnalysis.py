from .chatWithAiSeach import chatwithAISearch

def answerOnAnalysis(title,data,text):

  return  chatwithAISearch(
      f"""You are given a JSON data analysed from a legal case, the analysis was done by you.  You are supposed to answer the questions asked by the user. Don't make the answer too big, but it should explain everything. Use legal terms and be concise. 

        title : {title}
        data : {data}
        """,
      f"""{text}"""
  )
