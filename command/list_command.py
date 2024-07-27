import discord
from discord import app_commands
from discord.ext import commands
from database.role_database import fetch_roles

admin_roles, _, _ = fetch_roles()

@app_commands.command(name="list_commands", description="List all available commands")
async def list_commands(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    is_admin = any(str(role_id) in admin_roles for role_id in user_roles)
    if is_admin:
        embed = discord.Embed(
        title="Available Commands",
        description="Here is a list of all available commands:",
        color=discord.Color.blue()
        )

        for command in interaction.client.tree.get_commands():
            embed.add_field(name=f"/{command.name}", value=command.description, inline=False)

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("You do not have the permission for use this command.", ephemeral=True)
