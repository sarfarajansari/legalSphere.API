from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import json
import os
from .utils import json_formatter,safe_content, format
from .legal_framework import get_legal_framework
from .generate_legal_data import generate_legal_data
from .generate_views import generate_views



endpoint =  os.getenv("AZURE_ENDPOINT")
search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_index = os.getenv("AZURE_SEARCH_INDEX")
search_key = os.getenv("AZURE_SEARCH_KEY")


print("endp",endpoint)
def analyse_chat(messages ):

  chat_messages=[]
  for message in messages:
    chat_messages.append((message[0],message[1]))

  prompt = ChatPromptTemplate.from_messages(messages=chat_messages)


  llm = AzureChatOpenAI(
      azure_deployment="gpt-4o-2",
      api_version="2024-05-01-preview",
      api_key='50f8303273e34afd88a2846303333be1',
      azure_endpoint=endpoint
  )

  chain = prompt | llm |StrOutputParser()  |json_formatter  | get_legal_framework | generate_legal_data | generate_views

  out = chain.invoke({"format":format})

  caseoverview = out['tree']['caseoverview']
  chat = messages

  message = caseoverview['message']

  chat.append(['assistant',safe_content(json.dumps(caseoverview)),message])

  out['chat'] = chat
  return out
