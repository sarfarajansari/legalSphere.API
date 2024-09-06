from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

CONNECTION_STRING =   os.getenv("MONGO")
client = MongoClient(CONNECTION_STRING)


def get_database()-> MongoClient:

   return client['research_engine']
  

class DBClient:
    def __init__(self):
        self.db = get_database()
  
    def get_sphere_chat_id(self):
        db = self.db
        db['chat_counter'].update_one({},{"$inc":{"counter":1}},upsert=True,)
        counter =  db['chat_counter'].find_one({})['counter']
        return "sphere-chat"+ str(counter)
  
    def get_analysis(self,chat_id):
        latest = self.db['analysis'].aggregate([
        {
            '$sort': {
            '_id': -1
            }
        },
        {
            '$match': {
            'chat_id': chat_id
            }
        },
        {
            '$limit': 1
        },
        {
            '$project': {
            '_id': 0
            }
        }
        ])

        data = list(latest)

        if len(data)==0:
            raise Exception("Analysis not found")
        analysis = list(data)[0]

        return analysis
    
    def get_chat(self,chat_id):
        analysis = self.get_analysis(chat_id)
        return analysis['chat']
    
    def save_analysis(self,analysis,chat_id):
        analysis['chat_id'] = chat_id
        self.db['analysis'].insert_one(analysis)
    

    
  
