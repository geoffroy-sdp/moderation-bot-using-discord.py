import discord
from discord import app_commands
from database.database import user_sanctions_collection
from database.role_database import fetch_roles
from database.database_commands import log_command_history

# Fetching admin roles from role_database
admin_roles, warning_only_roles, muted_role = fetch_roles()

@app_commands.command(name='list_sanctions', description="(admin only) \n list every sanctions point of all the guy in the server")
async def list_sanctions(interaction: discord.Interaction):
    user_roles = {role.id for role in interaction.user.roles}
    
    is_admin = any(str(role_id) in admin_roles for role_id in user_roles)
    if not is_admin:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return True

    sanctions = user_sanctions_collection.find().sort('sanction_points', -1)
    
    if user_sanctions_collection.count_documents({}) == 0:
        await interaction.response.send_message("There are no sanctions currently.")
        return
    
    embed = discord.Embed(
        title="Sanctions",
        description="List of user sanctions",
        color=discord.Color.red()
    )
    
    for sanction in sanctions:
        user_id = sanction.get('user_id', 'Unknown')
        username = sanction.get('username', 'Unknown')
        points = sanction.get('sanctions_points', 0)
        status = sanction.get('status', 'member')  # Default to 'member' if status is not available

        # Retrieve the member object to get the current roles
        member = interaction.guild.get_member(int(user_id))
        if member:
            member_roles = {role.id for role in member.roles}
            if any(str(role) in admin_roles for role in member_roles):
                status = 'admin'
            elif any(str(role) in warning_only_roles for role in member_roles):
                status = 'warning_only'
            elif muted_role in member_roles:
                status = 'muted'
            else:
                status = 'member'

            # Update the status in the database
            user_sanctions_collection.update_one(
                {'user_id': user_id},
                {'$set': {'status': status}}
            )
        else:
            status = 'Unknown'

        embed.add_field(name=username, value=f"ID: {user_id}\nPoints: {points}\nStatus: {status}", inline=False)
    
    await interaction.response.send_message(embed=embed)
    log_command_history(interaction.user.id, interaction.user.name, interaction.command.name)
