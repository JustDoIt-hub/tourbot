import json
from pyrogram import Client, filters
from pyrogram.types import Message
import datetime

# Load the configuration
import config

# Initialize the bot
app = Client("tournament_bot", bot_token=config.BOT_TOKEN, api_id=config.API_ID, api_hash=config.API_HASH)

# Path to fixtures and teams JSON files
FIXTURES_FILE = "storage/fixtures.json"
TEAMS_FILE = "storage/teams.json"

# Helper function to load and save data
def load_data(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# Command: /fixtures (shows fixtures without scores)
@app.on_message(filters.command("fixtures"))
async def fixtures_command(client, message):
    data = load_data(FIXTURES_FILE)
    fixtures = data.get("fixtures", [])

    if fixtures:
        reply_text = "Upcoming Fixtures:\n\n"
        for idx, fixture in enumerate(fixtures, 1):
            reply_text += f"{idx}. {fixture['home_team']} vs {fixture['away_team']} - {fixture['date']}\n"
    else:
        reply_text = "No fixtures scheduled yet."

    await message.reply(reply_text)

# Command: /addfixture <home_team> <away_team> <date>
@app.on_message(filters.command("addfixture"))
async def add_fixture_command(client, message: Message):
    args = message.text.split()[1:]
    if len(args) != 3:
        await message.reply("Usage: /addfixture <home_team> <away_team> <date>")
        return

    home_team, away_team, date = args
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        await message.reply("Invalid date format. Please use 'YYYY-MM-DD'.")
        return

    data = load_data(FIXTURES_FILE)
    fixtures = data.get("fixtures", [])
    fixtures.append({
        "home_team": home_team,
        "away_team": away_team,
        "date": date,
        "score": None  # Score will be set later
    })

    save_data(FIXTURES_FILE, {"fixtures": fixtures})
    await message.reply(f"Fixture added: {home_team} vs {away_team} on {date}")

# Command: /setscore <fixture_index> <score>
@app.on_message(filters.command("setscore"))
async def set_score_command(client, message: Message):
    args = message.text.split()[1:]
    if len(args) != 2:
        await message.reply("Usage: /setscore <fixture_index> <score> (e.g. 2 1-0)")
        return

    try:
        index = int(args[0]) - 1  # User-facing index starts from 1
        score = args[1]

        data = load_data(FIXTURES_FILE)
        fixtures = data.get("fixtures", [])

        if 0 <= index < len(fixtures):
            fixtures[index]["score"] = score
            save_data(FIXTURES_FILE, {"fixtures": fixtures})
            fixture = fixtures[index]
            await message.reply(f"Score updated: {fixture['home_team']} vs {fixture['away_team']} is now {score}")
        else:
            await message.reply("Invalid fixture index.")
    except ValueError:
        await message.reply("Fixture index must be a number.")

# Command: /scores (shows all matches with a score)
@app.on_message(filters.command("scores"))
async def scores_command(client, message: Message):
    data = load_data(FIXTURES_FILE)
    fixtures = data.get("fixtures", [])

    scored_matches = [f for f in fixtures if f.get("score")]
    if scored_matches:
        reply_text = "Match Scores:\n\n"
        for idx, fixture in enumerate(scored_matches, 1):
            reply_text += f"{idx}. {fixture['home_team']} vs {fixture['away_team']} - Score: {fixture['score']}\n"
    else:
        reply_text = "No scores have been recorded yet."

    await message.reply(reply_text)

# Command: /table (just a link to the table for now)
@app.on_message(filters.command("table"))
async def table_command(client, message: Message):
    website_url = "https://your-website-name.netlify.app"
    await message.reply(f"Check out the latest points table here: {website_url}")

# Start the bot
print("Bot is running keep working")
if __name__ == "__main__":
    app.run()
