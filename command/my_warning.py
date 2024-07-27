import discord
from discord import app_commands
from database.database import get_sanction_points
from database.database_commands import log_command_history

@app_commands.command(name="my_warning", description="See your sanction points")
async def my_warning(interaction: discord.Interaction):
    points = get_sanction_points(interaction.user.id)
    await interaction.response.send_message(f'You have {points} sanction points.', ephemeral=True)
    
    log_command_history(interaction.user.id, interaction.user.name, interaction.command.name)
