import discord
from discord import app_commands
from database.banned_word import add_banned_word
from database.database_commands import log_command_history
from database.role_database import fetch_roles

try:
    admin_roles, _, _ = fetch_roles()
except ValueError as e:
    print(f"Error unpacking roles: {e}")


@app_commands.command(name="add_word", description="(admin only) \n Add a word to the list of banned words")
async def add_word(interaction: discord.Interaction, mot: str):
    user_roles = [role.id for role in interaction.user.roles]
    
    is_admin = any(str(role_id) in admin_roles for role_id in user_roles)
    if is_admin:
        mot = mot.lower()
        try:
            add_banned_word(mot)
            await interaction.response.send_message(f'The word "{mot}" has been added to the list of banned words.', ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f'An error occurred while adding the word "{mot}": {e}', ephemeral=True)
        
        log_command_history(interaction.user.id, interaction.user.name, interaction.command.name)
    else:
        await interaction.response.send_message("You do not have the permission for use this command.", ephemeral=True)