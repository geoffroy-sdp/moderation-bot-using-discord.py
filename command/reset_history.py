import discord
from discord import app_commands
from database.database import reset_sanction_data
from database.role_database import fetch_roles
from database.database_commands import log_command_history

admin_roles, _, _ = fetch_roles()

@app_commands.command(name="reset_history", description="(admin only) \n Reset the sanction history in the database")
async def reset_history(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if not any(str(role) in admin_roles for role in user_roles):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
    else:
        reset_sanction_data()
        await interaction.response.send_message("All sanction data has been reset in the database.", ephemeral=True)
    
    log_command_history(interaction.user.id, interaction.user.name, interaction.command.name)