import discord
from discord import app_commands

from . import util
from .config import config
from .main import CHECK_EMOJI, ERROR_EMOJI, tree
from .util import has_admin_role

team = app_commands.Group(name="team", description="チーム管理コマンド")


@team.command(name="list", description="すべてのチームを表示します")
async def list_teams(ctx: discord.Interaction):
    if not await util.check_is_in_bot_cmd(ctx):
        return

    if len(config.team_names) == 0:
        await ctx.response.send_message("チームが設定されていません", ephemeral=True)
        return

    team_info = []
    for i, (team_name, category_id, role_id) in enumerate(
        zip(config.team_names, config.contests_category_ids, config.team_role_ids)
    ):
        category = ctx.guild.get_channel(category_id)
        role = ctx.guild.get_role(role_id)
        category_name = category.name if category else "不明なカテゴリ"
        role_name = role.name if role else "不明なロール"
        team_info.append(f"{i+1}. **{team_name}** - カテゴリ: {category_name}, ロール: {role_name}")

    await ctx.response.send_message("## チーム一覧\n" + "\n".join(team_info), ephemeral=True)


@team.command(name="add", description="新しいチームを追加します")
@has_admin_role()
async def add_team(
    ctx: discord.Interaction, team_name: str, contests_category: discord.CategoryChannel, team_role: discord.Role
):
    if not await util.check_is_in_bot_cmd(ctx):
        return

    if team_name in config.team_names:
        await ctx.response.send_message(f"チーム名 '{team_name}' はすでに存在します {ERROR_EMOJI}", ephemeral=True)
        return

    config.team_names.append(team_name)
    config.contests_category_ids.append(contests_category.id)
    config.team_role_ids.append(team_role.id)

    config.save_to_file()

    await ctx.response.send_message(
        f"チーム '{team_name}' を追加しました {CHECK_EMOJI}\n" f"カテゴリ: {contests_category.name}, ロール: {team_role.name}",
        ephemeral=True,
    )


@team.command(name="remove", description="チームを削除します")
@has_admin_role()
async def remove_team(ctx: discord.Interaction, team_name: str):
    if not await util.check_is_in_bot_cmd(ctx):
        return

    if team_name not in config.team_names:
        await ctx.response.send_message(f"チーム名 '{team_name}' は存在しません {ERROR_EMOJI}", ephemeral=True)
        return

    index = config.team_names.index(team_name)

    category_id = config.contests_category_ids[index]
    role_id = config.team_role_ids[index]
    category = ctx.guild.get_channel(category_id)
    role = ctx.guild.get_role(role_id)
    category_name = category.name if category else "不明なカテゴリ"
    role_name = role.name if role else "不明なロール"

    config.team_names.pop(index)
    config.contests_category_ids.pop(index)
    config.team_role_ids.pop(index)

    config.save_to_file()

    await ctx.response.send_message(
        f"チーム '{team_name}' を削除しました {CHECK_EMOJI}\n" f"カテゴリ: {category_name}, ロール: {role_name}",
        ephemeral=True,
    )


@remove_team.autocomplete("team_name")
async def team_name_autocomplete(ctx: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    return sorted(
        app_commands.Choice(name=name, value=name) for name in config.team_names if current.lower() in name.lower()
    )


tree.add_command(team)
