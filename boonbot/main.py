import logging
from argparse import ArgumentParser

import discord
from discord import app_commands

from .config import config, CONFIG_FILE

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
JOIN_EMOJI = "💪"


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
- team list
- whitelist
- unwhitelist
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
    parser.add_argument("--admin-role-id", type=int, required=True)
    res = parser.parse_args()

    logging.basicConfig(level=logging.INFO, force=True)
    config.guild_id = res.guild_id
    config.bot_channel_id = res.bot_channel_id
    config.admin_role_id = res.admin_role_id

    loaded_from_file = config.load_from_file()
    logger.info(f"Loading team configuration from file: {'Success' if loaded_from_file else 'Failed'}")
    if not loaded_from_file:
        print(f'{CONFIG_FILE} not found')
        exit(1)

    assert (
            len(config.team_names) == len(config.contests_category_ids) == len(config.team_role_ids)
    ), "team_names / contests_category_ids / team_role_ids の設定が正しくないよ！"

    client.run(res.token)
