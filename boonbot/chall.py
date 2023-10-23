import enum

import discord

from . import util
from .config import config
from .main import tree, CHECK_EMOJI, SOLVED_SUFFIX


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


@tree.command(name="new-chall", description="問題スレッドを作成します")
async def new_chall(ctx: discord.Interaction, category: Categories, problem_name: str):
    channel_name = f"{category.value}: {problem_name}"
    if not await util.check_is_in_contest_channel(ctx) or not await util.check_channel_exists(ctx, ctx.channel,
                                                                                              channel_name):
        return
    thread = await ctx.channel.create_thread(name=channel_name, auto_archive_duration=10080)
    await ctx.response.send_message(f"{thread.mention}を作成しました {CHECK_EMOJI} ")


@tree.command(name="rename-chall", description="問題名を変更します")
async def rename_chall(ctx: discord.Interaction, category: Categories, problem_name: str):
    channel_name = f"{category.value}: {problem_name}"
    if not await util.check_is_in_thread(ctx) or not await util.check_channel_exists(ctx, ctx.channel.parent,
                                                                                     channel_name):
        return
    await ctx.response.send_message(f"問題名を変更しました {CHECK_EMOJI}")
    await ctx.channel.edit(name=channel_name)


@tree.command(name="solved", description="スレッドをsolved状態にします")
async def solved(ctx: discord.Interaction):
    if not await util.check_is_in_thread(ctx) or not await util.check_is_unsolved(ctx):
        return
    await ctx.response.send_message(":tensai:")
    await ctx.channel.edit(name=ctx.channel.name + SOLVED_SUFFIX)


@tree.command(name="unsolved", description="スレッドをunsolved状態にします")
async def unsolved(ctx: discord.Interaction):
    if not await util.check_is_in_thread(ctx) or not await util.check_is_solved(ctx):
        return
    await ctx.response.send_message(":cry:")
    await ctx.channel.edit(name=ctx.channel.name.removesuffix(SOLVED_SUFFIX))


@tree.command(name="new-ctf", description="新しいコンテストチャンネルを作成します")
async def new_ctf(ctx: discord.Interaction, ctf_name: str):
    if not await util.check_is_in_bot_cmd(ctx):
        return
    channel = await ctx.guild.create_text_channel(ctf_name, category=ctx.guild.get_channel(config.contests_category_id))
    await ctx.response.send_message(f'{channel.mention}を作成しました {CHECK_EMOJI}')
