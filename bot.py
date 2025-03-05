import discord
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Token dan API Key
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Setup Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Setup Discord Client
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot sudah online sebagai {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!tanya'):
        question = message.content[7:].strip()

        try:
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(question)

            # Ambil teks hasil dari response
            response_text = response.candidates[0].content.parts[0].text

            # Kirim pakai handler khusus untuk pesan panjang
            await send_long_message(message.channel, response_text)

        except Exception as e:
            await message.channel.send(f"Terjadi kesalahan: {e}")

async def send_long_message(channel, message):
    while message:
        part = message[:2000]
        message = message[2000:]
        await channel.send(part)


client.run(DISCORD_TOKEN)
