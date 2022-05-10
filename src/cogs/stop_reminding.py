from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command
)
from discord.ext import commands
from dotenv import load_dotenv
import os
import mysql.connector
from discord.utils import get
import random

load_dotenv()
DB_HOST = os.getenv("MYSQLHOST")
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_NAME = os.getenv("MYSQLDATABASE")
PORT = os.getenv("MYSQLPORT")

db = mysql.connector.connect(
    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, port=PORT
)
cursor = db.cursor(buffered=True)

reminder_deleted = [
    "Oh no, why did you delete your reminder T_T",
    "He deleted his reminders :(",
    "Man doesn't want to be reminded anymore?? Is this real??"
        ]

class StopReminding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def stop_reminding(self, ctx):
        """Stops the bot from reminding you about your goals"""
        # write code to check if reminders have been set first
        db.commit()
        delete_reminder_entries = "DELETE FROM reminder WHERE user_id = %s"
        delete_date_reminder_entries = "Delete FROM next_reminder WHERE user_id = %s"
        user = (str(ctx.author.id),)
        cursor.execute(delete_reminder_entries, user)
        cursor.execute(delete_date_reminder_entries, user)
        db.commit()
        await ctx.respond(
            f"{random.choice(reminder_deleted)}\nDo `/remind_me` again to change the interval. If not then we're sad to see you go... all the best"
        )

def setup(bot):
    bot.add_cog(StopReminding(bot))