import discord
from .main import tree
from .config import config


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
