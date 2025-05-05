from flask import Flask, render_template
import json
import os

app = Flask(__name__, template_folder='site/templates')

# Serve static files (CSS, images, etc.)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join('site', 'static'), filename)

# Serve the index.html template from 'templates' folder
@app.route('/')
def home():
    scoreboard = get_scoreboard()
    return render_template('index.html', scoreboard=scoreboard)

# Load the teams data from the JSON file
def load_teams():
    with open("storage/teams.json", "r") as f:
        return json.load(f)

# Get and sort the scoreboard
def get_scoreboard():
    teams = load_teams()["teams"]
    for team in teams:
        team["points"] = team["wins"] * 3 + team["draws"]
        team["goal_difference"] = team["goals_for"] - team["goals_against"]
    # Sort by points, goal difference, and goals scored if needed
    return sorted(teams, key=lambda x: (x["points"], x["goal_difference"], x["goals_for"]), reverse=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
