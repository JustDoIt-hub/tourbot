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

# Helper function to load data from JSON files
def load_data(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# Command: /fixtures
@app.on_message(filters.command("fixtures"))
async def fixtures_command(client, message):
    data = load_data(FIXTURES_FILE)
    fixtures = data.get("fixtures", [])

    if fixtures:
        # Display fixtures in a formatted way
        reply_text = "Upcoming Fixtures:\n\n"
        for idx, fixture in enumerate(fixtures, 1):
            reply_text += f"{idx}. {fixture['home_team']} vs {fixture['away_team']} - {fixture['date']} - Score: {fixture.get('score', 'Not Played Yet')}\n"
    else:
        reply_text = "No fixtures scheduled yet."

    await message.reply(reply_text)

# Command: /addfixture <home_team> <away_team> <date> <score>
@app.on_message(filters.command("addfixture"))
async def add_fixture_command(client, message: Message):
    # Extract arguments from the message
    args = message.text.split()[1:]
    if len(args) != 4:
        await message.reply("Usage: /addfixture <home_team> <away_team> <date> <score>")
        return

    home_team, away_team, date, score = args
    try:
        # Validate date format
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        await message.reply("Invalid date format. Please use 'YYYY-MM-DD' format.")
        return

    # Load current fixtures and add the new one
    data = load_data(FIXTURES_FILE)
    fixtures = data.get("fixtures", [])
    fixtures.append({
        "home_team": home_team,
        "away_team": away_team,
        "date": date,
        "score": score
    })

    # Save updated fixtures back to the JSON file
    save_data(FIXTURES_FILE, {"fixtures": fixtures})

    await message.reply(f"Fixture added: {home_team} vs {away_team} on {date} with score {score}")

# Command: /table (To display the points table, assuming teams.json is already loaded)
@app.on_message(filters.command("table"))
async def table_command(client, message: Message):
    # Here we will just provide a link to the website displaying the table.
    website_url = "https://your-website-name.netlify.app"
    await message.reply(f"Check out the latest points table here: {website_url}")

# Start the bot
if __name__ == "__main__":
    app.run()
