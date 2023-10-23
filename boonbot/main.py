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


@tree.command(name="new-ctf", description="新しいCTFチャンネルを作成します")
async def new_ctf(interaction: discord.Interaction, ctf_name: str):
    channel = await interaction.guild.create_text_channel(ctf_name,
                                                          category=interaction.guild.get_channel(1166000686975172690))
    await interaction.response.send_message(f'新しいCTFを作成しました。 {channel.mention}')


@tree.command(
    name="new-chall",
    description="新しい問題スレッドを作成します"
)
@discord.app_commands.choices(
    category=[
        discord.app_commands.Choice(name="Pwnable", value="pwn"),
        discord.app_commands.Choice(name="Crypto", value="crypto"),
        discord.app_commands.Choice(name="Web", value="web"),
        discord.app_commands.Choice(name="Reversing", value="rev")
    ]
)
async def new_chall(ctx: discord.Interaction, category: str, problem_name: str):
    channel_name = f"{category}-{problem_name}"
    thread = await ctx.channel.create_thread(name=channel_name, reason="あああ")
    await ctx.response.send_message(f"スレッドを作成したよ！: {thread.mention}")


@tree.command(
    name="solved"
)
async def solved(ctx: discord.Interaction):
    print(ctx.channel)


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
