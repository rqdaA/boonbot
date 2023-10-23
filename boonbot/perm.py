import discord
from .main import tree, CHECK_EMOJI
from .config import config
from .util import check_is_in_bot_cmd, check_is_in_contest_channel

PERMISSION_ALLOW = discord.PermissionOverwrite(read_messages=None, manage_channels=None)
PERMISSION_DENY = discord.PermissionOverwrite(read_messages=False, manage_channels=False)


@tree.command(name="leave", description="現在のCTFチャンネルから離脱します")
async def leave(ctx: discord.Interaction, channel: discord.TextChannel = None):
    if channel:
        if not await check_is_in_bot_cmd(ctx):
            return
        await channel.set_permissions(ctx.user, overwrite=PERMISSION_DENY)
    else:
        if not await check_is_in_contest_channel(ctx):
            return
        await ctx.channel.set_permissions(ctx.user, overwrite=PERMISSION_DENY)
    await ctx.response.send_message(f'{CHECK_EMOJI}')


@tree.command(name="join", description="CTFチャンネルに復帰します")
async def join(ctx: discord.Interaction, channel: str):
    if not await check_is_in_bot_cmd(ctx):
        return

    target = list(filter(lambda ch: ch.name == channel, [ch for ch in ctx.guild.channels]))
    if not target:
        await ctx.response.send_message(f'404 🥲')
    await target[0].set_permissions(ctx.user, overwrite=PERMISSION_ALLOW)
    await ctx.response.send_message(f'{CHECK_EMOJI}')


@join.autocomplete("channel")
async def autocomplete(ctx: discord.Interaction, current: str) -> list[discord.app_commands.Choice[str]]:
    contests = ctx.guild.get_channel(config.contests_category_id).channels
    did_leave = lambda ch: ch.overwrites_for(ctx.user).read_messages is not None

    return [
        discord.app_commands.Choice(name=ch.name, value=ch.name)
        for ch in contests if did_leave(ch) and current.lower() in ch.name.lower()
    ]
