import discord
from discord import app_commands
from database.banned_word import get_banned_words
from database.role_database import fetch_roles
from database.database_commands import log_command_history

@app_commands.command(name='list_banned_words', description="(admin only) \n list all the banned word")
async def list_banned_words(interaction: discord.Interaction):
    banned_words = get_banned_words()

    if not banned_words:
        await interaction.response.send_message("There are no banned words currently.")
        return
    
    banned_words_list = "\n".join(banned_words)
    embed = discord.Embed(
        title="List of Banned Words",
        description=banned_words_list,
        color=discord.Color.red()
    )
    
    await interaction.response.send_message(embed=embed)
    log_command_history(interaction.user.id, interaction.user.name, interaction.command.name)
