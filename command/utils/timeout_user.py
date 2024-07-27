from datetime import timedelta
import asyncio

async def timeout_user(member, duration):
    try:
        await member.timeout(timedelta(seconds=duration))
        print(f"{member.name} has been timed out for {duration} seconds.")

        await asyncio.sleep(duration)

    except discord.Forbidden:
        print(f"Could not send a DM to {member.name}. They might have DMs disabled.")
    except discord.HTTPException as e:
        print(f"Failed to timeout {member.name}: {e}")