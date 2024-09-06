from .utils import parsellmjson

from .chatWithAiSeach import chatwithAISearch

def get_legal_framework(casedata,):
  input = casedata['case']
  user_message = f"""Case Issue:
      {input}
  """
  system_message = """You are a legal assistant specialized in commercial cases in india, you already have data regarding past judgements. You are asked to find out the following when given a new case by carefully analysing the case:

    1) Strength and weekneess of the case
    2) Rules , regulations and laws which are applicable based on history with similar cases
    3)Referenced past judgement list with file links

    Output should be stricly JSON : {
      strengths:[''],
      weaknesses:[''],
      rules:[{rule:'',reason:''}],
      pastjudgments:[{citation:'',reason:'',filelink:''}]
    }

    """
  content = chatwithAISearch(system_message,user_message)

  legal_framework =  parsellmjson(content)


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
