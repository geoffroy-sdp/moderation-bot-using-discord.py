from datetime import datetime, timezone

def is_alt_account(bot, member):
    """Heuristic to determine if a member is an alt account based on activity history."""
    
    reasons = []
    
    account_created_at = member.created_at.astimezone(timezone.utc)

    now = datetime.now(timezone.utc)

    account_age = (now - account_created_at).days
    if account_age < 30: 
        reasons.append(f"Account age is {account_age} days (less than 30 days)")

    user_guilds = [guild for guild in bot.guilds if member in guild.members]
    if len(user_guilds) < 2:
        reasons.append(f"User is in {len(user_guilds)} server(s) (less than 2)")
    
    if reasons:
        return True, reasons
    return False, []
