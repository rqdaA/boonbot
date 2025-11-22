import enum
from typing import Dict, List, Set

import discord
from discord import ChannelType, app_commands
from discord.ui import Button, View

from . import util, perm
from .config import config
from .main import tree, client, CHECK_EMOJI, SOLVED_PREFIX, RUNNING_EMOJI, JOIN_EMOJI, ERROR_EMOJI

auto_join_users: Dict[int, Set[int]] = {}


class JoinButton(View):
    def __init__(self, thread):
        super().__init__(timeout=None)
        self.thread = thread

    @discord.ui.button(label="Join", style=discord.ButtonStyle.primary)
    async def join_button(self, interaction: discord.Interaction, button: Button):
        await self.thread.add_user(interaction.user)
        await interaction.response.send_message(f"スレッドに参加しました {CHECK_EMOJI}", ephemeral=True)


class AutoJoinButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="問題スレッドに自動で参加", style=discord.ButtonStyle.success)
    async def auto_join_button(self, interaction: discord.Interaction, button: Button):
        channel_id = interaction.channel.id
        if channel_id not in auto_join_users:
            auto_join_users[channel_id] = set()
        auto_join_users[channel_id].add(interaction.user.id)
        await interaction.response.send_message(
            f"問題スレッドに自動で参加するように設定しました {CHECK_EMOJI}",
            ephemeral=True,
        )


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
    thread = await ctx.channel.create_thread(
        name=channel_name, type=ChannelType.public_thread, auto_archive_duration=10080
    )
    await thread.send(view=JoinButton(thread))
    adding_users = set(ctx.guild.get_member(user_id) for user_id in auto_join_users.get(ctx.channel.id) or [])
    for user in adding_users | {ctx.user}:
        await thread.add_user(user)
    await ctx.delete_original_response()


@tree.command(name="rename-chall", description="問題名を変更します")
async def rename_chall(ctx: discord.Interaction, category: Categories, problem_name: str):
    channel_name = f"{category.value}: {problem_name}"
    if not await util.check_is_in_thread(ctx) or not await util.check_channel_exists(
        ctx, ctx.channel.parent, channel_name
    ):
        return
    await ctx.response.send_message(f"問題名を変更しました {CHECK_EMOJI}")
    await ctx.channel.edit(
        name=(f"{SOLVED_PREFIX}{channel_name}" if ctx.channel.name.startswith(SOLVED_PREFIX) else channel_name)
    )


@tree.command(name="solved", description="スレッドをsolved状態にします")
async def solved(ctx: discord.Interaction):
    if not await util.check_is_in_thread(ctx) or not await util.check_is_unsolved(ctx):
        return
    tensai_emoji = await util.get_tensai_emoji(ctx)
    await ctx.response.send_message(str(tensai_emoji))
    await ctx.channel.edit(name=f"{SOLVED_PREFIX}{ctx.channel.name}")


@tree.command(name="unsolved", description="スレッドをunsolved状態にします")
async def unsolved(ctx: discord.Interaction):
    if not await util.check_is_in_thread(ctx) or not await util.check_is_solved(ctx):
        return
    await ctx.response.send_message(":cry:")
    await ctx.channel.edit(name=ctx.channel.name.removeprefix(SOLVED_PREFIX))


@tree.command(name="new-ctf", description="新しいコンテストチャンネルを作成します")
async def new_ctf(ctx: discord.Interaction, ctf_name: str, role_name: str, need_reaction: bool = False):
    if not await util.check_is_in_bot_cmd(ctx):
        return
    else:
        role = list(filter(lambda _role: _role.name == role_name, ctx.guild.roles))
        if len(role) == 0:
            await ctx.response.send_message(f"指定されたロール名は存在しないよ！{ERROR_EMOJI}", ephemeral=True)
            return
        role = role[0]
        team_name = util.get_team_name_by_role(role)
        category_id = util.get_category_by_role(role)
        if need_reaction:
            overwrites = {
                ctx.guild.default_role: perm.PERMISSION_DENY,
            }
        else:
            overwrites = {
                ctx.guild.default_role: perm.PERMISSION_DENY,
                role: perm.PERMISSION_WHITE,
            }

        channel = await ctx.guild.create_text_channel(
            f"{RUNNING_EMOJI}{ctf_name}",
            category=ctx.guild.get_channel(category_id),
            overwrites=overwrites,
            position=0,
        )
        await channel.send(
            f"team name: `{team_name}`\npassword: `{util.gen_password(16)}`",
            view=AutoJoinButton(),
        )
        resp_text = f"{role_name}に{ctf_name} ({channel.mention}) を作成しました {CHECK_EMOJI}"
        if need_reaction:
            await ctx.response.defer()
            msg = await ctx.followup.send(f"{resp_text}\n参加するには{JOIN_EMOJI}を押してください")
            await msg.add_reaction(JOIN_EMOJI)
        else:
            await ctx.response.send_message(resp_text)


# TODO: need_reaction==TrueなCTFでunendをした時に閲覧制限の再設定がうまく行かない問題を解決
@tree.command(name="unend-ctf", description="コンテストの閲覧制限を再度付けます")
async def unend_ctf(ctx: discord.Interaction):
    if not await util.check_is_in_contest_channel(ctx):
        return

    for ch in [_ch for _ch in ctx.guild.channels if _ch.name == ctx.channel.name]:
        if ch.name.startswith(RUNNING_EMOJI):
            continue
        team_role = ctx.guild.get_role(util.get_role_by_category(ch.category))
        await ch.set_permissions(team_role, overwrite=perm.PERMISSION_WHITE)
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
        team_role = ctx.guild.get_role(util.get_role_by_category(ch.category))
        non_bot_member = list(filter(lambda u: not u.bot, ctx.guild.members))
        whitelisted_members = list(filter(lambda u: ch.overwrites_for(u).read_messages, non_bot_member))
        await ch.edit(name=ch.name.lstrip(RUNNING_EMOJI))
        for member in whitelisted_members:
            await ch.set_permissions(member, overwrite=perm.PERMISSION_DEFAULT)
        await ch.set_permissions(team_role, overwrite=perm.PERMISSION_DEFAULT)
        await ch.set_permissions(ctx.guild.default_role, overwrite=perm.PERMISSION_DEFAULT)
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


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.Member | discord.User):
    emoji = reaction.emoji
    if emoji != JOIN_EMOJI:
        return
    message = reaction.message
    if not util.is_bot_cmd_channel(message.channel):
        return
    if not any(line.startswith("参加するには") for line in message.content.split("\n")):
        return
    if not any(message.content.startswith(role.name) for role in user.roles):
        return
    contest_channel = message.channel_mentions
    if len(contest_channel) == 1:
        ch = contest_channel[0]
        await ch.set_permissions(user, overwrite=perm.PERMISSION_WHITE)


@client.event
async def on_reaction_remove(reaction: discord.Reaction, user: discord.Member | discord.User):
    emoji = reaction.emoji
    if emoji != JOIN_EMOJI:
        return
    message = reaction.message
    if not util.is_bot_cmd_channel(message.channel):
        return
    if not any(line.startswith("参加するには") for line in message.content.split("\n")):
        return
    if not any(message.content.startswith(role.name) for role in user.roles):
        return
    contest_channel = message.channel_mentions
    if len(contest_channel) == 1:
        ch = contest_channel[0]
        await ch.set_permissions(user, overwrite=perm.PERMISSION_DEFAULT)
