import random
import string

import discord
from discord import TextChannel, Thread, CategoryChannel, app_commands

from .config import config
from .main import ERROR_EMOJI, SOLVED_PREFIX


def gen_password(length: int):
    return "".join(random.choices(string.ascii_lowercase, k=length))


def get_team_info(member: discord.Member):
    for team_role_id, category_id in zip(config.team_role_ids, config.contests_category_ids):
        if member.get_role(team_role_id) is not None:
            return team_role_id, category_id
    return None, None


def get_contest_channels(guild: discord.Guild):
    channels = []
    for contests_category_id in config.contests_category_ids:
        channels.extend(guild.get_channel(contests_category_id).channels)
    return channels


def get_team_name_by_role(role: discord.Role):
    for team_role_id, team_name in zip(config.team_role_ids, config.team_names):
        if role.id == team_role_id:
            return team_name
    return None


def get_category_by_role(role: discord.Role):
    for team_role_id, category_id in zip(config.team_role_ids, config.contests_category_ids):
        if role.id == team_role_id:
            return category_id
    return None


def get_role_by_category(category: CategoryChannel):
    for team_role_id, category_id in zip(config.team_role_ids, config.contests_category_ids):
        if category.id == category_id:
            return team_role_id
    return None


async def check_is_in_contest_channel(ctx: discord.Interaction):
    if not isinstance(ctx.channel, TextChannel) or ctx.channel.category_id not in config.contests_category_ids:
        await ctx.response.send_message(f"ここはコンテストチャンネルじゃないよ！{ERROR_EMOJI}", ephemeral=True)
        return False
    return True


async def check_channel_exists(ctx: discord.Interaction, parent: TextChannel, channel_name: str):
    for channel in parent.threads:
        if channel.name.removeprefix(SOLVED_PREFIX).lower() == channel_name.lower():
            await ctx.response.send_message(f"すでに存在するよ！{ERROR_EMOJI}", ephemeral=True)
            return False
    return True


async def check_is_in_thread(ctx: discord.Interaction):
    if not isinstance(ctx.channel, Thread) or ctx.channel.category_id not in config.contests_category_ids:
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


async def get_tensai_emoji(ctx: discord.Interaction):
    for emoji in await ctx.guild.fetch_emojis():
        if emoji.name == "tensai":
            return emoji


def has_admin_role():
    async def predicate(interaction: discord.Interaction) -> bool:
        return interaction.user.get_role(config.admin_role_id) is not None

    return app_commands.check(predicate)
