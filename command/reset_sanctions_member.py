import discord
from discord import app_commands
from database.database import reset_sanction_points_member
from database.role_database import fetch_roles
from database.database_commands import log_command_history

admin_roles, _, _ = fetch_roles()

@app_commands.command(name="reset_sanctions_member", description="(admin only) \n Reset the sanction points of a member")
async def reset_sanctions_member(interaction: discord.Interaction, member: discord.Member):
    user_roles = [role.id for role in interaction.user.roles]
    if not any(str(role) in admin_roles for role in user_roles):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return

    member_roles = [role.id for role in member.roles]
    if any(str(role) in admin_roles for role in member_roles):
        await interaction.response.send_message("It's an admin, they don't have sanction points.", ephemeral=True)
        return

    reset_sanction_points_member(member.id)
    await interaction.response.send_message(f'Sanction points for {member.mention} have been reset to 0.', ephemeral=True)

    log_command_history(interaction.user.id, interaction.user.name, interaction.command.name)
