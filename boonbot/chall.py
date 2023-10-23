import enum

import discord
from discord import Thread

from .main import tree
from .config import config


SOLVED_POSTFIX = " (solved)"


class Categories(enum.Enum):
    WEB = "web"
    CRYPTO = "crypto"
    REVERSING = "rev"
    FORENSIC = "forensic"
    PWNABLE = "pwn"
    MISC = "misc"
    BLOCKCHAIN = "blockchain"
    OSINT = "osint"
    PROGRAMMING = "ppc"


@tree.command(name="new-chall")
async def new_chall(ctx: discord.Interaction, category: Categories, problem_name: str):
    channel_name = f"{category.name}: {problem_name}"
    for channel in ctx.channel.threads:
        if channel.name.removesuffix(SOLVED_POSTFIX) == channel_name:
            await ctx.response.send_message(f"すでに存在するよ！", ephemeral=True)
            return
    thread = await ctx.channel.create_thread(name=channel_name, auto_archive_duration=10080)
    await ctx.response.send_message(f"✅ {thread.mention}")


@tree.command(name="rename-chall")
async def rename_chall(ctx: discord.Interaction, category: Categories, problem_name: str):
    channel_name = f"{category.name}: {problem_name}"
    for channel in ctx.channel.threads:
        if channel.name.removesuffix(SOLVED_POSTFIX) == channel_name:
            await ctx.response.send_message(f"すでに存在するよ！", ephemeral=True)
            return
    await ctx.response.send_message("✅")
    await ctx.channel.edit(name=channel_name)


@tree.command(name="solved")
async def solved(ctx: discord.Interaction):
    if not isinstance(ctx.channel, Thread) or ctx.channel.category_id != config.contests_category_id:
        await ctx.response.send_message(f"コンテストスレッドじゃないよ！", ephemeral=True)
        return
    if ctx.channel.name.endswith(SOLVED_POSTFIX):
        await ctx.response.send_message(f"もうsolvedだよ！", ephemeral=True)
        return
    await ctx.response.send_message("Congratulations!")
    await ctx.channel.edit(name=ctx.channel.name + SOLVED_POSTFIX)


@tree.command(name="unsolved")
async def unsolved(ctx: discord.Interaction):
    if not isinstance(ctx.channel, Thread) or ctx.channel.category_id != config.contests_category_id:
        await ctx.response.send_message(f"コンテストスレッドじゃないよ！", ephemeral=True)
        return
    if not ctx.channel.name.endswith(SOLVED_POSTFIX):
        await ctx.response.send_message(f"まだsolvedじゃないよ！", ephemeral=True)
        return
    await ctx.response.send_message("✅")
    await ctx.channel.edit(name=ctx.channel.name.removesuffix(SOLVED_POSTFIX))
