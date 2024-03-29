import random
import string

import discord
from discord import TextChannel, Thread

from .config import config
from .main import ERROR_EMOJI, SOLVED_PREFIX


def gen_password(length: int):
    return "".join(random.choices(string.ascii_lowercase, k=length))


async def check_is_in_contest_channel(ctx: discord.Interaction):
    if not isinstance(ctx.channel, TextChannel) or ctx.channel.category_id != config.contests_category_id:
        await ctx.response.send_message(f"ここはコンテストチャンネルじゃないよ！{ERROR_EMOJI}", ephemeral=True)
        return False
    return True


async def check_channel_exists(ctx: discord.Interaction, parent: TextChannel, channel_name: str):
    for channel in parent.threads:
        if channel.name.removeprefix(SOLVED_PREFIX) == channel_name:
            await ctx.response.send_message(f"すでに存在するよ！{ERROR_EMOJI}", ephemeral=True)
            return False
    return True


async def check_is_in_thread(ctx: discord.Interaction):
    if not isinstance(ctx.channel, Thread) or ctx.channel.category_id != config.contests_category_id:
        await ctx.response.send_message(f"ここは問題スレッドじゃないよ！{ERROR_EMOJI}", ephemeral=True)
        return False
    return True


async def check_is_unsolved(ctx: discord.Interaction):
    if ctx.channel.name.startswith(SOLVED_PREFIX):
        await ctx.response.send_message(f"すでにsolvedだよ！{ERROR_EMOJI}", ephemeral=True)
        return False
    return True


async def check_is_solved(ctx: discord.Interaction):
    if not ctx.channel.name.startswith(SOLVED_PREFIX):
        await ctx.response.send_message(f"まだsolvedじゃないよ！{ERROR_EMOJI}", ephemeral=True)
        return False
    return True


async def check_is_in_bot_cmd(ctx: discord.Interaction):
    if ctx.channel.id != config.bot_channel_id:
        await ctx.response.send_message(
            f"{ctx.guild.get_channel(config.bot_channel_id).mention} で実行してね！{ERROR_EMOJI}",
            ephemeral=True,
        )
        return False
    return True


async def ratelimit_error(ctx: discord.Interaction):
    await ctx.response.send_message(f"レート制限だよ！{ERROR_EMOJI}", ephemeral=True)
