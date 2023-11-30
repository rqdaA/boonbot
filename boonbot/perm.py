import discord

from .config import config
from .main import tree
from .util import check_is_in_bot_cmd, check_is_in_contest_channel

PERMISSION_ALLOW = discord.PermissionOverwrite(read_messages=None, manage_channels=None)
PERMISSION_DENY = discord.PermissionOverwrite(read_messages=False, manage_channels=False)
LEAVE_MARK = ":broken_heart:"
JOIN_MARK = ":heart:"


@tree.command(name="leave", description="現在のコンテストチャンネルから離脱します")
async def leave(ctx: discord.Interaction, channel: discord.TextChannel = None):
    if channel:
        if not await check_is_in_bot_cmd(ctx):
            return
        await channel.set_permissions(ctx.user, overwrite=PERMISSION_DENY)
        await channel.send(f"{ctx.user.mention} が離脱しました {LEAVE_MARK}")
    else:
        if not await check_is_in_contest_channel(ctx):
            return
        await ctx.channel.set_permissions(ctx.user, overwrite=PERMISSION_DENY)
        await ctx.channel.send(f"{ctx.user.mention} が離脱しました {LEAVE_MARK}")
    await ctx.response.send_message(f"{channel.mention} から離脱しました {LEAVE_MARK}", ephemeral=True)


@tree.command(name="join", description="コンテストチャンネルに復帰します")
async def join(ctx: discord.Interaction, channel: str):
    if not await check_is_in_bot_cmd(ctx):
        return

    target = list(filter(lambda ch: ch.name == channel, [ch for ch in ctx.guild.channels]))
    if not target:
        await ctx.response.send_message(f"This must be a bug 🥲")
    target_ch = target[0]
    await target_ch.set_permissions(ctx.user, overwrite=PERMISSION_ALLOW)
    await target_ch.send(f"{ctx.user.mention} が復帰しました {JOIN_MARK}")
    await ctx.response.send_message(f"{target_ch.mention} に復帰しました {JOIN_MARK}", ephemeral=True)


@tree.command(name="whitelist", description="チャンネルを閲覧できるメンバーを制限します")
async def whitelist(
    ctx: discord.Interaction,
    u1: discord.Member,
    u2: discord.Member = None,
    u3: discord.Member = None,
    u4: discord.Member = None,
    u5: discord.Member = None,
):
    if not await check_is_in_contest_channel(ctx):
        return

    non_bot_guild_member = [member for member in ctx.guild.members if not member.bot]
    current_members = list(filter(lambda u: ctx.channel.overwrites_for(u).read_messages is None, non_bot_guild_member))
    target_members = list(filter(lambda u: u is not None, [ctx.user, u1, u2, u3, u4, u5]))

    if all([ctx.channel.overwrites_for(member).read_messages is None for member in non_bot_guild_member]):
        # Channel is Not Whitelisted
        mentions = " ".join({user.mention for user in target_members})
        await ctx.response.send_message(f"ホワイトリストに変更しました\nメンバー:{mentions}")
        for member in non_bot_guild_member:
            if member not in target_members:
                await ctx.channel.set_permissions(member, overwrite=PERMISSION_DENY)
    else:
        # Channel is Already Whitelisted
        if all([member in current_members for member in target_members]):
            await ctx.response.send_message(f"そのメンバーはすでにホワイトリストに入っています")
            return

        for member in target_members:
            await ctx.channel.set_permissions(member, overwrite=PERMISSION_ALLOW)
        mentions = " ".join({member.mention for member in target_members if member not in current_members})
        await ctx.response.send_message(f"{mentions}をホワイトリストに追加しました")


@join.autocomplete("channel")
async def autocomplete(ctx: discord.Interaction, current: str) -> list[discord.app_commands.Choice[str]]:
    contests = ctx.guild.get_channel(config.contests_category_id).channels
    did_leave = lambda ch: ch.overwrites_for(ctx.user).read_messages is not None

    return [
        discord.app_commands.Choice(name=ch.name, value=ch.name)
        for ch in contests
        if did_leave(ch) and current.lower() in ch.name.lower()
    ]
