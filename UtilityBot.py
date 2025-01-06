import discord
from discord.ext import commands
import cohere
import requests
import replicate

# Discord bot token
DISCORD_BOT_TOKEN =

# Cohere API key
COHERE_API_KEY = 
cohere_client = cohere.Client(COHERE_API_KEY)



REPLICATE_API_KEY = "
client = replicate.Client(api_token=REPLICATE_API_KEY)
# Initialize bot
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
        # Replace with the correct model ID (and version ID if necessary)
        model_id = "stability-ai/stable-diffusion"  # Replace with your model ID
        # Optional: Add version ID if required, e.g., "your-version-id"

        # Debug: Log the prompt and model
        print(f"Prompt: {prompt}")
        print(f"Model: {model_id}")

        # Run the prediction on Replicate
        prediction = client.run(
            model_id,
            input={"prompt": prompt}
        )

        # Debug: Log the prediction response
        print(f"Prediction Response: {prediction}")

        # Send the generated image
        if "output" in prediction:
            await ctx.send(f"Here's your generated image:\n{prediction['output'][0]}")
        else:
            await ctx.send("No output received from the model.")

    except replicate.exceptions.ReplicateError as e:
        # Handle API errors with specific logging
        print(f"ReplicateError: {e}")
        await ctx.send(f"An error occurred while generating the image: {e}")
    except Exception as e:
        # Handle other unexpected errors
        print(f"Unexpected Error: {e}")
        await ctx.send(f"An unexpected error occurred: {e}")

# AI Chat Command
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
            # Send the user's message to Cohere and get a response
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

