# handlers/callbacks.py

from pyrogram import Client
from pyrogram.types import CallbackQuery
from utils.json_handler import load_json
from config import TEAM_FILE

def register_callback_handlers(app: Client):
    @app.on_callback_query()
    async def callback_handler(client, query: CallbackQuery):
        if query.data == "show_table":
            teams = load_json(TEAM_FILE)
            sorted_teams = sorted(
                teams.items(),
                key=lambda x: (-x[1]['points'], -(x[1]['gf'] - x[1]['ga']), -x[1]['gf'])
            )
            text = "🏆 *League Table*\n\n"
            for i, (team, stats) in enumerate(sorted_teams, 1):
                gd = stats['gf'] - stats['ga']
                text += f"{i}. {team} - {stats['points']} pts (W:{stats['won']} D:{stats['drawn']} L:{stats['lost']} GD:{gd})\n"
            await query.message.edit_text(text, parse_mode="markdown")
