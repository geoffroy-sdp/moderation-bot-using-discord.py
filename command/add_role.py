import discord
from discord import app_commands
from database.role_database import fetch_roles, add_role as add_role_to_db

try:
    admin_roles, warning_only_roles, muted_role = fetch_roles()
except ValueError as e:
    print(f"Error unpacking roles: {e}")

@app_commands.command(name="add_role", description="(admin only) \n Add a role to the database")
async def add_role(interaction: discord.Interaction, role: discord.Role, role_type: str):
    
    user_roles = [role.id for role in interaction.user.roles]
    if not any(str(role) in admin_roles for role in user_roles):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return
    if role_type not in ["admin", "warning only", "mute"]:
        await interaction.response.send_message("Invalid role type. Please specify 'admin', 'warning only', or 'mute'.", ephemeral=True)
        return
    add_role_to_db(role_type, role.id, role.name)
    await interaction.response.send_message(f"Role '{role.name}' with ID {role.id} added to the database as '{role_type}'.", ephemeral=True)
