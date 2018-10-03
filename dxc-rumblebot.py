import discord, os, subprocess

client = discord.Client()
ADMINS = []

#Loads token from secrets file
DISCORD_TOKEN = ''
with open('/projects/rumblebot/rumblebot-secrets') as f:
    for l in f.read().split('\n'):
        if 'rumblebot_token' in l:
            DISCORD_TOKEN = l.split(':')[1]
        if 'admin' in l:
            ADMINS.append(l.split(':')[1])

#Grabs data from specified url
#def get_url(url):
#    r = requests.get(url)
#    return r

#Grabs the botserver public IP
#def get_public_ip():
#    public_ip = get_url('http://jsonip.com')
#    public_ip = public_ip.json()['ip']
#    return public_ip

#Used for bot cleanup, checks if message is from bot
def is_me(message):
    return message.author == client.user

#Used for bot cleanup, checks if message is a bot command
def is_command(message):
    return str(message.content).split(' ')[0] in ['!hello']

#run system command
def command(system_command):
    try:
        CMD = subprocess.Popen(system_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        return CMD.stdout, CMD.stderr
    except Exception as e:
        pass

#Actions bot takes on messages in Discord channel
@client.event
async def on_message(message):

    #User checks with bot if they are subscribed or not
    if message.content.startswith('!hello'):
        await client.send_message(message.channel, 'Hi!')


    #User wants to see their individual player stats
    if message.content == '!embed':
        embed = discord.Embed(title='Embed', description='Testing Embed', colour=0xDEADBF)
        embed.add_field(name="Field1", value='Field1_Text')
        embed.add_field(name="Field2", value='Field2_Text')
        embed.add_field(name="Field3", value='Field3_Text')
        await client.send_message(message.channel, embed=embed)

    if message.content == '!id':
        await client.send_message(message.channel, str(message.author.id))

    if message.content == '!disconnect rumblebot' and message.author.id in ADMINS:
        await client.logout()

    if message.content == '!rebuild rumblebot' and message.author.id in ADMINS:
        await client.logout()
        os.system('/projects/rumblebot/rebuild-rumblebot.py &')

    if message.content.startswith('!setplaying') and message.author.id in ADMINS:
        game_title = message.content.replace('!setplaying ', '')
        await client.change_presence(game=discord.Game(name=game_title), status=discord.Status("online"))

    if message.content.startswith('!rumblebot') and message.author.id in ADMINS:
        try:
            system_command = message.content.replace('!rumblebot ', '')
            c = command(system_command)
            stdout = c[0].read().decode("utf-8")
            stderr = c[1].read().decode("utf-8")

            #regular length message
            #stdout
            if stdout and len(stdout) < 2000:
                await client.send_message(message.channel, "stdout\n```bash\n" + stdout + "```")
            #stderr
            if stderr and len(stderr) < 2000:
                await client.send_message(message.channel, "stderr\n```bash\n" + stderr + "```")

            #length exceeds discord message limit
            #stdout
            if stdout and len(stdout) > 2000:
                count = math.ceil(len(stdout) / 1950)
                for i in range(0, count):
                    start = i*1950
                    end = (i+1)*1950
                    await client.send_message(message.channel, "stdout\n```bash\n" + stdout[start:end] + "```")
            #stderr
            if stderr and len(stderr) > 2000:
                count = math.ceil(len(stderr) / 1950)
                for i in range(0, count):
                    start = i*1950
                    end = (i+1)*1950
                    await client.send_message(message.channel, "stderr\n```bash\n" + stderr[start:end] + "```")

        #Logs exception
        except Exception as e:
            pass


    #Print help/commands menu
    if message.content in ['!commands','!help']:
        embed = discord.Embed(title='Control', description='Commands for controlling STASI', colour=0xDEADBF)
        embed.add_field(name="Command List", value="""
```bash
!commands               # Shows this menu
```""")
        await client.send_message(message.channel, embed=embed)


#Startup code
#client.loop.create_task(update_task())
client.run(DISCORD_TOKEN)
