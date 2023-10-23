import logging
import discord
from discord import app_commands
from argparse import ArgumentParser

from .config import config

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
intents.messages = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
logger = logging.getLogger(__name__)

SOLVED_SUFFIX = "-solved"
PIN_EMOJI = "📌"
CHECK_EMOJI = "✅"


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
