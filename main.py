from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
import os

app = Flask('')

@app.route('/')
def home():
    return "Bot is online!"

def run():
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

class SignalNumberModal(discord.ui.Modal, title="Επιλογή Σήματος (1-120)"):
    signal_id = discord.ui.TextInput(label="Αριθμός Σήματος", placeholder="1 έως 120...", style=discord.TextStyle.short, min_length=1, max_length=3)
    async def on_submit(self, interaction: discord.Interaction):
        try:
            val = int(self.signal_id.value)
            if 1 <= val <= 120:
                embed = discord.Embed(title="🚨 Ανάληψη Σήματος ΕΚΑΒ", description=f"Ο χρήστης **{interaction.user.mention}** ανέλαβε το **Σήμα #{val}**.", color=discord.Color.blue())
                await interaction.response.send_message(embed=embed, ephemeral=False)
            else:
                await interaction.response.send_message("❌ Πρέπει να είναι μεταξύ **1 και 120**!", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Μη έγκυρος αριθμός!", ephemeral=True)

class SignalsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Available Σήματα", style=discord.ButtonStyle.secondary, emoji="📋", custom_id="ekab_available_signals")
    async def available_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=discord.Embed(title="📋 Σήματα (1-120)", description="Τα 1-10 είναι reserved.", color=discord.Color.orange()), ephemeral=True)
    @discord.ui.button(label="Παίρνω Σήμα", style=discord.ButtonStyle.primary, emoji="🚨", custom_id="ekab_take_signal")
    async def take_signal_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SignalNumberModal())

class ElementiModal(discord.ui.Modal, title="Δήλωση Στοιχείων - ΕΚΑΒ"):
    steam_name = discord.ui.TextInput(label="Steam Name", placeholder="John_Doe", style=discord.TextStyle.short)
    character_name = discord.ui.TextInput(label="In-Game Όνομα", placeholder="Γιάννης...", style=discord.TextStyle.short)
    vathmos_klimakio = discord.ui.TextInput(label="Βαθμός & Κλιμάκιο", placeholder="Διευθυντής...", style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="🪪 Νέα Στοιχεία Υπαλλήλου", color=discord.Color.gold())
        embed.add_field(name="Steam Name", value=self.steam_name.value, inline=False)
        embed.add_field(name="In-Game Όνομα", value=self.character_name.value, inline=False)
        embed.add_field(name="Βαθμός / Κλιμάκιο", value=self.vathmos_klimakio.value, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=False)

class ElementiView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Στοιχεία Υπαλλήλου", style=discord.ButtonStyle.primary, emoji="🪪", custom_id="ekab_elements_button")
    async def elements_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ElementiModal())

class AbsencesModal(discord.ui.Modal, title="Αίτηση Απουσίας - ΕΚΑΒ"):
    dates = discord.ui.TextInput(label="Ημερομηνίες", placeholder="Από... έως...", style=discord.TextStyle.short)
    reason = discord.ui.TextInput(label="Λόγος", placeholder="Λόγοι...", style=discord.TextStyle.paragraph)
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="📅 Νέα Αίτηση Απουσίας", description=f"Από {interaction.user.mention}", color=discord.Color.purple())
        embed.add_field(name="Ημερομηνίες", value=self.dates.value, inline=False)
        embed.add_field(name="Λόγος", value=self.reason.value, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=False)

class AbsencesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Αίτηση Απουσίας", style=discord.ButtonStyle.secondary, emoji="📅", custom_id="ekab_absence_button")
    async def absence_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AbsencesModal())

class DutyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="On Duty", style=discord.ButtonStyle.success, emoji="🟢", custom_id="ekab_on_duty")
    async def on_duty_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=discord.Embed(title="🟢 On Duty", description=f"{interaction.user.mention} On Duty.", color=discord.Color.green()), ephemeral=False)
    @discord.ui.button(label="Off Duty", style=discord.ButtonStyle.danger, emoji="🔴", custom_id="ekab_off_duty")
    async def off_duty_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=discord.Embed(title="🔴 Off Duty", description=f"{interaction.user.mention} Off Duty.", color=discord.Color.dark_red()), ephemeral=False)
    @discord.ui.button(label="Προσωπικός Χρόνος", style=discord.ButtonStyle.secondary, emoji="⏱️", custom_id="ekab_personal_time")
    async def personal_time_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=discord.Embed(title="⏱️ Χρόνος", description="0 ώρες", color=discord.Color.blue()), ephemeral=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}!')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ekab(ctx):
    await ctx.send(embed=discord.Embed(title="🔴 Σύστημα Παράδοσης Σήματος", color=discord.Color.dark_red()), view=EkabView())

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_signals(ctx):
    await ctx.send(embed=discord.Embed(title="🚨 Σύστημα Σημάτων (1-120)", color=discord.Color.dark_blue()), view=SignalsView())

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_elementi(ctx):
    await ctx.send(embed=discord.Embed(title="🪪 Δήλωση Στοιχείων", color=discord.Color.gold()), view=ElementiView())

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_absences(ctx):
    await ctx.send(embed=discord.Embed(title="📅 Σύστημα Απουσιών", color=discord.Color.purple()), view=AbsencesView())

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_duty(ctx):
    await ctx.send(embed=discord.Embed(title="⏱️ Σύστημα Υπηρεσίας", color=discord.Color.blue()), view=DutyView())

if __name__ == "__main__":
    keep_alive()
    bot.run(os.getenv("DISCORD_TOKEN"))