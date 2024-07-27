import discord
from discord import app_commands
from database.banned_word import remove_banned_word, get_banned_words
from database.database_commands import log_command_history
from database.role_database import fetch_roles

try:
    admin_roles, _, _ = fetch_roles()
    banned_word = get_banned_words()
except ValueError as e:
    print(f"Error unpacking roles: {e}")

@app_commands.command(name="delete_word", description="(admin only) \n Remove a word from the list of banned words")
async def delete_word(interaction: discord.Interaction, mot: str):
    user_roles = [role.id for role in interaction.user.roles]
    is_admin = any(str(role) in admin_roles for role in user_roles)
    if is_admin:
        mot = mot.lower()
        if mot in banned_word:
            try:
                remove_banned_word(mot)
                await interaction.response.send_message(f'The word "{mot}" has been removed from the list of banned words.', ephemeral=True)
                log_command_history(interaction.user.id, interaction.user.name, interaction.command.name)
            except Exception as e:
                await interaction.response.send_message(f'An error occurred while removing the word "{mot}": {e}', ephemeral=True)
        else:
            await interaction.response.send_message(f'The word "{mot}" was not found in the list of banned words.', ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
