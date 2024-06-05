import enum

import discord
from discord import ChannelType

from . import util, perm
from .config import config
from .main import tree, CHECK_EMOJI, SOLVED_PREFIX, ERROR_EMOJI, RUNNING_EMOJI


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
async def new_ctf(ctx: discord.Interaction, ctf_name: str, role_name: str):
    if not await util.check_is_in_bot_cmd(ctx):
        return
    else:
        role = list(filter(lambda _role: _role.name == role_name, ctx.guild.roles))[0]
        team_name = util.get_team_name_by_role(role)
        category_id = util.get_category_by_role(role)
        overwrites = {ctx.guild.default_role: perm.PERMISSION_DENY, role: perm.PERMISSION_WHITE}

        channel = await ctx.guild.create_text_channel(
            f"{RUNNING_EMOJI}{ctf_name}", category=ctx.guild.get_channel(category_id), overwrites=overwrites
        )
        await channel.send(f"team name: `{team_name}`\npassword: `{util.gen_password(16)}`")
        await ctx.response.send_message(f"{role_name}に{channel.mention}を作成しました {CHECK_EMOJI}")


@tree.command(name="unend-ctf", description="コンテストの閲覧制限を再度付けます")
async def unend_ctf(ctx: discord.Interaction):
    if not await util.check_is_in_contest_channel(ctx):
        return

    for ch in [_ch for _ch in ctx.guild.channels if _ch.name == ctx.channel.name]:
        if ch.name.startswith(RUNNING_EMOJI):
            continue
        await ch.set_permissions(ctx.guild.default_role, overwrite=perm.PERMISSION_DENY)
        await ch.edit(name=f"{RUNNING_EMOJI}{ch.name}")
        if ch.id != ctx.channel.id:
            await ch.send(f"ロール制限を付けました {CHECK_EMOJI}")
    await ctx.response.send_message(f"ロール制限を付けました {CHECK_EMOJI}")


@tree.command(name="end-ctf", description="コンテストの閲覧制限を外します")
async def end_ctf(ctx: discord.Interaction):
    if not await util.check_is_in_contest_channel(ctx):
        return

    for ch in [_ch for _ch in ctx.guild.channels if _ch.name == ctx.channel.name]:
        if not ch.name.startswith(RUNNING_EMOJI):
            continue
        await ch.set_permissions(ctx.guild.default_role, overwrite=perm.PERMISSION_DEFAULT)
        await ch.edit(name=ch.name.lstrip(RUNNING_EMOJI))
        if ch.id != ctx.channel.id:
            await ch.send(f"ロール制限を外しました {CHECK_EMOJI}")
    await ctx.response.send_message(f"ロール制限を外しました {CHECK_EMOJI}")


@new_ctf.autocomplete("role_name")
async def autocomplete(ctx: discord.Interaction, current: str) -> list[discord.app_commands.Choice[str]]:
    roles = [ctx.guild.get_role(role_id) for role_id in config.team_role_ids]
    return sorted(
        [discord.app_commands.Choice(name=role.name, value=role.name) for role in roles if current in role.name],
        key=lambda choice: choice.name,
    )
