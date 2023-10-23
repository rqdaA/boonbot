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

# bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
logger = logging.getLogger(__name__)

SOLVED_SUFFIX = "-solved"
PIN_EMOJI = "📌"
CHECK_EMOJI = "✅"


@client.event
async def on_ready():
    await tree.sync()


@tree.command(name="test", description="this is test")
async def test_command(interaction: discord.Interaction, text: str):
    await interaction.response.send_message("てすと！", ephemeral=True)


def main():
    parser = ArgumentParser()
    parser.add_argument("--token", type=str, required=True)
    # parser.add_argument("--guild-id", type=int, required=True)
    # parser.add_argument("--bot-channel-id", type=int, required=True)
    # parser.add_argument("--bot-role-ids", nargs="+", type=int, required=True)
    # parser.add_argument("--member-role-ids", nargs="+", type=int, required=True)
    # parser.add_argument("--special-category-ids", nargs="+", type=int, required=True)
    # parser.add_argument("--main-channel-name", type=str, default="main")
    res = parser.parse_args()

    logging.basicConfig(level=logging.INFO, force=True)
    # config.guild_id = res.guild_id
    # config.bot_channel_id = res.bot_channel_id
    # config.main_channel_name = res.main_channel_name
    # config.bot_role_ids = res.bot_role_ids
    # config.member_role_ids = res.member_role_ids
    # config.special_category_ids = res.special_category_ids

    client.run(res.token)
    # bot.run(res.token)
