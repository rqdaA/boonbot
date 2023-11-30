import discord

from .config import config
from .main import tree, CHECK_EMOJI
from .util import check_is_in_bot_cmd, check_is_in_contest_channel

PERMISSION_ALLOW = discord.PermissionOverwrite(read_messages=None, manage_channels=None)
PERMISSION_DENY = discord.PermissionOverwrite(
    read_messages=False, manage_channels=False
)
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
    await ctx.response.send_message(
        f"{channel.mention} から離脱しました {LEAVE_MARK}", ephemeral=True
    )


@tree.command(name="join", description="コンテストチャンネルに復帰します")
async def join(ctx: discord.Interaction, channel: str):
    if not await check_is_in_bot_cmd(ctx):
        return

    target = list(
        filter(lambda ch: ch.name == channel, [ch for ch in ctx.guild.channels])
    )
    if not target:
        await ctx.response.send_message(f"This must be a bug 🥲")
    target_ch = target[0]
    await target_ch.set_permissions(ctx.user, overwrite=PERMISSION_ALLOW)
    await target_ch.send(f"{ctx.user.mention} が復帰しました {JOIN_MARK}")
    await ctx.response.send_message(
        f"{target_ch.mention} に復帰しました {JOIN_MARK}", ephemeral=True
    )


@join.autocomplete("channel")
async def autocomplete(
    ctx: discord.Interaction, current: str
) -> list[discord.app_commands.Choice[str]]:
    contests = ctx.guild.get_channel(config.contests_category_id).channels
    did_leave = lambda ch: ch.overwrites_for(ctx.user).read_messages is not None

    return [
        discord.app_commands.Choice(name=ch.name, value=ch.name)
        for ch in contests
        if did_leave(ch) and current.lower() in ch.name.lower()
    ]
