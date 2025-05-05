from flask import Flask, render_template
import json

def load_teams():
    with open("storage/teams.json", "r") as f:
        return json.load(f)

# Tell Flask to look in the site/static/ directory for static files
app = Flask(__name__, static_folder='site/static')

@app.route('/')
def home():
    scoreboard = get_scoreboard()
    return render_template('index.html', scoreboard=scoreboard)

def get_scoreboard():
    teams = load_teams()["teams"]
    for team in teams:
        team["points"] = team["wins"] * 3 + team["draws"]
        team["goal_difference"] = team["goals_for"] - team["goals_against"]
    
    return sorted(teams, key=lambda x: (x["points"], x["goal_difference"]), reverse=True)

if __name__ == '__main__':
    app.run(debug=True)
