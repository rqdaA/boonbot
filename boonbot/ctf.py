from discord.ext import commands

from main import bot, CHECK_EMOJI
from config import config

group = bot.group("ctf")


@bot.command(name='new-ctf', group=group, usage="bot channel: !new-ctf [ctf-name]")
@bot_channel_command
async def new_ctf(ctx: commands.Context, name: str, *role_ids: int):
    expanded_role_ids = (*(config.member_role_ids if len(role_ids) == 0 else role_ids), *config.bot_role_ids)

    roles = [r for r in ctx.guild.roles if r.id in expanded_role_ids]
    members = sum([r.members for r in roles], [])

    overwrites = {m: PERMISSION_ALLOW for m in members}
    overwrites[ctx.guild.default_role] = PERMISSION_DENY

    main_category = await ctx.guild.create_category(normalize(name), overwrites=overwrites)
    solved_category = await ctx.guild.create_category(normalize(name) + SOLVED_SUFFIX, overwrites=overwrites)
    await ctx.guild.create_text_channel(config.main_channel_name, category=main_category)

    # なんか1,2で順番に並べるよりうまく行く気がする……らしい
    await solved_category.edit(position=1)
    await main_category.edit(position=1)
    await ctx.message.add_reaction(CHECK_EMOJI)