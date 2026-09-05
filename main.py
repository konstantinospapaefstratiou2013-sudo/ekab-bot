import os
from threading import Thread
import discord
from discord.ext import commands
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "EKAB Bot is alive!"

def run():
    # Παίρνει αυτόματα την πόρτα από το Render (default 8080)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class EkabModal(discord.ui.Modal, title="Σύστημα Παράδοσης Σήματος - ΕΚΑΒ"):
    peristatiko = discord.ui.TextInput(label="Είδος Περιστατικού / Διεύθυνση", placeholder="π.χ. Τροχαίο...", style=discord.TextStyle.short)
    plirofories = discord.ui.TextInput(label="Λεπτομέρειες / Ασθενής", placeholder="π.χ. Τραυματίας...", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="🚑 Νέο Σήμα ΕΚΑΒ Καταχωρήθηκε", color=discord.Color.red())
        embed.add_field(name="Περιστατικό", value=self.peristatiko.value, inline=False)
        embed.add_field(name="Λεπτομέρειες", value=self.plirofories.value, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=False)

class EkabView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Παράδοση Σήματος", style=discord.ButtonStyle.danger, emoji="🚑", custom_id="ekab_paradosi_simatou")
    async def ekab_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EkabModal())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}!')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ekab(ctx):
    await ctx.send(embed=discord.Embed(title="🔴 Σύστημα Παράδοσης Σήματος", color=discord.Color.dark_red()), view=EkabView())

if __name__ == "__main__":
    keep_alive()
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("ERROR: DISCORD_TOKEN is missing!")