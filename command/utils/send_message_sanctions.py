async def send_warning_message(user, current_points):
    embed = discord.Embed(
        title="Warning Received",
        description=f"You have received a warning. You now have **{current_points}** warning(s).",
        color=discord.Color.red()
    )

    embed.add_field(
        name="Potential Future Sanctions",
        value=(
            f"**{mute_threshold} warnings**: Muted for {mute_duration} hours\n"
            f"**{longer_mute_threshold} warnings**: Muted for {longer_mute_duration} hours\n"
            f"**{kick_threshold} warnings**: Kicked from the server\n"
            f"**{warning_before_ban} warnings**: Final warning before ban\n"
            f"**{ban_threshold} warnings**: Permanently banned from the server"
        ),
        inline=False
    )
    
    try:
        await user.send(embed=embed)
    except discord.errors.Forbidden:
        print(f"Cannot send a message to {user.name}")