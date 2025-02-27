# /bot/commands/ping.py
from bot.config import Config, Embed
from bot.base import Command
from asyncio import sleep
from re import match
import time

class cmd(Command):
    """ A discord command instance. """

    name = "remind"
    usage = "remind <time> <*reminder>"
    description = """Reminds the user of something.
    The time is formatted with: 1d2h10m5s for 1 day, 2 hours, etc. You can also just use 2h for 2 hours."""

    async def execute(self, arguments, message) -> None:
        timeStr = arguments[0]
        regEx = r"(?:(?P<days>\d+)d)?(?:(?P<hours>\d+)h)?(?:(?P<minutes>\d+)m)?(?:(?P<seconds>\d+)s)?"
        times = match(regEx, timeStr).groupdict()
        d = int(times["days"]) if times["days"] else 0
        h = int(times["hours"]) if times["hours"] else 0
        m = int(times["minutes"]) if times["minutes"] else 0
        s = int(times["seconds"]) if times["seconds"] else 0
        reminderTime = d * 24 * 3600 + h * 3600 + m * 60 + s
        timestamp = int(time.time()) + reminderTime
        
        embed = Embed(title="New Reminder", description=f"Reminder set to <t:{timestamp}:f>, wich is in <t:{timestamp}:R>.")
        msg = await message.reply(embed=embed)
        url = msg.jump_url
        await sleep(reminderTime)
        embed = Embed(title=arguments[1], description=f"""This is your reminder.
        If you wan't to know the context, [here]({url}) is the link.""")
        await message.channel.send(f"<@{message.author.id}>", embed=embed)
