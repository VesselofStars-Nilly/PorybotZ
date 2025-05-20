import discord
import random
from asyncio import sleep
from discord.ext import tasks, commands


class Bot(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
# Guild ID, Change the default
guildID = int(input("Enter guild ID: "))
print(guildID)



intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Counters
with open("counters.json", "r") as f:
    counters = f.readlines()



async def play_sound():
    # Counters
    global counters
    global guildID

    # Wait
    async def vc_playing():
        while vc.is_playing():
            await sleep(.1)


    guild = bot.get_guild(guildID)
    channels = guild.voice_channels

    # Choosing a channel to join
    clist = []
    for c, i in enumerate(channels):
        mlist = channels[c].members
        if len(mlist) >= 1:
            clist.append(i)

    channel = random.choice(clist)
    vc = await channel.connect()
    clist = []
    print(clist)

    # Shiny
    if random.randint(1, 4095) == 1:
        vc.play(discord.FFmpegOpusAudio('shiny.mp3'))
        await vc_playing()
        counters[1] = str(int(counters[1].strip()) + 1) + "\n"

    # Audio
    vc.play(discord.FFmpegOpusAudio('porygon_z_cry.mp3'))
    await vc_playing()
    vc.play(discord.FFmpegOpusAudio('ability.mp3'))
    await vc_playing()
    vc.play(discord.FFmpegOpusAudio('stats_up.mp3'))
    await vc_playing()
    vc.play(discord.FFmpegOpusAudio('hyper_beam.mp3'))
    await vc_playing()

    # Counters
    counters[0] = str(int(counters[0].strip()) + 1) + "\n"
    with open("counters.json", "w") as f:
        f.writelines(counters)

    await vc.disconnect()



# 1/10 chance to join vc
@tasks.loop(hours=1)
async def hourly():
    rando = random.randrange(9)
    print(rando)
    if rando == 7:
        await play_sound()
    else:
        return


# Startup
@bot.event
async def on_ready():
    force = input("Force run? y/n: ")
    if force == "y":
        await play_sound()
    hourly.start()


@bot.listen("on_message")
async def on_message(message):
    randod = random.randrange(586)
    user = message.author
    if user.bot:
        return
    if randod == 8:
        await user.send(f"+6 252+ SpA Choice Specs Galvanize Tera Electric Porygon-Z Helping Hand Battery boosted Power Spot boosted Hyper Beam over 5 turns vs. -6 Lvl 1 0 HP 0 IVs / 0- SpD 0 IVs {user} in Electric Terrain: 133400-253320 (13340000 - 25332000%) -- guaranteed KO in 5 turns after Stealth Rock and Leech Seed damage", file=discord.File("hyper_beam.mp3"))
        print(user)




# Check joins/shinies
@bot.command()
async def joincount(ctx):
    with open("counters.json") as f:
        count = f.readlines()
    await ctx.send("Joins: " + count[0] + "\n" + "Shinies: " + count[1])


# Token
bot.run('')