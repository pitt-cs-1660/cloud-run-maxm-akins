from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore
from typing import Annotated
import datetime

app = FastAPI()

# mount static files
app.mount("/static", StaticFiles(directory="/app/static"), name="static")
templates = Jinja2Templates(directory="/app/template")

# init firestore client
db = firestore.Client()
votes_collection = db.collection("votes")


@app.get("/")
async def read_root(request: Request):
    # ====================================
    # ++++ START CODE HERE ++++
    # ====================================

    # get all votes from firestore collection
    votes = votes_collection.stream()
    # @note: we are storing the votes in `vote_data` list because the firestore stream closes after certain period of time
    vote_data = []
    tabs_count = 0
    spaces_count = 0
    for v in votes:
        dict_data = v.to_dict()
        if dict_data["team"] == "TABS":
            tabs_count += 1
        elif dict_data["team"] == "SPACES":
            spaces_count += 1
        vote_data.append(dict_data)
    

    return templates.TemplateResponse("index.html", {
        "request": request,
        "tabs_count": tabs_count,
        "spaces_count": spaces_count,
        "recent_votes": vote_data
    })


@app.post("/")
async def create_vote(team: Annotated[str, Form()]):
    if team not in ["TABS", "SPACES"]:
        raise HTTPException(status_code=400, detail="Invalid vote")
    
    print("ENDPOINT CALLED")

    # ====================================
    # ++++ START CODE HERE ++++
    # ====================================

    try:
        votes_collection.add({
            "team": team,
            "time_cast": datetime.datetime.utcnow().isoformat()
        })
        return {"detail": "vote submitted"}
    except Exception as e:
        print("error submitting votes")
        return {"detail": "error submitting votes"}

    # ====================================
    # ++++ STOP CODE ++++
    # ====================================
