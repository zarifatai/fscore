from flask import Flask
from flask import render_template
from sportdataapi.api import SportDataApi
import json

app = Flask(__name__)

api = SportDataApi()
matches = api.get_matches("England", "Premier League", "21/22", "2022-01-22")

for match in matches:
    if match.status == "finished":
        print(f"{match.home_team.name}-{match.away_team.name} ({match.stats.home_score}-{match.stats.away_score})")

@app.route("/")
def get_index():
    return render_template("index.html")

@app.route("/get_matches")
def get_matches():
    return json.dumps(matches.__dict__)
