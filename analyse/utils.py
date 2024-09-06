
import json



def parsellmjson(json_text):
  try:
      json_text = json_text.split("```json")[1]
      json_text = json_text.split("```")[0]
  
  except:
    json_text = json_text.replace("```json",'')
    json_text = json_text.replace("```",'')
  
  try:
    jd = json.loads(json_text)

    # return jd

    return jd
  except Exception as e:
    print(json_text)
    raise e
  
def save_output(data,name='out'):
  open(f"{name}.json",'w').write(json.dumps(data))



def json_formatter(json_text):
  import json
  jd = json.loads(json_text.strip().replace("```json","").replace('```',''))

  # return jd

  print(jd)
  output = []

  output.append(" People:")
  peopleList = jd.get("people") or []
  for person in peopleList:
    name = person.get('name')
    role = person.get('role')
    description = person.get('description')
    text = ""
    if name :
      text += f" - {name}"
    if role :
      text += f" - {role}"
    if description :
      text += f" - {description}"

    output.append(text)



  output.append(" Organizations:")
  ogs = jd.get("organizations") or []
  for org in ogs:
    text = ""
    if org.get('name'):
      text += f" - {org['name']}"
    if org.get('role'):
      text += f" - {org['role']}"

    output.append(text)


  output.append("")  # Adding a blank line for separation

  # Format places
  output.append("Places:")
  places = jd.get("places") or []

  for place in places:
    text = ""
    if place.get('location'):
      text += f" - {place['location']}"
    if place.get('description'):
      text += f" - {place['description']}"

    output.append(text)


  output.append("")

  # Format timeline
  output.append("Timeline:")
  timeline = jd.get("timeline") or []


  for entry in timeline:
    if 'date' in entry and 'event' in entry:
      output.append(f" - {entry['date']}: {entry['event']}")



  output.append("")  # Adding a blank line for separation

  # Format actions taken before coming to court
  output.append("Actions Taken already:")
  actions = jd.get("actions_taken") or []
  for action in actions:
    name = action.get('action')
    by = action.get('by')
    date = action.get('date')
    text=""

    if action :
      text += f" - {name}"
    if by :
      text += f" - {by}"
    if date :
      text += f" - {date}"

    output.append(text)

  output.append("\n")  # Adding a blank line for separation

  # Format claims
  output.append("Claims:")
  claims = jd.get("claims") or []
  for claim in jd['claims']:
      if 'claimant' in claim:
          output.append(f" - Claimant: {claim['claimant']}, Claim: {claim['claim']}")
      elif "defendant" in claim:
          output.append(f" - Defendant: {claim['defendant']}, Claim: {claim['claim']}")

      else:
          if "claim" in claim:
              output.append(f" - Claim: {claim['claim']}")
          else:
              output.append(f" - {claim}")

  output.append("")  # Adding a blank line for separation

  case_string = jd['detail_text'] + "\n" + "\n".join(output)

  title = jd.get('title')
  if title:
    del jd['title']

  return {
      'title':title,
      "caseoverview":jd,
      "case":case_string,

  }



def safe_content(content):
    """
    Escapes curly braces in the content to prevent LangChain from interpreting them as variables.
    """
    return content.replace('{', '{{').replace('}', '}}')



default_messages = [
          ["system", """
        witnesses, legal teams).
  1. 'places': Locations relevant to the case e.g., crime scene, court venue, places where evidence was gathered array of objects containing (name,date).
  2. 'timeline' : Important dates and events related to the case array of objects containing (date,event).
  3. 'actions_taken' : Steps and actions that were taken before the case reached court array of objects containing (action,by)
  4. 'claims' : Claims and assertions made in the case array of objects containing (claim,by).
  5. 'detail_text': Case Detailed Explanation -string (text)
  6 'people': array of objects containing (name,role,info),
  7 'organizations': array of objects containing (name,role,info),

  The output should be strictly JSON {format}

  when user answers your question following to a previous case in chat, you regerate the output strictly following the format with the updated information.
  ""","Welcome to Legal Sphere!\nTo get started, I’ll need some basic details about your case. Please provide Brief description of the issue."],
  ]


format = "{'places':[{name,date}],'people':[{name,role,info:'only if you know about the person'}],'organizations':[{name,role,info:'only if you know about the organization,should be in detail'}],'timeline':[{date,event}], 'actions_taken':[{action,by}],'claims':[{claim,by}],'message':' A humanly message to the user conveying how we understand the case and also attempt to gather more information with questions if required','detail_text':str, 'title':str}"


def new_chat():
  messages = default_messages.copy()
  # messages.append(['user',case_text,case_text])

  return messages

def user_message(chat,message):
  chat.append(['user',message,message])
  return chat


def display_message(messages):
  print(messages[-1][2])