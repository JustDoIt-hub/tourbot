# handlers/commands.py

from pyrogram import Client, filters
from utils.json_handler import load_json, save_json
from config import TEAM_FILE

def register_command_handlers(app: Client):
    @app.on_message(filters.command("start"))
    async def start(client, message):
        """Greet the user and explain commands."""
        await message.reply("👋 Welcome! Use /table to see the standings or /match to update results.")

    @app.on_message(filters.command("table"))
    async def show_table(client, message):
        """Show the current league table."""
        teams = load_json(TEAM_FILE)
        if not teams:
            return await message.reply("No data yet. Please add match results using /match.")
        
        sorted_teams = sorted(
            teams.items(),
            key=lambda x: (-x[1]['points'], -(x[1]['gf'] - x[1]['ga']), -x[1]['gf'])
        )
        text = "🏆 *League Table*\n\n"
        for i, (team, stats) in enumerate(sorted_teams, 1):
            gd = stats['gf'] - stats['ga']
            text += f"{i}. {team} - {stats['points']} pts (W:{stats['won']} D:{stats['drawn']} L:{stats['lost']} GD:{gd})\n"
        await message.reply(text, parse_mode="markdown")

    @app.on_message(filters.command("match"))
    async def update_match(client, message):
        """Record match results and update league table."""
        parts = message.text.split()
        if len(parts) != 5:
            return await message.reply("❗ Use the format: /match TeamA 2 TeamB 1")

        team1, score1, team2, score2 = parts[1], int(parts[2]), parts[3], int(parts[4])
        teams = load_json(TEAM_FILE)

        # Initialize teams if they don't exist
        for team in [team1, team2]:
            if team not in teams:
                teams[team] = {
                    "played": 0, "won": 0, "drawn": 0, "lost": 0,
                    "gf": 0, "ga": 0, "points": 0
                }

        # Update stats based on the match result
        teams[team1]["played"] += 1
        teams[team2]["played"] += 1
        teams[team1]["gf"] += score1
        teams[team1]["ga"] += score2
        teams[team2]["gf"] += score2
        teams[team2]["ga"] += score1

        if score1 > score2:
            teams[team1]["won"] += 1
            teams[team1]["points"] += 3
            teams[team2]["lost"] += 1
        elif score2 > score1:
            teams[team2]["won"] += 1
            teams[team2]["points"] += 3
            teams[team1]["lost"] += 1
        else:
            teams[team1]["drawn"] += 1
            teams[team2]["drawn"] += 1
            teams[team1]["points"] += 1
            teams[team2]["points"] += 1

        save_json(TEAM_FILE, teams)
        await message.reply("✅ Match result updated!")
