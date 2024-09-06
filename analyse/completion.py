
from openai import AzureOpenAI
import time
import os
from .utils import parsellmjson
from dotenv import load_dotenv
load_dotenv()
endpoint =  os.getenv("AZURE_ENDPOINT")
search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_index = os.getenv("AZURE_SEARCH_INDEX")
search_key = os.getenv("AZURE_SEARCH_KEY")




def get_completion(messages,attempt=0):
  try:
    deployment = "gpt-4o-2"
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key='50f8303273e34afd88a2846303333be1',
        api_version="2024-05-01-preview",
    )

    completion = client.chat.completions.create(
          model=deployment,
          messages= messages,
          max_tokens=3000,
          temperature=0.7,
          top_p=0.95,
          frequency_penalty=0,
          presence_penalty=0,
          stop=None,
          stream=False
      )
    return  parsellmjson(completion.choices[0].message.content)
  except Exception as e:
    print(e)
    if attempt < 5:
      time.sleep(5)
      print("retrying")
      return get_completion(messages,attempt+1)
    raise e
