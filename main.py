import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(verbose=True)

# Getting the guild ID from the environment variable
GUILD_ID: discord.Object|None = discord.Object(id=os.getenv("GUILD_ID")) if os.getenv("PYTHON_ENV") == "dev" else None

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            synced: list[discord.app_commands.AppCommand] = await self.tree.sync(guild=GUILD_ID)
            display_id: int|str = GUILD_ID.id if GUILD_ID else "global"
            print(f'Synced {len(synced)} commands to guild {display_id}')

        except Exception as e:
            print(f'Error syncing commands: {e}')

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if message.content.startswith('hello'):
            await message.channel.send(f'Hi there {message.author} : {message.author.mention}')

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        await reaction.message.channel.send(f'{user} reacted using {reaction.emoji}')

# Define the intents and create the client
intents = discord.Intents.default()
intents.message_content = True
client: Client = Client(command_prefix="!", intents=intents)

@client.tree.command(name="hello", description="Say hello", guild=GUILD_ID)
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}")

@client.tree.command(name="printer", description="Whatever you want, I'll print it", guild=GUILD_ID)
async def printer(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

@client.tree.command(name="embed", description="Embed demo", guild=GUILD_ID)
async def embed_demo(interaction: discord.Interaction):
    embed: discord.Embed = discord.Embed(title="I am a title", url="https://www.crunchyroll.com/fr/series/GQWH0M1J3/to-be-hero-x", description="I am a description", color=discord.Color.red())
    embed.set_thumbnail(url="https://placebear.com/200/200")
    embed.add_field(name="Field 1 title", value="Here comes something", inline=False)
    embed.add_field(name="Field 2 title", value="Value 2", inline=True)
    embed.add_field(name="Field 3 title", value="Value 3", inline=True)
    embed.set_footer(text="I am a footer")
    embed.set_author(name=interaction.user.name, url="https://placebear.com", icon_url="https://placebear.com/150/150")
    await interaction.response.send_message(embed=embed)

class View(discord.ui.View):
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.blurple, emoji="🙏")
    async def button_callback_1(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_message("You clicked me!")

    @discord.ui.button(label="I'm a button", style=discord.ButtonStyle.red, emoji="🔥")
    async def button_callback_2(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_message("You burn your finger")

    @discord.ui.button(label="Don't click me", style=discord.ButtonStyle.secondary)
    async def button_callback_3(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_message("Why did you do that")

@client.tree.command(name="buttons", description="Displaying some buttons", guild=GUILD_ID)
async def display_buttons(interaction: discord.Interaction):
    await interaction.response.send_message(view=View())

# Run the bot
client.run(os.getenv('BOT_TOKEN'))