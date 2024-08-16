import discord
from discord.ext import commands
from discord.ui import Button
import json
import os

from command import (
    add_word,
    delete_word,
    print_warning,
    my_warning,
    clear,
    reset_sanctions_member,
    reset_sanctions,
    reset_history,
    list_banned_words,
    list_sanctions,
    add_role,
    remove_role_command,
    list_roles_command,
    list_commands,
    
    # utils
    
    timeout_user,
    is_alt_account,
    send_message_sanctions
)

from database.database import update_sanction_points, get_sanction_points, reset_sanction_points_member
from database.banned_word import get_banned_words
from database.role_database import fetch_roles

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

banned_word = get_banned_words()

admin_roles, warning_only_roles, muted_role = fetch_roles()

CONFIG_FILE = 'config.json'

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)
        
        token = data.get("token", [])
        GUILD_ID = data.get("Guild", [])
        
        dev = data.get("dev", [])
        contact_admin = data.get("admin", [])
        
        moderator_channel = data.get("moderator_channel", [])

else:
    token = []
    GUILD_ID = []
    
    dev = []
    contact_admin = []
    
    moderator_channel = []
    
# Warning thresholds    
mute_threshold = 3  # mute 2h
longer_mute_threshold = 4  # mute 24h
kick_threshold = 5  # kick
warning_before_ban = 6  # last warning
ban_threshold = 7  # ban

mute_duration = 10  # first mute
longer_mute_duration = 15  # second mute

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)

@bot.event
async def on_member_join(member):
    is_alt, reasons = is_alt_account(bot, member)
    if is_alt:
        channel = bot.get_channel(moderator_channel)
        if channel:
            reasons_str = "\n".join(reasons)
            await channel.send(
                f"{member.name} joined the server and is identified as a potential alt account. Reasons:\n{reasons_str}"
            )
        else:
            print(f"Channel with ID {moderator_channel} not found.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.guild is None:
        try:
            await message.author.send("This bot can't answer your request.")
        except discord.errors.Forbidden:
            print(f"Cannot send message to {message.author.name}")
        return  
    
    user_roles = [role.id for role in message.author.roles]
    is_admin = any(str(role) in admin_roles for role in user_roles)
    is_warning_only = any(str(role) in warning_only_roles for role in user_roles)

    current_sanction_points = get_sanction_points(message.author.id)
    banned_words = get_banned_words()
    point = get_sanction_points(message.author.id)

    if any(word in message.content.lower() for word in banned_words):
        try:
            await message.delete()
        except discord.NotFound:
            pass

        if is_admin:
            await message.channel.send(f'{message.author.mention}, you are admin, respect the rules!')
            update_sanction_points(message.author.id, message.author.name, points=0, is_admin=True)

        elif is_warning_only:
            update_sanction_points(message.author.id, message.author.name, 1)
            await message.channel.send(f'{message.author.mention}, you are a helper/distro, respect the rules!')
            if point >= mute_threshold:
                await message.channel.send(f'{message.author.mention}, you have been muted for {mute_duration} hours for reaching the sanction threshold.')
                await message.author.send(f'You have been muted because you have too many warnings (3).\nYou can contact an administrator if you want to complain about your mute.\n\nContact <@{contact_admin}>')
                await timeout_user(message.author, mute_duration)
                await send_warning_message(message.author, point)

        else:
            update_sanction_points(message.author.id, message.author.name, 1)
            point = get_sanction_points(message.author.id)
            await message.channel.send(f'{message.author.mention}, that word is not allowed!')

            if point == mute_threshold:
                await message.channel.send(f'{message.author.mention}, you have been muted for {mute_duration} hours for reaching the sanction threshold.')
                await message.author.send(f'You have been muted because you have too many warnings (3).\nYou can contact an administrator if you want to complain about your mute.\n\nContact <@{contact_admin}>')
                await timeout_user(message.author, mute_duration)
                await send_warning_message(message.author, point)

            elif point == longer_mute_threshold:
                await message.channel.send(f'{message.author.mention}, you have been muted for {longer_mute_duration} hours for reaching the sanction threshold.')
                await message.author.send(f'You have been muted because you have too many warnings (4).\nYou can contact an administrator if you want to complain about your mute.\n\nContact <@{contact_admin}>')
                await timeout_user(message.author, longer_mute_duration)
                await send_warning_message(message.author, point)

            elif point == kick_threshold:
                await message.author.send(f'You have been kicked because you have too many warnings (5).\nYou can contact an administrator if you want to complain about your kick.\n\nContact <@{contact_admin}>')
                await message.channel.send(f'{message.author.mention} has been kicked for too many warnings.')
                await message.guild.kick(message.author, reason="Too many warnings")
                await send_warning_message(message.author, point)

            elif point == warning_before_ban:
                await message.author.send(f'You have 6 warnings. One more warning and you will be banned permanently!\n\nContact <@{contact_admin}>')
                await send_warning_message(message.author, point)
            
            elif point == ban_threshold:
                await message.channel.send(f'{message.author.mention} has been banned for too many warnings.')
                await message.author.send(f'You have been banned because you have too many warnings (7).\nYou can contact an administrator if you want to complain about your ban.\n\nContact <@{contact_admin}>')
                await message.guild.ban(message.author, reason="Too many warnings")
                await send_warning_message(message.author, point)

    await bot.process_commands(message)

bot.tree.add_command(add_word)
bot.tree.add_command(delete_word)
bot.tree.add_command(print_warning)
bot.tree.add_command(my_warning)
bot.tree.add_command(clear)
bot.tree.add_command(reset_sanctions_member)
bot.tree.add_command(reset_sanctions)
bot.tree.add_command(reset_history)
bot.tree.add_command(list_banned_words)
bot.tree.add_command(list_sanctions)
bot.tree.add_command(add_role)
bot.tree.add_command(remove_role_command)
bot.tree.add_command(list_roles_command)
bot.tree.add_command(list_commands)

bot.run(token)
