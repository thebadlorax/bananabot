import os
from urllib import parse
from uuid import uuid4
import io

import discord
import requests
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(
  name="avatar",
  description="get the avatar of a person (or banana)"
)
async def avatar_cmd(interaction, target: discord.User, public: bool):
  if public:
    await interaction.response.send_message(target.display_avatar.url)
  else:
    await interaction.response.send_message(target.display_avatar.url, ephemeral=True)

@tree.command(
  name="leave",
  description="make the bot leave the current voice channel"
)
async def leave_cmd(interaction):
    voice_client = interaction.guild.voice_client
    if voice_client:
        await voice_client.disconnect()
        await interaction.response.send_message("Left the voice channel", ephemeral=True)
    else:
        await interaction.response.send_message("I am not in a voice channel currently", ephemeral=True)

@tree.command(
  name="join",
  description="join the vc"
)
async def join_cmd(interaction):
    voice_client = interaction.user.voice.channel
    if voice_client:
        await voice_client.connect()
        await interaction.response.send_message("Joined the vc", ephemeral=True)
    else:
        await interaction.response.send_message("You need to be in a voice channel to use this command", ephemeral=True)

@tree.command(
  name="delete-channels",
  description="iykyk"
)
async def nuker(interaction, password: str):
  if password == str(len(interaction.guild.channels)):
    for channel in interaction.guild.channels:
      await channel.delete()
  else:
    await interaction.response.send_message("Incorrect password", ephemeral=True)

@tree.command(
  name="random-img",
  description="get a random image"
)
async def imagecmd(interaction):
  url = "https://picsum.photos/370/250"
  response = requests.get(url)
  extension = os.path.splitext(parse.urlsplit(response.url).path)[-1]
  image_name = f'{uuid4()}{extension}'
  path = f'images/{image_name}'
  with open(path, mode='wb') as f:
      f.write(response.content)
  await interaction.response.send_message(file=discord.File(path))
  os.remove(path)

"""
@tree.command(
  name="join",
  description="join the sender's voice channel"
)
async def join_cmd(interaction, url: str):
    voice_state = interaction.user.voice
    if not voice_state:
        await interaction.response.send_message("You have to be in a voice channel to use this command!", ephemeral=True)
        return
    voice_channel = voice_state.channel
    if voice_channel:
        voice_client = await voice_channel.connect()
""" # wip

@tree.command(
  name="spam-channel",
  description="spam a channel"
)
async def channelspammer(interaction, message: str, channel: discord.TextChannel, amount: int):
  if amount <= 10:
    for x in range(amount):
      await channel.send(message)
  else:
    await interaction.response.send_message("You can't spam more than 10 times!", ephemeral=True)

@tree.command(
  name="brainfu__",
  description="evaluate Brainfu** code"
)
async def evalbrainfu_cmd(interaction, code: str):
    memory = [0] * 30000
    code = ''.join(filter(lambda x: x in ['<', '>', '+', '-', '.', ',', '[', ']'], code))
    code_ptr = 0
    memory_ptr = 0
    output = ""

    while code_ptr < len(code):
        command = code[code_ptr]

        if command == '>':
            memory_ptr = (memory_ptr + 1) % 30000
        elif command == '<':
            memory_ptr = (memory_ptr - 1) % 30000
        elif command == '+':
            memory[memory_ptr] = (memory[memory_ptr] + 1) % 256
        elif command == '-':
            memory[memory_ptr] = (memory[memory_ptr] - 1) % 256
        elif command == '.':
            output += chr(memory[memory_ptr])
        elif command == ',':
            # Implementation needed to handle input if required
            pass
        elif command == '[' and memory[memory_ptr] == 0:
            loop_count = 1
            while loop_count != 0:
                code_ptr += 1
                if code[code_ptr] == '[':
                    loop_count += 1
                elif code[code_ptr] == ']':
                    loop_count -= 1
        elif command == ']' and memory[memory_ptr] != 0:
            loop_count = 1
            while loop_count != 0:
                code_ptr -= 1
                if code[code_ptr] == ']':
                    loop_count += 1
                elif code[code_ptr] == '[':
                    loop_count -= 1

        code_ptr += 1

    await interaction.response.send_message(output)
    return


@tree.command(
  name="reverse",
  description="reverse a message"
)
async def reverse_cmd(interaction, message: str):
  await interaction.response.send_message(message[::-1])

@tree.command(
  name="spam",
  description="spam someone in their dms >:)"
)
async def spam(interaction, target: discord.User, message: str, times: int):
  if times <= 10:
    await interaction.response.send_message("messages sent", ephmeral=True)
    channel = await target.create_dm()
    for x in range(times):
      await channel.send(str(x+1) + ": " + message)
  else:
    await interaction.response.send_message("don't be too evil son. i can't spam that many times", ephmeral=True)

@tree.command(
  name="impersonate",
  description="impersonate a person ( steal their skin >:} )"
)
async def impersonate(interaction, target: discord.User, message: str):
  webhook = await interaction.channel.create_webhook(name=target.name)
  await webhook.send(
      str(message), username=target.display_name, avatar_url=target.display_avatar.url)

  webhooks = await interaction.channel.webhooks()
  for webhook in webhooks:
          await webhook.delete()
  await interaction.response.send_message(target.mention + " just got pwned", ephemeral=True)

@tree.command(
  name="reset",
  description="debug idk reset the bot"
)
async def reset(interaction):
  with open("bananacat.jpeg", 'rb') as image:
    await client.user.edit(avatar=image.read())
  #await client.user.edit(username="bananabot") # 24h cooldown :skull:
  await interaction.guild.me.edit(nick="bananabot")
  await interaction.response.send_message("reset worked", ephemeral=True)

@tree.command(
  name="nick",
  description="nick the bot"
)
async def nickme(interaction, name: str):
  await interaction.guild.me.edit(nick=name)
  await interaction.response.send_message("nick worked", ephemeral=True)

@tree.command(
  name="pfpnick",
  description="steal the pfp of a person"
)
async def pfpnickme(interaction, user: discord.User):
  data = requests.get(user.display_avatar.url).content
  await interaction.response.send_message("pfp nick worked :)")
  await client.user.edit(avatar=data)

@tree.command(
  name="transform",
  description="steal the pfp of a person and change the nickname"
)
async def transform(interaction, user: discord.User):
  data = requests.get(user.display_avatar.url).content
  await client.user.edit(avatar=data)
  await interaction.guild.me.edit(nick=user.display_name)
  await interaction.response.send_message("transformed into " + user.mention + ". Use /reset to go back!", ephemeral=True)

@tree.command(
  name="speak",
  description="say something (works well with /transform)"
)
async def speak(interaction, msg: str):
  await interaction.channel.send(msg)
  await interaction.response.send_message("message sent", ephemeral=True)


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

my_secret = os.environ['DISCORD_BOT_SECRET']
client.run(my_secret)