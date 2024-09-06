
from openai import AzureOpenAI
import time
import os
from .utils import parsellmjson

endpoint =  os.getenv("AZURE_ENDPOINT")
search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_index = os.getenv("AZURE_SEARCH_INDEX")
search_key = os.getenv("AZURE_SEARCH_KEY")


def get_legal_framework(casedata,attempt=0):
  deployment = "gpt-4o"
  client = AzureOpenAI(
      azure_endpoint=endpoint,
      api_key='50f8303273e34afd88a2846303333be1',
      api_version="2024-05-01-preview",
  )

  input = casedata['case']

  completion=None
  try:
    completion = client.chat.completions.create(
        model=deployment,
        messages= [
        {
          "role": "user",
          "content": f"""**Case Issue**
      {input}
  """
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
                "role_information": """You are a legal assistant specialized in commercial cases in india, you already have data regarding past judgements. You are asked to find out the following when given a new case by carefully analysing the case:

    1) Strength and weekneess of the case
    2) Rules , regulations and laws which are applicable based on history with similar cases
    3)Referenced past judgement list with file links

    Output should be stricly JSON : {
      strengths:[''],
      weaknesses:[''],
      rules:[{rule:'',reason:''}],
      pastjudgments:[{citation:'',reason:'',filelink:''}]
    }

    """,
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
      return get_legal_framework(casedata,attempt+1)
    raise e

  legal_framework =  parsellmjson(completion.choices[0].message.content)


  # print(legal_framework)
  print("Generated Legal Framework")

  output = []
  output.append("strength : ")
  output.extend(legal_framework['strengths'])
  output.append("weaknesses : ")
  output.extend(legal_framework['weaknesses'])
  output.append("rules :")


  for rule in legal_framework['rules']:
    output.append(f" - {rule['rule']} - {rule['reason']}")


  case_string = input + "\n" + "\n".join(output)
  casedata['legalframework'] = legal_framework
  casedata['case'] = case_string


  return casedata
