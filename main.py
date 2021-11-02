import os
import json
import discord
import random
from discord.ext import commands
from keep_alive import keep_alive
from news import news_page_refresher
from race_table import race_table_updater
from team_standings import team_standings_updater
from driver_standings import driver_standings_updater
from team_page_getter import team_page_getter_details
from driver_page_getter import driver_page_getter_details
from race_result_page_getter import race_result_page_updater
from misc import race_result_page_url_getter, team_page_url_getter, driver_page_url_getter 

bot = commands.Bot(command_prefix='.', intents = discord.Intents.all() , help_command=None)

quotes = [
'''"As a Formula One Driver, you dream about winning your first race all your life. I am desperate to know how it feels like."
~Sergio Perez''',
'''"The satisfaction you have in a few minutes when you become champion, it's enough to live forever."
~Fernando Alonso''',
'''"Sometimes you need to press pause to let everything sink in."
~Sebastian Vettel''',
'''"Sometimes you love the sport, it just don’t love you back."
~Lance Stroll''',
'''"Every day, every year, every new season is a reset from the last, and you are still hungry for success, to do things better and better."
~Fernando Alonso''',
'''"I like to race, not to do laps alone."
~Fernando Alonso''',
'''"I miss winning. I miss being on the podium."
~Fernando Alonso''',
'''"I'm just hungry to win."
~Fernando Alonso''',
'''"You can't always say what you'd like to say."
~Sebastian Vettel''',
'''"You can't change what happened. But you can still change what will happen."
~Sebastian Vettel''',
'''"Simply racing a Formula 1 car is an achievement."
~Sebastian Vettel''',
'''"You're traveling all over the world but to be home is something special."
~Sebastian Vettel''',
'''"Everybody who knows Formula 1 knows McLaren and knows that it is the greatest team in Formula 1."
~Sergio Perez''',
'''"How many points, how many races you can win, how many times you be on the podium. That's the name of the game."
~Valtteri Bottas''',
'''"Of course, when you start in pole, winning is the only target you have."
~Valtteri Bottas''',
'''"I studied to be a car mechanic. That was my plan B. Servicing cars and changing tyres in Finland."
~Valtteri Bottas''',
'''"Prove them wrong."
~Anthoine Hubert''',
'''"The way I drive, the way I handle a car, is an expression of my inner feelings."
~Lewis Hamilton''',
'''"Everyone loves a winner. That's just how the world is. And Ayrton Senna was one of the greatest winners this sport has ever had."
~Lewis Hamilton''',
'''"It's important for everyone to stand up for what they believe in."
~Lewis Hamilton''',
'''"Let's put it this way, I like number seven."
~Michael Schumacher'''
]

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=".help"))
    print('Logged in as ' + bot.user.name)
    print('Ready!\n')

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def races(ctx , year : int = 2021):
    if year > 2021 or year < 1950:
        await ctx.send("The year that you entered is invalid.")   
    
    else:
        race_table_updater(str(year))
        with open("race_table.json" , "r") as f:
            data = json.load(f)
        
        race_count = len(data)

        i = 0

        embed = discord.Embed(title = f"Race Results of {str(year)}" , color = 0xff1801)
            
        while i < race_count:
            venue = data[str(i+1)]['venue']
            date = data[str(i+1)]['date']
            driver = data[str(i+1)]['race_winner'][0]
            team = data[str(i+1)]['race_winner'][1]
            race_winner = f"{driver} - {team}"
            laps = data[str(i+1)]['laps']
            time = data[str(i+1)]['time']
            embed.add_field(name = f"{i + 1}. {venue}" , value = f'''Date: {date}
Winner: {race_winner}
Laps: {laps}
Time: {time}''' , inline = False)
            i += 1

        embed.set_thumbnail(url = "https://www.racecar-engineering.com/wp-content/uploads/2018/03/F1-LOGO.png")
        embed.set_footer(text = "Formula 1")
        await ctx.send(embed = embed)

@bot.command()
async def teams(ctx , year : int = 2021):
    if year > 2021 or year < 1950:
        await ctx.send("The year that you entered is invalid.")   
    elif year < 1959 and year > 1949:
        await ctx.send("The Constructors Championship was not awarded until 1958.")
    else:
        team_standings_updater(year)
        with open("team_standings.json" , "r") as f:
            data = json.load(f)
        
        race_count = len(data)

        i = 0

        embed = discord.Embed(title = f"Team Standings of {year}" , color = 0xff1801)
            
        while i < race_count:
            position = data[str(i+1)]['number']
            team = data[str(i+1)]['team']
            points = data[str(i+1)]['points']
            embed.add_field(name = f"{position}. {team}" , value = f"Points: {points}", inline = False)
            i += 1

        embed.set_thumbnail(url = "https://www.racecar-engineering.com/wp-content/uploads/2018/03/F1-LOGO.png")
        embed.set_footer(text = "Formula 1")
        await ctx.send(embed = embed)

@bot.command()
async def drivers(ctx , year : int = 2021):
    if year > 2021 or year < 1950:
        await ctx.send("The year that you entered is invalid.")   
    
    else:
        driver_standings_updater(year)
        with open("driver_standings.json" , "r") as f:
            data = json.load(f)
        
        race_count = len(data)

        i = 0

        embed = discord.Embed(title = f"Driver Standings of {year}" , color = 0xff1801)
            
        while i < race_count:
            position = data[str(i+1)]['number']
            driver = data[str(i+1)]['driver']
            team = data[str(i+1)]['team']
            points = data[str(i+1)]['points']
            embed.add_field(name = f"{position}. {driver}" , value = f'''Team: {team}
Points: {points}''', inline = False)
            i += 1

        embed.set_thumbnail(url = "https://www.racecar-engineering.com/wp-content/uploads/2018/03/F1-LOGO.png")
        embed.set_footer(text = "Formula 1")
        await ctx.send(embed = embed)

@bot.command()
async def race(ctx , race_no:int = 1 , year:int = 2021):
    URL = race_result_page_url_getter(str(year) , int(race_no))
    race_result_page_updater(URL)
    
    with open("race_result_page_getter.json" , "r") as f:
        data = json.load(f)

    title = data['title']
    date = data['date']
    circuit = data['circuit']

    embed = discord.Embed(title = title , description = f'''{date}
{circuit}''' , color = 0xff1801)

    i = 0
    while i < len(data['drivers']):
        temp = data['drivers'][str(i + 1)]
        embed.add_field(name = f"{temp['position']}. {temp['driver']} - {temp['team']} - {temp['driver_no']}" , value = f'''Laps: {temp['laps']}
Time: {temp['time']}
Points: {temp['points']}''' , inline = False)

        i += 1
    embed.set_thumbnail(url = data['sponsor'])
    embed.set_footer(text = "Formula 1")
    await ctx.send(embed = embed)

@bot.command()
async def team(ctx , team_short = None):
    if team_short == None:
        await ctx.send("You need to send a team's short name for an input.")
    else:
        team_short = team_short.upper()
        if team_short == "MER" or team_short == "RBR" or team_short == "MCL" or team_short == "FER" or team_short == "ALP" or team_short == "ALT" or team_short == "ASM" or team_short == "WIL" or team_short == "ALF" or team_short == "HAS":
            URL = team_page_url_getter(team_short)
            team_page_getter_details(URL)

            with open("images.json" , "r") as f:
                images = json.load(f)

            with open("team_page_getter.json" , "r") as g:
                data = json.load(g)

            embed = discord.Embed(title = data['Full Team Name'] , color = 0xff1801)
            embed.add_field(name = "Base", value = data['Base'], inline = False)
            embed.add_field(name = "Team Chief", value = data['Team Chief'], inline = False)
            embed.add_field(name = "Technical Chief", value = data['Technical Chief'], inline = False)
            embed.add_field(name = "Chassis", value = data['Chassis'], inline = False)
            embed.add_field(name = "Power Unit", value = data['Power Unit'], inline = False)
            embed.add_field(name = "First Team Entry", value = data['First Team Entry'], inline = False)
            embed.add_field(name = "World Championships", value = data['World Championships'], inline = False)
            embed.add_field(name = "Highest Race Finish", value = data['Highest Race Finish'], inline = False)
            embed.add_field(name = "Pole Positions", value = data['Pole Positions'], inline = False)
            embed.add_field(name = "Fastest Laps", value = data['Fastest Laps'], inline = False)
            embed.add_field(name = "Driver: 1", value = f'''Name: {data['drivers']['1']['name']}
Number: {data['drivers']['1']['number']}''', inline = False)
            embed.add_field(name = "Driver: 2", value = f'''Name: {data['drivers']['2']['name']}
Number: {data['drivers']['2']['number']}''', inline = False)

            embed.set_thumbnail(url = images['teams'][team_short])
            embed.set_image(url = images['cars'][team_short])

            await ctx.send(embed = embed)

        else:
            await ctx.send("Please send a correct Team short form. You can use the `.teamshorts` command to find the short form of teams.")

@bot.command()
async def driver(ctx , driver_short = None):
    if driver_short == None:
        await ctx.send("You need to send a driver's short name for an input.")
    else:
        driver_short = driver_short.upper()
        if driver_short == "HAM" or driver_short == "BOT" or driver_short == "VER" or driver_short == "PER" or driver_short == "NOR" or driver_short == "RIC" or driver_short == "SAI" or driver_short == "LEC" or driver_short == "ALO" or driver_short == "OCO" or driver_short == "GAS" or driver_short == "TSU" or driver_short == "VET" or driver_short == "STR" or driver_short == "RUS" or driver_short == "LAT" or driver_short == "RAI" or driver_short == "GIO" or driver_short == "MSC" or driver_short == "MAZ":
            URL = driver_page_url_getter(driver_short)
            driver_page_getter_details(URL)

            with open("images.json" , "r") as f:
                images = json.load(f)

            with open("driver_page_getter.json" , "r") as g:
                data = json.load(g)

            embed = discord.Embed(title = data['Name'] , color = 0xff1801)
            embed.add_field(name = "Car Number", value = data['Number'], inline = False)
            embed.add_field(name = "Team", value = data['Team'], inline = False)
            embed.add_field(name = "Country", value = data['Country'], inline = False)
            embed.add_field(name = "Podiums", value = data['Podiums'], inline = False)
            embed.add_field(name = "Points", value = data['Points'], inline = False)
            embed.add_field(name = "Grands Prix entered", value = data['Grands Prix entered'], inline = False)
            embed.add_field(name = "World Championships", value = data['World Championships'], inline = False)
            embed.add_field(name = "Highest Race Finish", value = data['Highest race finish'], inline = False)
            embed.add_field(name = "Highest Grid Position", value = data['Highest grid position'], inline = False)
            embed.add_field(name = "Date of birth", value = data['Date of birth'], inline = False)
            embed.add_field(name = "Place of birth", value = data['Place of birth'], inline = False)

            embed.set_thumbnail(url = images['helmets'][driver_short])
            embed.set_image(url = images['drivers'][driver_short])

            await ctx.send(embed = embed)

        else:
            await ctx.send("Please send a correct Driver short form. You can use the `.drivershorts` command to find the short form of teams.")

@bot.command()
async def teamshorts(ctx):
    embed = discord.Embed(title = "Teams of 2021" , color = 0xff1801)
    embed.add_field(name = "Mercedes" , value = "MER" , inline = False)
    embed.add_field(name = "Red Bull Racing" , value = "RBR" , inline = False)
    embed.add_field(name = "McLaren" , value = "MCL" , inline = False)
    embed.add_field(name = "Ferrari" , value = "FER" , inline = False)
    embed.add_field(name = "Alpine" , value = "ALP" , inline = False)
    embed.add_field(name = "AlphaTauri" , value = "ALT" , inline = False)
    embed.add_field(name = "Aston Martin" , value = "ASM" , inline = False)
    embed.add_field(name = "Williams" , value = "WIL" , inline = False)
    embed.add_field(name = "Alfa Romeo" , value = "ALF" , inline = False)
    embed.add_field(name = "Haas" , value = "HAS" , inline = False)
    embed.set_thumbnail(url = "https://www.racecar-engineering.com/wp-content/uploads/2018/03/F1-LOGO.png")
    embed.set_footer(text = "Formula 1")
    await ctx.send(embed = embed)

@bot.command()
async def drivershorts(ctx):
    embed = discord.Embed(title = "Drivers of 2021" , color = 0xff1801)
    embed.add_field(name = "Lewis Hamilton" , value = "HAM" , inline = False)
    embed.add_field(name = "Valtteri Bottas" , value = "BOT" , inline = False)
    embed.add_field(name = "Max Verstappen" , value = "VER" , inline = False)
    embed.add_field(name = "Sergio Perez" , value = "PER" , inline = False)
    embed.add_field(name = "Lando Norris" , value = "NOR" , inline = False)
    embed.add_field(name = "Daniel Ricciardo" , value = "RIC" , inline = False)
    embed.add_field(name = "Carlos Sainz" , value = "SAI" , inline = False)
    embed.add_field(name = "Charles Leclerc" , value = "LEC" , inline = False)
    embed.add_field(name = "Fernando Alonso" , value = "ALO" , inline = False)
    embed.add_field(name = "Esteban Ocon" , value = "OCO" , inline = False)
    embed.add_field(name = "Pierre Gasly" , value = "GAS" , inline = False)
    embed.add_field(name = "Yuki Tsunoda" , value = "TSU" , inline = False)
    embed.add_field(name = "Sebastian Vettel" , value = "VET" , inline = False)
    embed.add_field(name = "Lance Stroll" , value = "STR" , inline = False)
    embed.add_field(name = "George Russell" , value = "RUS" , inline = False)
    embed.add_field(name = "Nicholas Latifi" , value = "LAT" , inline = False)
    embed.add_field(name = "Kimi Raikkonen" , value = "RAI" , inline = False)
    embed.add_field(name = "Antonio Giovinazzi" , value = "GIO" , inline = False)
    embed.add_field(name = "Mick Schumacher" , value = "MSC" , inline = False)
    embed.add_field(name = "Nikita Mazepin" , value = "MAZ" , inline = False)
    embed.set_thumbnail(url = "https://www.racecar-engineering.com/wp-content/uploads/2018/03/F1-LOGO.png")
    embed.set_footer(text = "Formula 1")
    await ctx.send(embed = embed)

@bot.command()
async def news(ctx):
    news_page_refresher()
    with open("news.json" , "r") as f:
        data = json.load(f)
    embed = discord.Embed(title = "Latest News" , color = 0xff1801)
    embed.add_field(name = data['primary']['heading'] , value = f'''Tags: {data['primary']['tags']}
URL: {data['primary']['article url']}''' , inline = False)
    embed.add_field(name = data['secondary']['first']['heading'] , value = f'''Tags: {data['secondary']['first']['tags']}
URL: {data['secondary']['first']['article url']}''' , inline = False)
    embed.add_field(name = data['secondary']['second']['heading'] , value = f'''Tags: {data['secondary']['second']['tags']}
URL: {data['secondary']['second']['article url']}''' , inline = False)
    embed.set_image(url = data['primary']['thumbnail'])
    embed.set_thumbnail(url = "https://www.racecar-engineering.com/wp-content/uploads/2018/03/F1-LOGO.png")
    embed.set_footer(text = "Formula 1")
    await ctx.send(embed = embed)

@bot.command()
async def quote(ctx):
    quote_send = random.choice(quotes)
    embed = discord.Embed(description = f"{quote_send}" , color = 0xff1801)
    await ctx.send(embed = embed)
@bot.command()
async def feedback(ctx):
    await ctx.send("Write something!")
    msg = await bot.wait_for('message', timeout=120.0) 
    out = msg.content

    master = bot.get_user(854593489307435009)

    embed = discord.Embed(title = "New Feedback from " , description = f"{ctx.author.name}#{ctx.author.discriminator}" , color = 0xff1801)
    embed.add_field(name = "Message" , value = out , inline = False)
    embed.set_footer(text = "Formula 1")
    embed.set_thumbnail(url = ctx.author.avatar_url)

    await master.send(embed = embed) 

@bot.command()
async def help(ctx):
    embed = discord.Embed(title = "Help" , color = 0xff1801)
    embed.add_field(name = "Race Results" , value = "`.race <race no.> <year>`" , inline = False)
    embed.add_field(name = "All Races" , value = "`.races <year>`" , inline = False)
    embed.add_field(name = "Driver Stats" , value = "`.driver <short-code>`" , inline = False)
    embed.add_field(name = "Team Stats" , value = "`.team <short-code>`" , inline = False)
    embed.add_field(name = "Driver Standings" , value = "`.drivers <year>`" , inline = False)
    embed.add_field(name = "Team Standings" , value = "`.teams <year>`" , inline = False)
    embed.add_field(name = "Driver short-codes" , value = "`.drivershorts`" , inline = False)
    embed.add_field(name = "Team short-codes" , value = "`.teamshorts`" , inline = False)
    embed.add_field(name = "F1 Quote" , value = "`.quote`" , inline = False)
    embed.add_field(name = "Bot Info" , value = "`.info`" , inline = False)
    embed.add_field(name = "Help" , value = "`.help`" , inline = False)
    embed.set_footer(text = "Formula 1")
    await ctx.author.send(embed = embed)
    await ctx.send("A help menu has been sent to you.")

@bot.command()
async def info(ctx):
    creation , not_req = str(bot.user.created_at).split(" ")
    
    embed = discord.Embed(title = "Bot Info" , color = 0xff1801)
    embed.add_field(name = "Name" , value = f"{bot.user.name}#{bot.user.discriminator}" , inline = False)
    embed.add_field(name = "Created on" , value = creation , inline = False) 
    embed.add_field(name = "By" , value = "Shuvam586#9909" , inline = False)
    embed.set_footer(text = "Formula 1")
    await ctx.send(embed = embed)

Token = os.environ['Token']
keep_alive()
bot.run(Token)