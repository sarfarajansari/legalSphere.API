
from openai import AzureOpenAI
import time
import os

endpoint =  os.getenv("AZURE_ENDPOINT")
search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_index = os.getenv("AZURE_SEARCH_INDEX")
search_key = os.getenv("AZURE_SEARCH_KEY")



def chatwithAISearch(systemMessage,userMessage,attempt=0):
  deployment = "gpt-4o"
  client = AzureOpenAI(
      azure_endpoint=endpoint,
      api_key='50f8303273e34afd88a2846303333be1',
      api_version="2024-05-01-preview",
  )



  completion=None
  try:
    completion = client.chat.completions.create(
        model=deployment,
        messages= [
        {
          "role": "user",
          "content": userMessage
        }],
        max_tokens=2000,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False,
        extra_body={
          "data_sources": [{
              "type": "azure_search",
              "parameters": {
                "endpoint": f"{search_endpoint}",
                "index_name": search_index,
                "semantic_configuration": "default",
                "query_type": "vector_semantic_hybrid",
                "fields_mapping": {},
                "in_scope": True,
                "role_information": systemMessage,
                "filter": None,
                "strictness": 3,
                "top_n_documents": 6,
                "authentication": {
                  "type": "api_key",
                  "key": f"{search_key}"
                },
                "embedding_dependency": {
                  "type": "deployment_name",
                  "deployment_name": "customusage"
                }
              }
            }]
        }
    )

  except Exception as e:
    print(e)
    if attempt < 5:
      time.sleep(8)
      print("retrying")
      return chatwithAISearch(systemMessage,userMessage,attempt+1)
    raise e

  return completion.choices[0].message.content
