import discord
from discord import app_commands
from database.database import reset_sanction_points
from database.role_database import fetch_roles
from database.database_commands import log_command_history

admin_roles, _, _ = fetch_roles()

@app_commands.command(name="reset_sanctions", description="(admin only) \n Reset sanction points for all members")
async def reset_sanctions(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if not any(str(role) in admin_roles for role in user_roles):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return

    try:
        reset_sanction_points()
        await interaction.response.send_message("All sanction points have been reset.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message("An error occurred while resetting sanctions.", ephemeral=True)
        print(f"Error: {e}")

    log_command_history(interaction.user.id, interaction.user.name, interaction.command.name)
