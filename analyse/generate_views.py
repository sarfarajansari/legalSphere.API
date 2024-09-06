import json
from threading import Thread
import os
from .completion import get_completion
endpoint =  os.getenv("AZURE_ENDPOINT")
search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_index = os.getenv("AZURE_SEARCH_INDEX")
search_key = os.getenv("AZURE_SEARCH_KEY")


def generate_views(casedata):

  title = casedata.get('title')
  if title:
    del casedata['title']
  data = {
      "title":title,
      "tree":casedata,

  }
  def gen_map():
    mapview = get_completion([
      {
          "role": "system",
          "content": "You are json expert, you take json in one form and convert to another. Convert the given JSON in legal case data Tree view to Map view, where you just need to keep array of pointer nodes in the map, where every node should contain {location:'full address of the location',date:'if available', events:['events that occured in the location'], description:'detailed explanation',coordinates:[lat,long (approximately)]}, every location node shall be unique . So just return {mapview:[pointers]}"
      },
      {
          "role": "user",
          "content": json.dumps(casedata)
      },
    ])
    data.update(mapview)


  def gen_evidence():
    evidenceBoard = get_completion([
      {
          "role": "system",
          "content": "You are json expert, you take json in one form and convert to another. Convert the given JSON of legal case data Tree view to Evidence board, where evidence board view is basically a graph containing nodes and edges, showing the relation of crucial entities in the case like people, places, events,laws, or whatever suits the  scenarios, and edges are just relation between two nodes. return {nodes:[{type:'node type',name:'node name or label',description:'explanation of the node', id:'some unique number'}], edges:[{'fromId:'node 1 id',toId:'node 2 id', descripition:'reason of relation'}]}"
      },
      {
          "role": "user",
          "content": json.dumps(casedata)
      },
    ])

    data['evidence_board'] = evidenceBoard

  def gen_timeline():
    timeline = get_completion([
      {
          "role": "system",
          "content": "You are json expert, you take json in one form and convert to another. Convert the given JSON of legal case data Tree view to Timeline View, where timeline view in the sequence of events happening in the case with detailed explnation. Return [{title:'event title',description:'description of the event',time:'time stamp of the event if available', location:'location of the event if available'}]"
      },
      {
          "role": "user",
          "content": json.dumps(casedata)
      },
    ])
    data['timeline'] = timeline

  t1 = Thread(target=gen_map)
  t2 = Thread(target=gen_evidence)
  t3 = Thread(target=gen_timeline)

  t1.start()
  t2.start()
  t3.start()

  t1.join()
  t2.join()
  t3.join()

  print("Generated views")

  return data


