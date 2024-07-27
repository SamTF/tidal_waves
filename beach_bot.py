###### IMPORTS          ##########################################################
# discord.py
import discord
from discord.ext import commands, tasks
from discord import app_commands

# standard library
from typing import Literal
from datetime import datetime, timedelta, time
import pickle

# My modules
import img_getter
from spots import Spot, SPOTS
from weather import get_weather
from weather import weather_codes
from image_generation.pill import create_image

###### CONSTANTS        ##########################################################
TOKEN_FILE = '.bot.token'
DATA = []


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

    # Get current month and year as 0724
    current_date = datetime.now()
    f_date = current_date.strftime("%m%y")

    global DATA

    # Read the tidal data from all pickle files
    for i in range(0, 6):
        with open(f'data/tides_{f_date}_{i}.pickle', 'rb') as file:
            DATA.append(pickle.load(file))

    # global DATA
    # with open('data.pkl', 'rb') as file:
    #     DATA = pickle.load(file)

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
    app_commands.Choice(name='Comporta', value='5'),
])
@app_commands.describe(time_period = 'Check for tides how far out? 🏄')
@app_commands.choices(time_period=[
    app_commands.Choice(name='today', value='today'),
    app_commands.Choice(name='tomorrow', value='tomorrow'),
    app_commands.Choice(name='weekly', value='weekly'),
])
@app_commands.guilds(discord.Object(id=349267379991347200))
async def tides(ctx, spot:app_commands.Choice[str], time_period:app_commands.Choice[str], type: Literal['image', 'message', 'embed']) -> None:
    '''
    Displays tidal information for the requested period of time.
    '''
    print(f'>>> Requesting tides at {spot.name} for {time_period.value} by [{ctx.author.name}]')

    # get dates
    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    # init vars
    days = []
    msg = ''
    data = DATA[int(spot.value)]
    spot_object = SPOTS[int(spot.value)]

    # get data
    match time_period.value:
        case 'today':
            days = [d for d in data if (d.datetime == today)]
            msg = f'Here are the tides at __{spot.name}__ today, dude 😎\n'

        case 'tomorrow':
            days = [d for d in data if (d.datetime == tomorrow)]
            msg = f'This is what the waves are gonna look like __tomorrow at {spot.name}__, dude 🤙\n'

        case 'weekly':
            days = [d for d in data if (d.datetime - today).days <= 7]
            msg = 'Look at all those waves, bro 🌊\n'

        case _:
            days = [d for d in data if (d.datetime == today)]
            msg = 'Here are the tides today\n'
    
    for d in days:
        formatted_date = d.datetime.strftime("%-d/%-m")
        msg += f"\n**__{d.weekday}__**__ ({formatted_date}):__\n"

        for t in d.tides:
            icon = '🌊' if t.tide == True else '🏖️'
            bold = '**' if t.tide == False else ''
            msg += f"{icon}  {bold}{t.time}{bold}  ({t.height})\n"


    # Add extra information if not weekly
    if time_period.value != 'weekly':
        # information for today
        if time_period.value == 'today':
            print('TODAY')
            temp, wwo_code = get_weather.current_weather(spot_object.coordinates)
            print(wwo_code)
            full_date = f"TODAY | {today.strftime('%-d %B')}"
            text = '\n\nCurrent weather:'

        # information for tomorrow
        elif time_period.value == 'tomorrow':
            temp, wwo_code = get_weather.tomorrow_weather(spot_object.coordinates)
            full_date = f"TOMORROW | {tomorrow.strftime('%-d %B')}"
            text = '\n\nWeather forecast:'

        # formatting data
        conditions = weather_codes.WWO_CODE[wwo_code]
        weather_icon = weather_codes.WEATHER_SYMBOL[conditions]
        msg += f'{text} **{temp}ºC** // {conditions} {weather_icon}'
    
    # log print
    print(msg)

    # Check for return type
    # Normal message
    if type == 'message' and time_period.value != 'weekly':
        await ctx.reply(msg)
        # return
    
    # Generate Image
    if type == 'image' and time_period.value != 'weekly':
        # get tides occuring during the day        
        high_tide, low_tide = days[0].daytime_tides()

        image = create_image(
            full_date,
            spot.name,
            { 'time' : high_tide.datetime, 'height' : high_tide.height[:-1] },
            { 'time' : low_tide.datetime, 'height' : low_tide.height[:-1] },
            temp if temp else None,
            wwo_code,
            time_period.value == 'today',
            True
        )
        image.seek(0)
        
        await ctx.send(file=discord.File(image, 'tide_report.png'))
    
    # Send embed
    else:
        # format data fetched as an embed
        embed = discord.Embed(
            title=f'{spot.name}',
            description=msg,
            colour=0x2596be,
            url=spot_object.url
        )
        embed.set_thumbnail(url=img_getter.get_thumb(spot.name))
        embed.set_image(url=img_getter.get_img(spot.name))

        # send the embed
        await ctx.send(embed = embed)

###### RUNNING THE BOT #################################################
if __name__ == "__main__":
    print("_____________BEACH BUDDY INITIALISED_____________")

    with open(TOKEN_FILE, 'r') as f:
        token = f.read()
    
    bot.run(token)
                              