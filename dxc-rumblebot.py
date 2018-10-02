import discord, os

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
#def command(system_command):
#    try:
#        CMD = subprocess.Popen(system_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
#        return CMD.stdout, CMD.stderr
#    except Exception as e:
#        pass

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

    #Botadmin wants to see botserver public IP
    #if message.content == '!getip':
    #    try:
    #        public_ip = get_public_ip()
    #        embed = discord.Embed(title='System', description='Public IP', colour=0xDEADBF)
    #        embed.add_field(name="IP", value="```\n" + public_ip + "```")
    #        await client.send_message(message.channel, embed=embed)

        #Logs exception
    #    except Exception as e:
    #        pass

    if message.content == '!id':
        await client.send_message(message.channel, str(message.author.id))

    if message.content == '!disconnect rumblebot' and message.author.id in ADMINS:
        await client.logout()

    if message.content == '!rebuild rumblebot' and message.author.id in ADMINS:
        await client.logout()
        os.system('/projects/rumblebot/rebuild-rumblebot.py &')

    if message.content.startswith('!setplaying') and message.author.id in botadmins:
        status = message.content.replace('!setplaying ', '')
        client.change_status(game=discord.Game(name=status))

    #Print help/commands menu
    if message.content in ['!commands','!help']:
        embed = discord.Embed(title='Control', description='Commands for controlling STASI', colour=0xDEADBF)
        embed.add_field(name="Command List", value="""
```bash
!commands               # Shows this menu
```""")
        await client.send_message(message.channel, embed=embed)

#Creates a background stats update task
#async def update_task():
#    await client.wait_until_ready()
#    while not client.is_closed:
#        try:
            #Update user and statistics data and wait 1 hour
#            player.initialize()
#            await asyncio.sleep(3600)

        #Logs exception
#        except Exception as e:
#            os.system('echo "' + str(datetime.datetime.now()) + " Update_task: " + str(e) + '" >> ' + logpath)

#Startup code
#client.loop.create_task(update_task())
client.run(DISCORD_TOKEN)
