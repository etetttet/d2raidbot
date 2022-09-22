import discord
from discord import app_commands, Embed
from typing import Optional

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=ID))
        self.synced = True
        print("Bot is ON now")


client = aclient()
tree = app_commands.CommandTree(client)
emoji_kao = "<:kao:1018949565287759884>"
emoji_sub = "<:spare:1020235494182883339>"

@tree.command(name="raid", description="掠奪喊團", guild=discord.Object(id=ID))
@ app_commands.choices(掠奪=[app_commands.Choice(name="國王殞落", value="國王殞落"),
                           app_commands.Choice(name="門徒之誓", value="門徒之誓"),
                           app_commands.Choice(name="玻璃寶庫", value="玻璃寶庫"),
                           app_commands.Choice(name="深石地窖", value="深石地窖"),
                           app_commands.Choice(name="救贖花園", value="救贖花園"),
                           app_commands.Choice(name="最後遺願", value="最後遺願")
                           ])
async def raid(interaction: discord.Interaction,
               掠奪: app_commands.Choice[str],
               時間: str = '滿人就打',
               正選: Optional[str] = None,
               候補: Optional[str] = None,
               備註: Optional[str] = '全通'
               ):
    if interaction.channel.id == CHANNEL:
        formalteam = []
        if 正選 is None:
            formalteam.append(interaction.user.mention)
            slot = 5
            team = ' '.join(formalteam)
        else:
            formalteam.append(interaction.user.mention)
            list = 正選.split()
            formalteam.extend(list)
            slot = 6 - len(formalteam)
            team = ' '.join(formalteam)

        if 候補 is None:
            候補 = ['\u200b']
            sub = ' '.join(候補)
        else:
            候補 = [候補]
            sub = ' '.join(候補)

        raidinfo = Embed(title=interaction.user, color=0x00ff00)
        raidinfo.add_field(name=掠奪.value, value=備註, inline=True)
        raidinfo.add_field(name="空位", value=slot, inline=False)
        raidinfo.add_field(name="時間", value=時間, inline=False)
        raidinfo.add_field(name="人員", value=team, inline=False)
        raidinfo.add_field(name="候補", value=sub, inline=False)
        await interaction.response.send_message(embed=raidinfo)


@ client.event
async def on_message(msg):
    if msg.author == client.user:
        await msg.add_reaction(emoji_kao)
        await msg.add_reaction(emoji_sub)
        await msg.add_reaction("❌")


@ client.event
async def on_raw_reaction_add(payload):

    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = client.get_user(payload.user_id)
    member = payload.member
    total = 6

    def goto_sub(user):
        embed = message.embeds[0]
        embed_to_dict = embed.to_dict()
        for field in embed_to_dict['fields']:
            if field['name'] == '候補':
                if field['value'] == '\u200b':
                    sub = []
                    sub.append(user.mention)
                    field['value'] = ' '.join(sub)
                    dict_to_embed = Embed.from_dict(embed_to_dict)
                    return dict_to_embed
                else:
                    sub = field['value'].split()
                    sub.append(user.mention)
                    field['value'] = ' '.join(sub)
                    dict_to_embed = Embed.from_dict(embed_to_dict)
                    return dict_to_embed

    def teamadd(slot):
        embed = message.embeds[0]
        embed_to_dict = embed.to_dict()
        for field in embed_to_dict['fields']:
            if field['name'] == '空位':
                field['value'] = slot
                slot_to_embed = Embed.from_dict(embed_to_dict)
                return slot_to_embed

    if member == client.user:
        return

    if str(payload.emoji) == "❌":
        embed = message.embeds[0]
        embed_to_dict = embed.to_dict()
        if embed_to_dict['title'] == str(member):
            await message.delete()
        else:
            for field in embed_to_dict['fields']:
                if field['name'] == '人員':
                    fml_remove = field['value'].split()
                    fml_remove.remove(user.mention)
                    if not len(fml_remove) == 0:
                        checkslot = total - len(fml_remove)
                        field['value'] = ' '.join(fml_remove)
                        slot_to_embed = team(checkslot)
                        dict_to_embed = Embed.from_dict(embed_to_dict)
                        await message.edit(embed=dict_to_embed)
                        await message.edit(embed=slot_to_embed)
                    else:
                        field['value'] = '\u200b'
                        slot_to_embed = teamadd(total)
                        dict_to_embed = Embed.from_dict(embed_to_dict)
                        await message.edit(embed=dict_to_embed)
                        await message.edit(embed=slot_to_embed)

    if str(payload.emoji) == emoji_kao:
        embed = message.embeds[0]
        embed_to_dict = embed.to_dict()
        for field in embed_to_dict['fields']:
            if field['name'] == '人員':
                fml_add = field['value'].split()
                if len(fml_add) < 6:
                    if not user.mention in fml_add:
                        if field['value'] == '\u200b':
                            fml_add.append(user.mention)
                            fml_add.remove('\u200b')
                            checkslot = total - len(fml_add)
                            field['value'] = ' '.join(fml_add)
                            dict_to_embed = Embed.from_dict(embed_to_dict)
                            slot_to_embed = teamadd(checkslot)
                            await message.edit(embed=dict_to_embed)
                            await message.edit(embed=slot_to_embed)
                        else:
                            fml_add.append(user.mention)
                            checkslot = total - len(fml_add)
                            field['value'] = ' '.join(fml_add)
                            dict_to_embed = Embed.from_dict(embed_to_dict)
                            slot_to_embed = teamadd(checkslot)
                            await message.edit(embed=dict_to_embed)
                            await message.edit(embed=slot_to_embed)
                    else:
                        pass
                else:
                    pass

    if str(payload.emoji) == emoji_sub:
        dict_to_embed = goto_sub(user)
        await message.edit(embed=dict_to_embed)


@client.event
async def on_raw_reaction_remove(payload):

    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = client.get_user(payload.user_id)
    total = 6

    def teamremove(slot):
        embed = message.embeds[0]
        embed_to_dict = embed.to_dict()
        for field in embed_to_dict['fields']:
            if field['name'] == '空位':
                field['value'] = slot
                slot_to_embed = Embed.from_dict(embed_to_dict)
                return slot_to_embed

    if str(payload.emoji) == emoji_kao:
        embed = message.embeds[0]
        embed_to_dict = embed.to_dict()
        for field in embed_to_dict['fields']:
            if field['name'] == '人員':
                fml_remove = field['value'].split()
                fml_remove.remove(user.mention)
                if not len(fml_remove) == 0:
                    checkslot = total - len(fml_remove)
                    field['value'] = ' '.join(fml_remove)
                    dict_to_embed = Embed.from_dict(embed_to_dict)
                    slot_to_embed = teamremove(checkslot)
                    await message.edit(embed=dict_to_embed)
                    await message.edit(embed=slot_to_embed)
                else:
                    field['value'] = '\u200b'
                    checkslot = total
                    dict_to_embed = Embed.from_dict(embed_to_dict)
                    slot_to_embed = teamremove(checkslot)
                    await message.edit(embed=dict_to_embed)
                    await message.edit(embed=slot_to_embed)

    if str(payload.emoji) == emoji_sub:
        embed = message.embeds[0]
        embed_to_dict = embed.to_dict()
        for field in embed_to_dict['fields']:
            if field['name'] == '候補':
                sub = field['value'].split()
                sub.remove(user.mention)
                if len(sub) == 0:
                    field['value'] = '\u200b'
                    dict_to_embed = Embed.from_dict(embed_to_dict)
                    await message.edit(embed=dict_to_embed)
                else:
                    dict_to_embed = Embed.from_dict(embed_to_dict)
                    await message.edit(embed=dict_to_embed)

client.run(token)
