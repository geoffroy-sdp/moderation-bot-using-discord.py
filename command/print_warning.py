import discord
from discord import app_commands
from database.database import get_sanction_points
from database.database_commands import log_command_history

from database.role_database import fetch_roles

try:
    admin_roles, _, _ = fetch_roles()
except ValueError as e:
    print(f"Error unpacking roles: {e}")

@app_commands.command(name="print_warning", description="(admin only) \n Display the sanction points of a member")
async def print_warning(interaction: discord.Interaction, membre: discord.Member):
    user_roles = [role.id for role in interaction.user.roles]
    is_admin = any(str(role_id) in admin_roles for role_id in user_roles)
    if is_admin:    
        points = get_sanction_points(membre.id)
        await interaction.response.send_message(f'{membre.mention} has {points} sanction points.', ephemeral=True)

        log_command_history(interaction.user.id, interaction.user.name, interaction.command.name)
    else:
        await interaction.response.send_message("You do not have the permission for use this command.", ephemeral=True)
