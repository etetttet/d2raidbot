import discord
from discord import app_commands
import json
from typing import Optional

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=718495741730881586))
        self.synced = True
        print("Bot is ON now")


client = aclient()
tree = app_commands.CommandTree(client)

raidname = str
raidtime = str
formallist = []
sublist = []
slot = 6
caller = str
desc = str

@tree.command(name="raid", description="掠奪喊團", guild=discord.Object(id=1020775231670976523))
@app_commands.choices(掠奪=[
    app_commands.Choice(name="國王殞落", value="國王殞落"),
    app_commands.Choice(name="門徒之誓", value="門徒之誓"),
    app_commands.Choice(name="玻璃寶庫", value="玻璃寶庫"),
    app_commands.Choice(name="深石地窖", value="深石地窖"),
    app_commands.Choice(name="救贖花園", value="救贖花園"),
    app_commands.Choice(name="最後遺願", value="最後遺願")
])
# async def raid(interaction: discord.Interaction,
async def raid(interaction: discord.Interaction,
               掠奪: app_commands.Choice[str],
               時間: str = '滿人就打',
               正選: Optional[str] = None,
               候補: Optional[str] = None,
               備註: Optional[str] = None
               ):
    global raidname
    global raidtime
    global formallist
    global sublist
    global slot
    global caller
    global desc

    raidname = 掠奪.value
    raidtime = 時間
    caller = interaction.user

    if 正選 is None:
        正選 = ''
        formallist.append(caller.mention)
    elif not 正選 is None:
        formallist.append(caller.mention)
        formallist.extend([正選])
    if 候補 is None:
        候補 = ''
        sublist = []
    elif not 候補 is None:
        sublist.append([候補])
    if 備註 is None:
        desc = ''
    elif not 備註 is None:
        desc = 備註
        
    slot = slot - len(formallist)
    await interaction.response.send_message(f"活動: {掠奪.value} -{slot}"'\n'
                                            f"時間: {時間}"'\n'
                                            f"人員: {' '.join(formallist)}"'\n'
                                            f"候補: {' '.join(sublist)}"'\n'
                                            f"備註: {desc}"
                                            )


@client.event
async def on_message(msg):
    if "活動" in msg.content:
        await msg.add_reaction("<:kao:1018949565287759884>")
        await msg.add_reaction("<:spare:1020235494182883339>")
        await msg.add_reaction("❌")


@client.event
async def on_reaction_add(reaction, user):

    global raidname
    global raidtime
    global formallist
    global sublist
    global slot
    global caller
    global desc
    
    if user == client.user:
        return

    channel = await client.fetch_channel('1018958415416021073')
    message = await channel.fetch_message(reaction.message.id)

    if reaction.emoji == "❌":
        if user == caller:
            await message.delete()

    if str(reaction.emoji) == "<:kao:1018949565287759884>":
        slot = slot - 1
        if slot <= 0:
            return
        formallist.extend([user.mention])
        await message.edit(content=f"活動: {raidname} -{slot}"'\n'
                           f"時間: {raidtime}"'\n'
                           f"人員: {' '.join(formallist)}"'\n'
                           f"候補: {' '.join(sublist)}"'\n'
                           f"備註: {desc}"
                           )

    if str(reaction.emoji) == "<:spare:1020235494182883339>":
        slot = slot
        sublist.extend([user.mention])
        await message.edit(content=f"活動: {raidname} -{slot}"'\n'
                           f"時間: {raidtime}"'\n'
                           f"人員: {' '.join(formallist)}"'\n'
                           f"候補: {' '.join(sublist)}"'\n'
                           f"備註: {desc}"
                           )


@client.event
async def on_reaction_remove(reaction, user):

    global raidname
    global raidtime
    global formallist
    global sublist
    global slot
    global desc
    
    if user == client.user:
        return
    channel = await client.fetch_channel('1018958415416021073')
    message = await channel.fetch_message(reaction.message.id)

    if str(reaction.emoji) == "<:kao:1018949565287759884>":
        slot = slot + 1
        formallist.remove(user.mention)
        await message.edit(content=f"活動: {raidname} -{slot}"'\n'
                           f"時間: {raidtime}"'\n'
                           f"人員: {' '.join(formallist)}"'\n'
                           f"候補: {' '.join(sublist)}"'\n'
                           f"備註: {desc}"
                           )

    if str(reaction.emoji) == "<:spare:1020235494182883339>":
        slot = slot
        sublist.remove(user.mention)
        await message.edit(content=f"活動: {raidname} -{slot}"'\n'
                           f"時間: {raidtime}"'\n'
                           f"人員: {' '.join(formallist)}"'\n'
                           f"候補: {' '.join(sublist)}"'\n'
                           f"備註: {desc}"
                           )

client.run(TOKEN)
