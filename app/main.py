from fastapi import FastAPI,  Request
from datetime import date, datetime
import requests

app = FastAPI()



@app.on_event("startup")
def on_startup():
    print("starting app")
    

INFINITY_INT = 10**15#float('inf')
INFINITY_DATE = date.max
MIN_DATE = date.min

url = "https://dev.ylytic.com/ylytic/test"

def get_response_from_url(url):
    
        response = requests.get(url)
        print(response)
        if response.status_code == 200:
            return { **response.json()}
        else:
            return {"error": "Failed to hit API"}

@app.get("/search")
async def search(search_author: str = None, 
           at_from: date = MIN_DATE, at_to: date = INFINITY_DATE, 
           like_from: int = 0, like_to: float = INFINITY_INT, 
           reply_from: int = 0, reply_to: float = INFINITY_INT, 
           search_text: str = ""):
    
    comments = get_response_from_url(url)["comments"]
    res = []
    date_format = "%a, %d %b %Y %H:%M:%S %Z"
    for comment in comments:
        date = datetime.strptime(comment["at"], date_format).date()
        if at_from <= date <= at_to and like_from <= comment["like"] <= like_to and reply_from <= comment["reply"] <= reply_to and search_text in comment["text"]:
            res.append(comment)
    return res

@app.get("/")
def home():
    return {"message": "appication is woking"}
