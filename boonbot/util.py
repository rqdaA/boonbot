import discord
from discord import TextChannel, Thread

from .chall import SOLVED_POSTFIX
from .config import config


async def check_is_in_contest_channel(ctx: discord.Interaction):
    if not isinstance(ctx.channel, TextChannel) or ctx.channel.category_id != config.contests_category_id:
        await ctx.response.send_message(f"コンテストチャンネルじゃないよ！", ephemeral=True)
        return False
    return True


async def check_channel_exists(ctx: discord.Interaction, channel_name: str):
    for channel in ctx.channel.threads:
        if channel.name.removesuffix(SOLVED_POSTFIX) == channel_name:
            await ctx.response.send_message(f"すでに存在するよ！", ephemeral=True)
            return False
    return True


async def check_is_in_thread(ctx: discord.Interaction):
    if not isinstance(ctx.channel, Thread) or ctx.channel.category_id != config.contests_category_id:
        await ctx.response.send_message(f"問題スレッドじゃないよ！", ephemeral=True)
        return False
    return True


async def check_is_unsolved(ctx: discord.Interaction):
    if ctx.channel.name.endswith(SOLVED_POSTFIX):
        await ctx.response.send_message(f"もうsolvedだよ！", ephemeral=True)
        return False
    return True


async def check_is_solved(ctx: discord.Interaction):
    if not ctx.channel.name.endswith(SOLVED_POSTFIX):
        await ctx.response.send_message(f"まだsolvedじゃないよ！", ephemeral=True)
        return False
    return True



