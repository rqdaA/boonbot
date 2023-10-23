import discord
from discord import TextChannel, Thread

from .chall import SOLVED_POSTFIX
from .config import config


async def check_is_in_contest_channel(ctx: discord.Interaction):
    if not isinstance(ctx.channel, TextChannel) or ctx.channel.category_id != config.contests_category_id:
        await ctx.response.send_message(f"ここはコンテストチャンネルじゃないよ！", ephemeral=True)
        return False
    return True


async def check_channel_exists(ctx: discord.Interaction, parent: TextChannel, channel_name: str):
    for channel in parent.threads:
        if channel.name.removesuffix(SOLVED_POSTFIX) == channel_name:
            await ctx.response.send_message(f"すでに存在するよ！", ephemeral=True)
            return False
    return True


async def check_is_in_thread(ctx: discord.Interaction):
    if not isinstance(ctx.channel, Thread) or ctx.channel.category_id != config.contests_category_id:
        await ctx.response.send_message(f"ここは問題スレッドじゃないよ！", ephemeral=True)
        return False
    return True


async def check_is_unsolved(ctx: discord.Interaction):
    if ctx.channel.name.endswith(SOLVED_POSTFIX):
        await ctx.response.send_message(f"すでにsolvedだよ！", ephemeral=True)
        return False
    return True


async def check_is_solved(ctx: discord.Interaction):
    if not ctx.channel.name.endswith(SOLVED_POSTFIX):
        await ctx.response.send_message(f"まだsolvedじゃないよ！", ephemeral=True)
        return False
    return True


async def check_is_in_bot_cmd(ctx: discord.Interaction):
    if ctx.channel.id != config.bot_channel_id:
        await ctx.response.send_message(f"{ctx.guild.get_channel(config.bot_channel_id).mention} で実行してね！",
                                        ephemeral=True)
        return False
    return True


async def ratelimit_error(ctx: discord.Interaction):
    await ctx.response.send_message(f"レート制限だよ！", ephemeral=True)
