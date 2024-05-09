import enum

import discord
from discord import ChannelType

from . import util, perm
from .config import config
from .main import tree, CHECK_EMOJI, SOLVED_PREFIX, ERROR_EMOJI


class Categories(enum.Enum):
    web = "web"
    crypto = "crypto"
    rev = "rev"
    forensic = "forensic"
    pwn = "pwn"
    misc = "misc"
    blockchain = "blockchain"
    osint = "osint"
    ppc = "ppc"


@tree.command(name="new-chall", description="問題スレッドを作成します")
async def new_chall(ctx: discord.Interaction, category: Categories, problem_name: str):
    channel_name = f"{category.value}: {problem_name}"
    if not await util.check_is_in_contest_channel(ctx) or not await util.check_channel_exists(
        ctx, ctx.channel, channel_name
    ):
        return
    await ctx.response.defer(ephemeral=True)
    await ctx.channel.create_thread(name=channel_name, type=ChannelType.public_thread, auto_archive_duration=10080)
    await ctx.delete_original_response()


@tree.command(name="rename-chall", description="問題名を変更します")
async def rename_chall(ctx: discord.Interaction, category: Categories, problem_name: str):
    channel_name = f"{category.value}: {problem_name}"
    if not await util.check_is_in_thread(ctx) or not await util.check_channel_exists(
        ctx, ctx.channel.parent, channel_name
    ):
        return
    await ctx.response.send_message(f"問題名を変更しました {CHECK_EMOJI}")
    await ctx.channel.edit(name=channel_name)


@tree.command(name="solved", description="スレッドをsolved状態にします")
async def solved(ctx: discord.Interaction):
    if not await util.check_is_in_thread(ctx) or not await util.check_is_unsolved(ctx):
        return
    await ctx.response.send_message("<:tensai:1096701452078022707>")
    await ctx.channel.edit(name=SOLVED_PREFIX + ctx.channel.name)


@tree.command(name="unsolved", description="スレッドをunsolved状態にします")
async def unsolved(ctx: discord.Interaction):
    if not await util.check_is_in_thread(ctx) or not await util.check_is_solved(ctx):
        return
    await ctx.response.send_message(":cry:")
    await ctx.channel.edit(name=ctx.channel.name.removeprefix(SOLVED_PREFIX))


@tree.command(name="new-ctf", description="新しいコンテストチャンネルを作成します")
async def new_ctf(ctx: discord.Interaction, ctf_name: str):
    if not await util.check_is_in_bot_cmd(ctx):
        return
    role_id, category_id = util.get_team_role(ctx.user)
    if role_id is None:
        await ctx.response.send_message(f"チームロールがついてないよ！{ERROR_EMOJI}")
    else:
        overwrites = {
            ctx.guild.default_role: perm.PERMISSION_DENY,
            ctx.guild.get_role(role_id): perm.PERMISSION_WHITE
        }
        channel = await ctx.guild.create_text_channel(ctf_name, category=ctx.guild.get_channel(category_id), overwrites=overwrites)
        await channel.send(f"`{util.gen_password(16)}`")
        await ctx.response.send_message(f"{channel.mention}を作成しました {CHECK_EMOJI}")
