import discord
from .main import tree, CHECK_EMOJI
from .config import config
from .util import check_is_in_bot_cmd


@tree.command(name="new-ctf", description="新しいCTFチャンネルを作成します")
async def new_ctf(ctx: discord.Interaction, ctf_name: str):
    if not await check_is_in_bot_cmd(ctx):
        return
    await ctx.guild.create_text_channel(ctf_name, category=ctx.guild.get_channel(config.contests_category_id))
    await ctx.response.send_message(f'{CHECK_EMOJI}')
