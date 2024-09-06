
import os
from .utils import parsellmjson
from .chatWithAiSeach import chatwithAISearch
endpoint =  os.getenv("AZURE_ENDPOINT")
search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_index = os.getenv("AZURE_SEARCH_INDEX")
search_key = os.getenv("AZURE_SEARCH_KEY")


def generate_legal_data(casedata,attemp=0):

  input = casedata['case']

  user_message = f"""Case Issue:
      {input}
  """

  system_message =  """You are a legal assistant specialized in commercial cases in india, you already have data regarding past judgements. You are asked to find out the following when given a new case by carefully analysing the case:

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


    """
  content = chatwithAISearch(system_message,user_message)




  additional_data =  parsellmjson(content)
  print("Generated additional data")

  for key in additional_data:
    casedata[key] = additional_data[key]

  return casedata
