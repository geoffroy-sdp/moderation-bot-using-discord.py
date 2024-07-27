import discord
from discord import app_commands
import asyncio
from database.database_commands import log_command_history
from database.role_database import fetch_roles

try:
    admin_roles, _, _ = fetch_roles()
except ValueError as e:
    print(f"Error unpacking roles: {e}")

@app_commands.command(name="clear", description="(admin only) \n delete all the message from a channel")
async def clear(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if not any(str(role) in admin_roles for role in user_roles):
        await interaction.response.send_message("You do not have the permission for use this command.", ephemeral=True)
        return True

    await interaction.channel.purge()
    await asyncio.sleep(2)  # Wait 2 seconds before the next purge
    await interaction.channel.send("A new fresh history")
    log_command_history(interaction.user.id, interaction.user.name, interaction.command.name)
