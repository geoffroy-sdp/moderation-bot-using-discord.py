import discord
from discord import app_commands
from database.role_database import remove_role
from database.role_database import fetch_roles

try:
    admin_roles, _, _ = fetch_roles()
except ValueError as e:
    print(f"Error unpacking roles: {e}")

@app_commands.command(name="remove_role", description="(admin only) \n Remove a role from the database")
async def remove_role_command(interaction: discord.Interaction, role: discord.Role):
    user_roles = [role.id for role in interaction.user.roles]
    is_admin = any(str(role_id) in admin_roles for role_id in user_roles)
    if is_admin:
    
        role_id = role.id
    
        if remove_role(role_id):
            await interaction.response.send_message(f"Role '{role.name}' with ID {role_id} has been removed from the database.", ephemeral=True)
        else:
            await interaction.response.send_message(f"No role with ID {role_id} found in the database.", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have the permission for use this command.", ephemeral=True)
