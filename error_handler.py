import discord
from discord import app_commands


async def error_handler(*, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
    """
    This function handles errors that occur during the execution of app commands.
    :param interaction: The interaction object.
    :param error: The error object.
    """
    # Defer the response to allow for a longer processing time
    # and to prevent the interaction from timing out.
    # This is an ephemeral response, meaning it will only be visible to the user who triggered the interaction.
    await interaction.response.defer(ephemeral=True)

    # Default error message
    title: str = "An error occurred while processing your request."
    text: str = "Sorry, an error occurred while processing your request."

    # Check if the error is a known error
    if isinstance(error, app_commands.CommandNotFound):
        text = "The command you tried to use does not exist."
    elif isinstance(error, app_commands.MissingPermissions):
        text = "You don't have permission to use this command."
    elif isinstance(error, app_commands.BotMissingPermissions):
        text = "You don't have permission to use this command."
    elif isinstance(error, app_commands.CommandOnCooldown):
        text = f"This command is on cooldown. Please try again in {error.retry_after:.2f} seconds."

    # Create an embed with the error message
    embed: discord.Embed = discord.Embed(title=title, description=text, color=discord.Color.red())
    embed.set_footer(text="If the problem persists, please contact support or your server administrator.")
    embed.timestamp = discord.utils.utcnow()

    # Send the embed as a response to the interaction
    await interaction.followup.send(embed=embed)