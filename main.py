
import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

STAFF_CHANNEL_ID = 1381270661472718980
BOTAO_CHANNEL_ID = 1338540925701455893
VERIFICATION_CHANNEL_ID = 1338540925701455893

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f"🤖 Bot conectado como {bot.user}")
    canal = bot.get_channel(BOTAO_CHANNEL_ID)
    if canal:
        view = CargoView()
        await canal.send("🎮 Clique em um botão para solicitar seu cargo:", view=view)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == VERIFICATION_CHANNEL_ID and str(payload.emoji.name) == "✅":
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member and not member.bot:
            staff_channel = bot.get_channel(STAFF_CHANNEL_ID)
            if staff_channel:
                await staff_channel.send(
                    f"👋 {member.mention} clicou em ✅. Por favor, revise e dê o cargo manualmente."
                )

class CargoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="R1", style=discord.ButtonStyle.primary)
    async def r1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.notificar_staff(interaction, "R1")

    @discord.ui.button(label="R2", style=discord.ButtonStyle.primary)
    async def r2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.notificar_staff(interaction, "R2")

    @discord.ui.button(label="R3", style=discord.ButtonStyle.success)
    async def r3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.notificar_staff(interaction, "R3")

    @discord.ui.button(label="R4", style=discord.ButtonStyle.success)
    async def r4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.notificar_staff(interaction, "R4")

    async def notificar_staff(self, interaction, cargo):
        membro = interaction.user
        staff_channel = bot.get_channel(STAFF_CHANNEL_ID)
        await interaction.response.send_message(
            f"✅ Solicitação para `{cargo}` enviada. Aguarde a staff.",
            ephemeral=True
        )
        if staff_channel:
            await staff_channel.send(f"📩 {membro.mention} solicitou o cargo `{cargo}`.")

keep_alive()
bot.run(os.getenv("BOT_TOKEN"))
