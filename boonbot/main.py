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

SOLVED_SUFFIX = " (solved)"
CHECK_EMOJI = "✅"
ERROR_EMOJI = "😡"


@tree.command(name="help", description="Botで使えるコマンドを一覧で表示します")
async def help(ctx: discord.Interaction):
    await ctx.response.send_message(f"""
## 利用可能なコマンド一覧
- help
- new-ctf
- new-chall 
- rename-chall
- join
- leave
- solved
- unsolved
""", ephemeral=True)


@client.event
async def on_ready():
    await tree.sync()


def main():
    parser = ArgumentParser()
    parser.add_argument("--token", type=str, required=True)
    parser.add_argument("--guild-id", type=int, required=True)
    parser.add_argument("--bot-channel-id", type=int, required=True)
    parser.add_argument('--contests-category-id', type=int, required=True)
    res = parser.parse_args()

    logging.basicConfig(level=logging.INFO, force=True)
    config.guild_id = res.guild_id
    config.bot_channel_id = res.bot_channel_id
    config.contests_category_id = res.contests_category_id

    client.run(res.token)
