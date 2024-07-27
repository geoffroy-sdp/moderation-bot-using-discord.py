import discord
from discord import app_commands
from database.role_database import list_roles

@app_commands.command(name="list_roles", description="List all roles in the database")
async def list_roles_command(interaction: discord.Interaction):
    print(f"Interaction: {interaction}")
    
    roles = list_roles()
    
    if roles:
        embed = discord.Embed(
            title="List of Roles",
            description="Here are all the roles in the database:",
            color=discord.Color.green()
        )
        
        for role in roles:
            embed.add_field(name="Role", value=role, inline=False)
        
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("No roles found in the database.", ephemeral=True)
