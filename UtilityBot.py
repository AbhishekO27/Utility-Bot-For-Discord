import discord
from discord.ext import commands
import cohere
import requests
import replicate

from dotenv import load_dotenv
import os

load_dotenv()



discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")


cohere_api_key = os.getenv("COHERE_API_KEY")
cohere_client = cohere.Client(cohere_api_key)




replicate_api = os.getenv("REPLICATE_API_KEY")
client = replicate.Client(api_token=replicate_api)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")

@bot.command()
async def image(ctx, *, prompt: str):
    await ctx.send("Generating your image... Please wait!")
    
    try:
        
        model_id = "stability-ai/stable-diffusion" 

        
        print(f"Prompt: {prompt}")
        print(f"Model: {model_id}")

        
        prediction = client.run(
            model_id,
            input={"prompt": prompt}
        )

        
        print(f"Prediction Response: {prediction}")

        
        if "output" in prediction:
            await ctx.send(f"Here's your generated image:\n{prediction['output'][0]}")
        else:
            await ctx.send("No output received from the model.")

    except replicate.exceptions.ReplicateError as e:
        
        print(f"ReplicateError: {e}")
        await ctx.send(f"An error occurred while generating the image: {e}")
    except Exception as e:
       
        print(f"Unexpected Error: {e}")
        await ctx.send(f"An unexpected error occurred: {e}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        user_input = message.content.replace(f"<@{bot.user.id}>", "").strip()
        if not user_input:
            await message.channel.send("How can I assist you?")
            return

        try:
           
            response = cohere_client.generate(
                model="command-xlarge-nightly",
                prompt=user_input,
                max_tokens=300,
                temperature=0.7,
            )
            await message.channel.send(response.generations[0].text.strip())
        except Exception as e:
            await message.channel.send(f"An error occurred while processing your request: {e}")
            print(e)

    await bot.process_commands(message)


@bot.command()
async def weather(ctx, *, city: str):
    """Fetch weather for a given city."""
    try:
        api_key = os.getenv("WEATHER_API")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()

        if response.get("cod") != 200:
            await ctx.send(f"City '{city}' not found.")
            return

        weather_desc = response["weather"][0]["description"]
        temp = response["main"]["temp"]
        feels_like = response["main"]["feels_like"]
        humidity = response["main"]["humidity"]

        weather_report = (
            f"**Weather in {city.title()}:**\n"
            f"Description: {weather_desc.capitalize()}\n"
            f"Temperature: {temp}°C (Feels like {feels_like}°C)\n"
            f"Humidity: {humidity}%"
        )
        await ctx.send(weather_report)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


bot.run(discord_bot_token)

