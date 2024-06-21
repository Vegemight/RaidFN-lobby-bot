import fortnitepy
import json
import os
import aiohttp
import time
from fortnitepy.party import ReadyState
from fortnitepy.ext import commands as fortnite_commands

print("""
█████████████████████████████████████
█▄─▄▄▀██▀▄─██▄─▄█▄─▄▄▀█▄─▄▄─█▄─▀█▄─▄█
██─▄─▄██─▀─███─███─██─██─▄████─█▄▀─██
▀▄▄▀▄▄▀▄▄▀▄▄▀▄▄▄▀▄▄▄▄▀▀▄▄▄▀▀▀▄▄▄▀▀▄▄▀""")
print("v1.0")
time. sleep(1)

filename = 'device_auths.json'
description = 'Fortnite Bot'

async def fetch_cosmetic(matchMethod: str, name: str, backendType: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://fortnite-api.com/v2/cosmetics/br/search/all?matchMethod={matchMethod}&name={name}&backendType={backendType}") as response:
            data = await response.json()
            if data['data']:
                return data['data'][0]['id']
            else:
                raise Exception('Cosmetic not found.')

def get_device_auth_details():
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open(filename, 'w') as fp:
        json.dump(existing, fp)

print("You can get an auth code from rebrand.ly/authcode")
# Initialize bot with authentication
auth = fortnitepy.AuthorizationCodeAuth(
    code=input("Enter a code: ")
)

bot = fortnite_commands.Bot(
    command_prefix='!',  # Command prefix for your bot
    description=description,  # Description of your bot
    auth=auth  # Pass the authentication method here
)

@bot.event
async def event_ready():
    print(f'Bot launched as {bot.user.display_name}')
    print('Thank you for using RaidFN!')

@bot.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)

@bot.event
async def event_friend_request(request):
    await request.accept()

@bot.event
async def event_friend_message(message):
    print(f'Received fortnite message from {message.author.display_name} | Content "{message.content}"')

@bot.command()
async def skin(ctx, *, content: str):
    try:
        matchMethod = "contains"
        backendType = "AthenaCharacter"
        
        print("Fetching cosmetic...")
        cosmetic_id = await fetch_cosmetic(matchMethod, content, backendType)
        print(f"Received cosmetic ID: {cosmetic_id}")

        print(f"Skin set to: {cosmetic_id}")
        await ctx.send(f'Skin set to {cosmetic_id}.')

        print(f"Attempting to set skin: {cosmetic_id}")
        await bot.party.me.set_outfit(asset=cosmetic_id)
        print("Skin set successfully.")

    except Exception as e:
        await ctx.send(f"Failed to set skin: {e}")
        print(f"Failed to set skin: {e}")


@bot.command()
async def emote(ctx, content: str):
    try:
        cosmetic = await fetch_cosmetic(
            matchMethod="contains",
            name=content,
            backendType="AthenaDance"
        )
        await ctx.send(f'Emote set to {cosmetic}.')
        print(f"Set emote to: {cosmetic}.")
        await bot.party.me.set_emote(asset=cosmetic)

    except Exception as e:
        await ctx.send(f"Failed to find an emote with the name: {content}.")
        print(f"Failed to find an emote with the name: {content}. Error: {e}")

@bot.command()
async def level(ctx, level: int):
    try:
        await ctx.send(f"Setting season level to {level}.")
        await bot.party.me.set_banner(season_level=level)
        print(f"Season level set to {level}.")
    except Exception as e:
        await ctx.send(f"Failed to set season level: {e}")
        print(f"Failed to set season level: {e}")
@bot.command()
async def crowns(ctx, amount: int):
    try:
       meta = client.party.me.meta
        data = (meta.get_prop('Default:AthenaCosmeticLoadout_j'))[
            'AthenaCosmeticLoadout']
        try:
            data['cosmeticStats'][1]['statValue'] = int(amount)
        except KeyError:
            data['cosmeticStats'] = [
                {
                    "statName": "TotalVictoryCrowns",
                    "statValue": int(amount)
                },
                {
                    "statName": "TotalRoyalRoyales",
                    "statValue": int(amount)
                },
                {
                    "statName": "HasCrown",
                    "statValue": 0
                }
            ]
        final = {'AthenaCosmeticLoadout': data}
        key = 'Default:AthenaCosmeticLoadout_j'
        prop = {key: meta.set_prop(key, final)}

        await client.party.me.patch(updated=prop)
        await client.party.me.clear_emote()
        await asyncio.sleep(1)
        await client.party.me.set_emote(asset="EID_Coronet.EID_Coronet")
        return await ctx.send(f"Set Crown Wins To: {amount}")
    except Exception as e:
        await ctx.send(f"Failed to set Crown Wins: {e}")
        print(f"Failed to set Crown Wins: {e}")
@bot.command()
async def discord(ctx):
    await ctx.send("https://discord.gg/2VmQTQVe3B")
    await ctx.send("Join the discord!")

bot.run()
