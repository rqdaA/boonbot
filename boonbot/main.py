import logging
from argparse import ArgumentParser

import discord
from discord import app_commands

from .config import config

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
intents.messages = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
logger = logging.getLogger(__name__)

SOLVED_PREFIX = "🚩 "
CHECK_EMOJI = "✅"
ERROR_EMOJI = "😡"
RUNNING_EMOJI = "🆙"


@tree.command(name="help", description="Botで使えるコマンドを一覧で表示します")
async def commands_help(ctx: discord.Interaction):
    await ctx.response.send_message(
        f"""
## 利用可能なコマンド一覧
- help
- new-ctf
- new-chall 
- rename-chall
- join
- leave
- solved
- unsolved
""",
        ephemeral=True,
    )


@client.event
async def on_ready():
    await tree.sync()


def main():
    parser = ArgumentParser()
    parser.add_argument("--token", type=str, required=True)
    parser.add_argument("--guild-id", type=int, required=True)
    parser.add_argument("--bot-channel-id", type=int, required=True)
    parser.add_argument("--team-names", nargs="+", type=str, required=True)
    parser.add_argument("--contests-category-ids", nargs="+", type=int, required=True)
    parser.add_argument("--team-role-ids", nargs="+", type=int, required=True)
    res = parser.parse_args()

    logging.basicConfig(level=logging.INFO, force=True)
    config.guild_id = res.guild_id
    config.bot_channel_id = res.bot_channel_id
    config.team_names = res.team_names
    config.contests_category_ids = res.contests_category_ids
    config.team_role_ids = res.team_role_ids

    assert (
        len(config.team_names) == len(config.contests_category_ids) == len(config.team_role_ids)
    ), "team_names / contests_category_ids / team_role_ids の設定が正しくないよ！"

    client.run(res.token)
