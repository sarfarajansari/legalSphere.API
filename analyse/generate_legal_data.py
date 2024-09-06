
from openai import AzureOpenAI
import time
import os
from .utils import parsellmjson

endpoint =  os.getenv("AZURE_ENDPOINT")
search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_index = os.getenv("AZURE_SEARCH_INDEX")
search_key = os.getenv("AZURE_SEARCH_KEY")


def generate_legal_data(casedata,attemp=0):
  deployment = "gpt-4o"
  client = AzureOpenAI(
      azure_endpoint=endpoint,
      api_key='50f8303273e34afd88a2846303333be1',
      api_version="2024-05-01-preview",
  )

  input = casedata['case']

  completion = None
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
        max_tokens=3000,
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

    Follow the JSON structure to understand the output requirement
    keep arrays empty when you don't have enough data
    Output should be stricly JSON : {
    "evidence_and_support": {
      "witness_statements": ["Summaries or key points from witness statements. "],
      "expert_opinions": ["Relevant expert opinions that could support the case."],
      "detailed_evidence": ["Detailed evidence that supports your case."]
    },
    "case_strategy": {
      "legal_strategies": ["Suggested strategies for presenting the case, including defenses for your side."],
      "opposition_weaknesses": ["Identification of weaknesses in the opposition’s case."],
      "defenses_for_opposite":[ "Possible defenses the opposing party might use."],
      "cross_examination_questions": ["Suggested questions for cross-examining the opposition’s witnesses."]
    },
    "risk_and_outcome_analysis": {
      "potential_outcomes": ["Analysis of potential outcomes based on similar cases."],
      "risk_analysis": ["Assessment of risks involved in the case."],
      "financial_impact": ["Potential financial implications or damages associated with the case."],
      "appeal_potential": ["Analysis of the potential for appeal if the case doesn’t go in favor."]
    },
    "settlement_and_negotiation": {
      "settlement_options":[ "Possible settlement options and their implications."],
      "negotiation_tactics": ["Suggested tactics for negotiating with the opposing party."]
    },
    "courtroom_and_trial_management": {
      "courtroom_procedures": ["Suggested courtroom procedures and etiquette."],
      "jury_instructions": ["Guidelines or suggestions for jury instructions."],
      "document_checklist": ["Checklist of necessary documents for the case."]
    },
    "public_relations_and_client_communication": {
      "public_relations_impact": ["Analysis of how the case might affect public perception."],
      "client_communication": ["Suggestions for communicating case progress to the client."]
    }
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
    if attemp < 5:
      time.sleep(8)
      print("retrying")
      return generate_legal_data(casedata,attemp+1)

    raise e



  additional_data =  parsellmjson(completion.choices[0].message.content)
  print("Generated additional data")

  for key in additional_data:
    casedata[key] = additional_data[key]






  return casedata
