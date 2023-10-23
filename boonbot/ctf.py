import discord
from .main import tree, CHECK_EMOJI
from .config import config


@tree.command(name="new-ctf", description="新しいCTFチャンネルを作成します")
async def new_ctf(interaction: discord.Interaction, ctf_name: str):
    await interaction.guild.create_text_channel(ctf_name,
                                                category=interaction.guild.get_channel(config.contests_category_id))
    await interaction.response.send_message(f'{CHECK_EMOJI}')
