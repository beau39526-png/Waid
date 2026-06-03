# raid_ephemeral_confirmation.py
# YOUR BOT TOKEN ALREADY INSERTED - READY TO RUN

import discord
from discord import app_commands
from discord.ui import Button, View
import asyncio

# ========== YOUR TOKEN ==========
BOT_TOKEN = "MTUxMTg3MTkyMDY2NzM2MTMyMA.GN7CiQ.yKubdnvNMnFLOT9vuUeyqTRhFMB2uuZC_zp-Vg"

MAX_LEN = 2000

RAID_MSG = ("@everyone **🚨 EXTERNAL BOT RAID 🚨**\n" + "💀 OMNICOMPLY 💀\n" * 66)[:MAX_LEN]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

class RaidConfirm(View):
    def __init__(self, user_id: int, channel_id: int):
        super().__init__(timeout=30)
        self.user_id = user_id
        self.channel_id = channel_id
    
    @discord.ui.button(label="✅ CONFIRM RAID", style=discord.ButtonStyle.danger, emoji="💀")
    async def confirm(self, interaction: discord.Interaction, button: Button):
        # Only the command user can interact
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("❌ Not your raid!", ephemeral=True)
        
        # Ephemeral response (only you see this)
        await interaction.response.send_message("🔥 **RAID EXECUTING...** (messages are public)", ephemeral=True)
        
        # Get channel and send PUBLIC raid messages (everyone sees)
        channel = client.get_channel(self.channel_id)
        
        for i in range(50):
            await channel.send(f"{RAID_MSG} [{i+1}/50]")
            await asyncio.sleep(0.2)
        
        # Send public completion message
        await channel.send("@everyone **💀 RAID COMPLETE - 50 MESSAGES 💀**")
        
        # Disable buttons
        for child in self.children:
            child.disabled = True
        await interaction.edit_original_response(view=self)
    
    @discord.ui.button(label="❌ CANCEL", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("❌ Not your raid!", ephemeral=True)
        
        # Ephemeral cancellation (only you see)
        await interaction.response.send_message("❌ **Raid cancelled**", ephemeral=True)
        
        for child in self.children:
            child.disabled = True
        await interaction.edit_original_response(view=self)

@tree.command(name="raid", description="⚠️ RAID THIS SERVER (Admin only)")
@app_commands.default_permissions(administrator=True)
async def raid(interaction: discord.Interaction):
    # EPHEMERAL = Only YOU can see this confirmation message and buttons
    embed = discord.Embed(
        title="💀 **RAID CONFIRMATION** 💀",
        description="⚠️ This will send **50 max-length messages**\n⚠️ @everyone ping on every message\n⚠️ **Messages will be PUBLIC**\n\n**Confirm or Cancel**",
        color=0xFF0000
    )
    # ephemeral=True makes this visible ONLY to you
    await interaction.response.send_message(embed=embed, view=RaidConfirm(interaction.user.id, interaction.channel_id), ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot online: {client.user}")
    print(f"✅ /raid command ready (ephemeral confirmation)")
    print(f"✅ Invite link: https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot%20applications.commands")

client.run(BOT_TOKEN)
