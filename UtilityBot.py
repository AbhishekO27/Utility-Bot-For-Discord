import discord
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import discord

scheduler = AsyncIOScheduler()

async def send_reminder(ctx, message):
    await ctx.send(message)


@scheduler.scheduled_job('interval', minutes=15)
async def reminder_task():
    await send_reminder(ctx, "Time to walk the dog!")