from discord.ext import commands
import discord
import requests



# get API keys from environment variables
TOKEN='Your Token'

bot = discord.Client()#Creates Client
bot = commands.Bot(command_prefix='!')#Sets prefix for commands(!Command)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def define(ctx, word):
    await ctx.send(embed = getDefinition(word))

@bot.command()
async def synonyms(ctx, word):
    await ctx.send(embed = getSynonym(word))    

def getDefinition(word):
    request = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en_US/" + word)
    embed = discord.Embed()
    
    if (request.status_code == 200):
        request = request.json()[0]

        phonetics = "/" 
        for i in request["phonetics"]:
            phonetics += i["text"][1:-1] + ", "
        phonetics = phonetics[:-2] + "/"

        embed = discord.Embed(
            title = word[0].upper() + word[1:].lower() + " | Definitions",
            #description = phonetics + "\n",
            colour= discord.Colour.green()                
        )

        for i in request["meanings"]:
            definition = "⠀⠀" + i["definitions"][0]["definition"] + "\n"
            if ("example" in i["definitions"][0]):
                definition += "⠀⠀_\"" + i["definitions"][0]["example"] + "_\""
            embed.add_field(
                name = "_" + i["partOfSpeech"] + "_",
                value = definition,
                inline = False
            )
        
    elif (request.status_code == 404):
        embed = discord.Embed(
            title ="Error",
            description = "No definitions found for \"" + word + "\".",
            colour = discord.Colour.gold()
        )
        
    return embed  

def getSynonym(word):
    request = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en_US/" + word)
    embed = discord.Embed()

    if (request.status_code == 200):
        request = request.json()[0]

        allSynonyms = ""
        for i in request["meanings"]:
            if ("synonyms" in i["definitions"][0]):
                for synonym in i["definitions"][0]["synonyms"]:
                    allSynonyms += synonym[0].upper() + synonym[1:].lower() + "\n"
        
        embed = discord.Embed(
            title = word[0].upper() + word[1:].lower() + " | Synonyms",
            description = allSynonyms,
            colour= discord.Colour.blue()                
        )
        
    elif (request.status_code == 404):
        embed = discord.Embed(
            title ="Error",
            description = "No synonyms found for \"" + word + "\".",
            colour = discord.Colour.gold()
        )
        
    return embed
    




bot.run(TOKEN)