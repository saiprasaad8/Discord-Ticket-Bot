"""
Discord Ticket-bot
Author: Sai Prasaad
"""
import discord
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.default()
intents.message_content = True  
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

SUPPORT_ROLE = "ROLE_NAME"  # Replace it with your support role name. It is case sensitive!

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="🎫 Create Ticket",
        style=discord.ButtonStyle.green,
        custom_id="persistent_create_ticket"
    )
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        author = interaction.user
        channel_name = f"ticket-{author.name}".lower().replace(" ", "-")

        # Checking duplicate tickets
        if discord.utils.get(guild.text_channels, name=channel_name):
            await interaction.response.send_message("You already have a ticket open.", ephemeral=True)
            return

        # Setting  permissions
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        support_role = get(guild.roles, name=SUPPORT_ROLE)
        if support_role:
            overwrites[support_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        else:
            await interaction.response.send_message("'Ticket support' role not found.", ephemeral=True)
            return

        # Creating private ticket channel
        ticket_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
        await ticket_channel.send(f"Hello {author.mention}, a staff member will be with you shortly.\nUse `!close` to close this ticket.")

        await interaction.response.send_message(
            f"Your ticket has been created: {ticket_channel.mention}",
            ephemeral=True
        )

@bot.command()
async def ticketpanel(ctx):
    embed = discord.Embed(
        title="Need Support?",
        description="Click the button below to create a ticket.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, view=TicketView())

@bot.command()
@commands.has_role(SUPPORT_ROLE)
async def close(ctx):
    await ctx.send("Closing this ticket...")
    await ctx.channel.delete()

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    bot.add_view(TicketView())
    print(f"🤖 Logged in as {bot.user}")


bot.run("Add_your_Token_Here") # Replace it with your bot's token
