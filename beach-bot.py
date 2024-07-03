###### IMPORTS          ##########################################################
import discord
from discord.ext import commands, tasks
from discord import app_commands

from typing import Literal
from datetime import datetime, timedelta
import pickle


###### CONSTANTS        ##########################################################
TOKEN_FILE = '.bot.token'
DATA = ''


###### DISCORD STUFF  ############################################################
### Creating the bot!
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='🌊', intents=intents)

    # on_ready event l think
    async def setup_hook(self) -> None:
        await self.tree.sync(guild=discord.Object(id=349267379991347200))
        print(f'Synced slash commands for {self.user} @ server 349267379991347200')
    
    # error handling
    async def on_command_error(self, ctx, error) -> None:
        await ctx.reply(error, ephemeral=True)

bot = Bot()


###### EVENTS        ##########################################################
# Runs this when the bot becomes online
@bot.event
async def on_ready():
    print("Ready to hang loose dude!")
    print(bot.user.name)

    # Read the tidal data from the pickle file
    global DATA
    with open('data.pkl', 'rb') as file:
        DATA = pickle.load(file)

    await bot.change_presence(activity=discord.Game("🌊 Surfin' the waves 🏖️"))


###### COMMANDS        #######################################################
### /concerts
@bot.hybrid_command(name = 'tides', description = 'Check out all the tidal information in your local beach!')
@app_commands.describe(spot = 'Which beach, dude? 🤙')
@app_commands.choices(spot=[
    app_commands.Choice(name='São Pedro de Moel', value='0'),
    app_commands.Choice(name='Nazaré', value='1'),
    app_commands.Choice(name='Peniche', value='2'),
    app_commands.Choice(name='Ericeira', value='3'),
    app_commands.Choice(name='Cascais', value='4'),
])
@app_commands.describe(time_period = 'Check for tides how far out? 🏄')
@app_commands.choices(time_period=[
    app_commands.Choice(name='today', value='today'),
    app_commands.Choice(name='tomorrow', value='tomorrow'),
    app_commands.Choice(name='weekly', value='weekly'),
])
@app_commands.guilds(discord.Object(id=349267379991347200))
async def tides(ctx, spot:app_commands.Choice[str], time_period:app_commands.Choice[str], fruits: Literal['apple', 'banana', 'cherry']) -> None:
    '''
    Displays tidal information for the requested period of time.
    '''
    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    print(f'>>> Requesting tides at {spot.name} for {time_period.value} by [{ctx.author.name}]')

    days = []
    msg = ''

    match time_period.value:
        case 'today':
            days = [d for d in DATA if (d.datetime == today)]
            msg = f'Here are the tides at __{spot.name}__ today, dude 😎\n\n'

        case 'tomorrow':
            days = [d for d in DATA if (d.datetime == tomorrow)]
            msg = f'This is what the waves are gonna look like __tomorrow at {spot.name}__, dude 🤙\n\n'

        case 'weekly':
            days = [d for d in DATA if (d.datetime - today).days <= 7]
            msg = 'Look at all those waves, bro 🌊\n\n'

        case _:
            days = [d for d in DATA if (d.datetime == today)]
            msg = 'Here are the tides today\n\n'
    
    for d in days:
        formatted_date = d.datetime.strftime("%-d/%-m")
        msg += f"**__{d.weekday}__**__ ({formatted_date}):__\n"

        for t in d.tides:
            icon = '🌊' if t.tide == True else '🏖️'
            bold = '**' if t.tide == False else ''
            msg += f"{icon}  {bold}{t.time}{bold}  ({t.height})\n"

    print(msg)

    await ctx.send(f"{msg}")

###### RUNNING THE BOT #################################################
if __name__ == "__main__":
    print("_____________BEACH BUDDY INITIALISED_____________")

    with open(TOKEN_FILE, 'r') as f:
        token = f.read()
    
    bot.run(token)
                              