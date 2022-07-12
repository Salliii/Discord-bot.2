import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.utils import get
from threading import *
import datetime
import asyncio
import random
import atexit
import time
import os



client = commands.Bot(command_prefix = '!')
status = ''
token = ''

UserLog = '_UserLog'
ConsoleLog = '_ConsoleLog'
ServerLog = '_ServerLog'

ruleList = [('Spam', 'Das spammen von Nachrichten in den Textkanälen ist untersagt und wird durch den Bot verhindert.'),\
            ('Beleidigungen', 'Das Beleidigen anderer ist Verboten und wird so gut es geht durch den Bot verhindert.'),\
            ('Private Daten', 'Bitte schick keine privaten Daten in die Textkanäle. Diese Regel dient ausschließlich dem eigenen Schutz, wird aber nicht durch den Bot verhindert.'),\
            ('Verhalten', 'Bitte sei freundlich und fair den anderen gegenüber.'),\
            ('Inhalte', 'Das Verschicken von sexistischen, rassistischen, pornografischen und diskriminierenden Nachrichten und Inhalten ist Verboten.')]
drehenIconList = [(0.7,50,'🥐'),(0.7,50,'🥐'),\
                  (0.8,100,'🥯'),(0.8,100,'🥯'),\
                  (0.9,150,'🍞'),(0.9,150,'🍞'),(0.9,150,'🍞'),\
                  (1,200,'🥖'),(1,200,'🥖'),(1,200,'🥖'),\
                  (1.1,250,'🥨'),(1.1,250,'🥨'),\
                  (1.2,300,'🥪'),(1.2,300,'🥪'),\
                  (1.4,350,'🥠'),\
                  (1.6,500,'❓')]





def console(input, type):
    if type == 0:
        console_entry = str(datetime.datetime.now())[:19] + ' | >>>' + str(input)
    elif type == 1:
        if input.author != client.user:
            console_entry = str(datetime.datetime.now())[:19] + ' | ' + str(input.author) + ' ' + str(((input.content).encode('unicode-escape').decode('utf-8')))
    try:
        with open(ConsoleLog, 'a')as console_log:
            console_log.write(console_entry+'\n')
    except:
        pass
console('bot starting...', 0)

def offline():
    console('bot offline', 0)



@client.event
async def on_ready():
    console('bot started', 0)
    if status != '':
        await client.change_presence(activity=discord.Streaming(status))

@client.event
async def on_message(message):
    console(message, 1)
    await client.process_commands(message)

@client.group(invoke_without_command=True, aliases=['Regeln'])
async def regeln(ctx):
    console(f'Successfully issued the rules to {ctx.message.author} in {ctx.message.channel}', 0)
    embed = discord.Embed(title='Regeln', description='Die folgenden Regeln sollen eingehalten werden und werden durch die Admins und den Bot so gut es geht kontrolliert.')
    for rules in ruleList:
        embed.add_field(name=f'```- {rules[0]}```', value=f'{rules[1]}', inline=False)
    await ctx.send(embed=embed)

@client.command(aliases=['Purge'])
async def purge(ctx):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.channel.purge()
        console(f'successfully cleared {ctx.message.channel} by {ctx.message.author}', 0)



@client.command(aliases=['Brötchen'])
async def brötchen(ctx):
    brötchenMember = []
    with open(UserLog, 'r')as brötchenAmount:
        splitInLines = (brötchenAmount.read()).split('\n')
    for line in range(len(splitInLines)):
        if splitInLines[line] == '':
            pass
        else:
            Segments = splitInLines[line].split(',')
            brötchenMember.append(int(Segments[0]))
    if int(ctx.author.id) in brötchenMember:
        with open(UserLog, 'r')as brötchenAmount:
            splitInLines = (brötchenAmount.read()).split('\n')
        for line in range(len(splitInLines)):
            if splitInLines[line] == '':
                pass
            else:
                Segments = splitInLines[line].split(',')
            
                if int(ctx.author.id) == int(Segments[0]):
                    if int(Segments[1]) == 0:
                        output = None
                    else:
                        output = f'{ctx.message.author.mention} du hast {Segments[1]} Brötchen.'
                        amount = Segments[1]
                else:
                    pass    
    else:
        output = 'Create'

    if output == None:
        await ctx.send(f'{ctx.message.author.mention} du hast leider noch keine Brötchen.')
    elif output == 'Create':
        with open(UserLog, 'a')as brötchenAmount:
            brötchenAmount.write(f'{str(ctx.author.id)},0,0,0\n')                                                                                                                   #UserSync
        await ctx.send(f'{ctx.message.author.mention} du hast leider noch keine Brötchen.')
    else:
        await ctx.send(output)
    console(f'successfully issued the "Broetchenstand" ({amount}) to {ctx.message.author} in {ctx.message.channel}', 0)

@client.command(aliases=['Drehen'])
async def drehen(ctx):
    brötchenMember = []
    with open('BrötchenAmount', 'r')as brötchenAmount:
        splitInLines = (brötchenAmount.read()).split('\n')
    for line in range(len(splitInLines)):
        if splitInLines[line] == '':
            pass
        else:
            Segments = splitInLines[line].split(',')
            brötchenMember.append(int(Segments[0]))

    if int(ctx.author.id) in brötchenMember:
        pass
    else:
        with open('BrötchenAmount', 'a')as brötchen_amount:
            brötchen_amount.write(f'{str(ctx.author.id)},0,0,0\n')                                                                                                                  #UserSync

    with open('BrötchenAmount', 'r')as brötchenAmount:
        splitInLines = (brötchenAmount.read()).split('\n')
    for line in range(len(splitInLines)):
        if splitInLines[line] == '':
            pass
        else:
            Segments = splitInLines[line].split(',')
            if int(Segments[0]) == int(ctx.author.id):
                result = 0
                if (time.time() - float(Segments[2])) > 300:
                    drehenmessage = await ctx.send(f'{drehenIconList[random.randint(0, int(len(drehenIconList)-1))][2]}{drehenIconList[random.randint(0, int(len(drehenIconList)-1))][2]}{drehenIconList[random.randint(0, int(len(drehenIconList)-1))][2]}')
                    for roll in range(5):
                        Icon_1 = drehenIconList[random.randint(0, int(len(drehenIconList)-1))]
                        Icon_2 = drehenIconList[random.randint(0, int(len(drehenIconList)-1))]
                        Icon_3 = drehenIconList[random.randint(0, int(len(drehenIconList)-1))]
                        result = int(Icon_1[0] * (Icon_2[1] - (Icon_3[1])))
                        if f'{Icon_1[2]}{Icon_1[2]}{Icon_1[2]}' == '❓❓❓':
                            result = random.randint(200, 1000)
                        elif Icon_1 == Icon_2 and Icon_1 == Icon_3:
                            result = result + Icon_1[1]
                        elif Icon_1 == Icon_2 or Icon_1 == Icon_3 or Icon_2 == Icon_3:
                            result = result + 50
                        else:
                            pass
                        await drehenmessage.edit(content=f'{Icon_1[2]}{Icon_2[2]}{Icon_3[2]}')
                    if result > 0:
                        await ctx.send(f'{ctx.message.author.mention} du hast {int(result)} Brötchen bekommen.')
                    elif result < 0:
                        await ctx.send(f'{ctx.message.author.mention} du hast {str(int(result))[1:]} Brötchen verloren.')
                    elif result == 0:
                        await ctx.send(f'{ctx.message.author.mention} du bekommst keine Brötchen.')
                    console(f'successfully turned the "Broetchen Rad" ({int(result)}) for {ctx.message.author} in {ctx.message.channel}', 0)

                    brötchen = int(Segments[1])+result
                    if brötchen < 0:
                        brötchen = 0
                        await ctx.send('Da du nicht genug Brötchen hast, wurde dein Brötchenstand auf 0 zurückgesetzt.')
                    with open('brötchenAmount', 'w')as brötchenAmount:
                        brötchenAmount.write('')
                    with open('brötchenAmount', 'a')as brötchenAmount:
                        for writeLine in range(len(splitInLines)):
                            if str(splitInLines[writeLine]) == '':
                                pass
                            else:
                                if writeLine == line:
                                    brötchenAmount.write(str(f'{str(ctx.author.id)},{str(brötchen)},{time.time()},{Segments[3]}\n'))                                                #UserSync
                                else:
                                    brötchenAmount.write(str(splitInLines[writeLine])+'\n')

                else:
                    await ctx.send(f'{ctx.message.author.mention} du musst noch {int((300-(time.time()-float(Segments[2])))/60)} Minuten und {int((300-(time.time()-float(Segments[2]))) - (int((300-(time.time()-float(Segments[2])))/60)*60))} Sekunden warten.')
                    console(f'unsuccessfully turned the "Broetchen Rad" (time) for {ctx.message.author} in {ctx.message.channel}', 0)

@client.command(aliases=['Würfeln'])
async def würfeln(ctx):
    brötchenMember = []
    with open(UserLog, 'r')as brötchenAmount:
        splitInLines = (brötchenAmount.read()).split('\n')
    for line in range(len(splitInLines)):
        if splitInLines[line] == '':
            pass
        else:
            Segments = splitInLines[line].split(',')
            brötchenMember.append(int(Segments[0]))

    if int(ctx.author.id) in brötchenMember:
        pass
    else:
        with open(UserLog, 'a')as brötchen_amount:
            brötchen_amount.write(f'{str(ctx.author.id)},0,0,0\n')                                                                                                                  #UserSync

    with open(UserLog, 'r')as brötchenAmount:
        splitInLines = (brötchenAmount.read()).split('\n')
    for line in range(len(splitInLines)):
        if splitInLines[line] == '🎲':
            pass
        else:
            Segments = splitInLines[line].split(',')
            if int(Segments[0]) == int(ctx.author.id):
                result = 0
                if (time.time() - float(Segments[3])) > 60:
                    würfelnMessage = await ctx.send('a')
                    dice = random.randint(1,6)
                    result = -150+(dice * 50)
                    if result < 0:
                        await ctx.send(f'{ctx.message.author.mention} du hast eine {dice} gewürfelt und {str(int(result))[1:]} Brötchen verloren.')
                    elif result == 0:
                        await ctx.send(f'{ctx.message.author.mention} du hast eine {dice} gewürfelt und keine Brötchen bekommen.')
                    elif result > 0 :
                        await ctx.send(f'{ctx.message.author.mention} du hast eine {dice} gewürfel und {result} Brötchen gewonnen.')
                    result = int(Segments[1]) + result
                    if result < 0:
                        result = 0
                        await ctx.send('Da du nicht genug Brötchen hast, wurde dein Brötchenstand auf 0 zurückgesetzt.')
                    console(f'successfully rolled the "Broetchen Würfel" ({int(result)}) for {ctx.message.author} in {ctx.message.channel}', 0)
                    with open(UserLog, 'w')as brötchenAmount:
                        brötchenAmount.write('')
                    with open(UserLog, 'a')as brötchenAmount:
                        for writeLine in range(len(splitInLines)):
                            if str(splitInLines[writeLine]) == '':
                                pass
                            else:
                                if writeLine == line:
                                    brötchenAmount.write(str(f'{str(ctx.author.id)},{str(result)},{Segments[2]},{time.time()}\n'))                                                  #UserSync
                                else:
                                    brötchenAmount.write(str(splitInLines[writeLine])+'\n')
                else:
                    await ctx.send(f'{ctx.message.author.mention} du musst noch {int(60-(time.time()-float(Segments[3])))} Sekunden warten.')
                    console(f'unsuccessfully rolled the "Broetchen Würfel" (time) for {ctx.message.author} in {ctx.message.channel}', 0)

@client.command(aliases=['Wettbacken'])
async def wettbacken(ctx):
    sleepAnnouncement = 1
    sleepStart = 1
    sleepResult = 10
    sleepCooldown = 10
    
    with open(ServerLog, 'r')as ServerLogFile:
        ServerLogLines = (ServerLogFile.read()).split('\n')
    for ServerLogLine in ServerLogLines:
        if (ServerLogLine.split(' = '))[0] == 'log.wettbacken':
            active, cooldown, host, member = ((ServerLogLine.split(" = "))[1]).split(',')
            member = ((member[1:])[:-1]).split('/')
        else:
            pass
    if cooldown == 'True':
        await ctx.send(f'{ctx.author.mention} du musst noch warten, bis ein neues Wettbacken gestartet werden kann.')
    elif active == 'True':
        await ctx.send(f'{ctx.author.mention} es findet bereits ein Wettbacken teil. Du musst warten bis dieses rum ist.')
    else:
        if host == ' ':
            with open(ServerLog, 'r')as ServerLogFile:
                ServerLogLines = (ServerLogFile.read()).split('\n')
            with open(ServerLog, 'w')as ServerLogFile:
                for ServerLogLine in ServerLogLines:
                    if (ServerLogLine.split(' = '))[0] == 'log.wettbacken':
                        SubSegment = ((ServerLogLine.split(' = '))[1]).split(',')
                        ServerLogFile.write(f'log.wettbacken = False,False,{ctx.author.id},()\n')
                    elif ServerLogLine == '':
                        pass
                    else:
                        ServerLogFile.write(ServerLogLine+'\n')
            await ctx.send(f'{ctx.author.mention} du hast hiermit die Anmeldung für ein Wettbacken gestartet.')

            await ctx.send('@everyone wer an dem Wettbacken teilnehmen möchte kann dies durch den Befehl **!wettbacken** tun')
            await asyncio.sleep(sleepAnnouncement)

            await ctx.send(f'@everyone das Wettbacken startet in {sleepStart}Minuten. Gib **!wettbacken** ein um teilzunehmen.')
            await asyncio.sleep(sleepStart)

            with open(ServerLog, 'r')as ServerLogFile:
                ServerLogLines = (ServerLogFile.read()).split('\n')
            for ServerLogLine in ServerLogLines:
                if (ServerLogLine.split(' = '))[0] == 'log.wettbacken':
                    active, Cooldown, host, member = ((ServerLogLine.split(" = "))[1]).split(',')
                    member = ((member[1:])[:-1]).split('/')
                else:
                    pass
            for addMemberRole in member:
                await #.add_roles(get(ctx.guild.roles,name='Wettbackteilnehmer/in'))
            await ctx.send(f'{get(ctx.guild.roles,name="Wettbackteilnehmer/in").mention} Das Wettbacken hat gestartet. Die Ergebnisse werden in {sleepResult} Minuten bekannt gegeben.')

            with open(ServerLog, 'r')as ServerLogFile:
                ServerLogLines = (ServerLogFile.read()).split('\n')
            with open(ServerLog, 'w')as ServerLogFile:
                for ServerLogLine in ServerLogLines:
                    if (ServerLogLine.split(' = '))[0] == 'log.wettbacken':
                        SubSegment = ((ServerLogLine.split(' = '))[1]).split(',')
                        ServerLogFile.write(f'log.wettbacken = True,False,{SubSegment[1]},{SubSegment[2]}\n')
                    elif ServerLogLine == '':
                        pass
                    else:
                        ServerLogFile.write(ServerLogLine+'\n')
            await asyncio.sleep(sleepResult)
            resultMember = []
            with open(ServerLog, 'r')as ServerLogFile:
                ServerLogLines = (ServerLogFile.read()).split('\n')
            for ServerLogLine in ServerLogLines:
                if (ServerLogLine.split(' = '))[0] == 'log.wettbacken':
                    active, Cooldown, host, member = ((ServerLogLine.split(" = "))[1]).split(',')
                    member = ((member[1:])[:-1]).split('/')
                else:
                    pass
            for addMember in member:
                resultMember.append(int(addMember))
            resultMember.append(int(host))
            result = resultMember[random.randint(1,len(resultMember))]
            await ctx.send(f'{get(ctx.guild.roles,name="Wettbackteilnehmer/in").mention} Der gewinner ist {(client.fetch_user(int(result))).mention}. Du gewinnst 150 Brötchen')
            with open(ServerLog, 'r')as ServerLogFile:
                ServerLogLines = (ServerLogFile.read()).split('\n')
            with open(ServerLog, 'w')as ServerLogFile:
                for ServerLogLine in ServerLogLines:
                    if (ServerLogLine.split(' = '))[0] == 'log.wettbacken':
                        SubSegment = ((ServerLogLine.split(' = '))[1]).split(',')
                        ServerLogFile.write(f'log.wettbacken = False,True, ,())\n')
                    elif ServerLogLine == '':
                        pass
                    else:
                        ServerLogFile.write(ServerLogLine+'\n')
            await asyncio.sleep(sleepCooldown)
            with open(ServerLog, 'r')as ServerLogFile:
                ServerLogLines = (ServerLogFile.read()).split('\n')
            with open(ServerLog, 'w')as ServerLogFile:
                for ServerLogLine in ServerLogLines:
                    if (ServerLogLine.split(' = '))[0] == 'log.wettbacken':
                        SubSegment = ((ServerLogLine.split(' = '))[1]).split(',')
                        ServerLogFile.write(f'log.wettbacken = False,False, ,())\n')
                    elif ServerLogLine == '':
                        pass
                    else:
                        ServerLogFile.write(ServerLogLine+'\n')



        else:
            if str(ctx.author.id) in member:
                await ctx.send(f'{ctx.author.mention} du hast bereits an diesem Wettbacken teilgenommen.')
                pass
            elif str(ctx.author.id) == str(host):
                await ctx.send(f'{ctx.author.mention} du bist bereits der Host dieses Wettbackens.')
                pass
            else:
                await ctx.author.add_roles(get(ctx.guild.roles,name='Wettbackteilnehmer/in'))
                with open(ServerLog, 'r')as ServerLogFile:
                    ServerLogLines = (ServerLogFile.read()).split('\n')
                with open(ServerLog, 'w')as ServerLogFile:
                    for ServerLogLine in ServerLogLines:
                        if (ServerLogLine.split(' = '))[0] == 'log.wettbacken':
                            SubSegment = ((ServerLogLine.split(' = '))[1]).split(',')
                            member.append(str(ctx.author.id))
                            ServerLogFile.write(f'log.wettbacken = False,False,{SubSegment[1]},({("/".join(member))[1:]})\n')
                        elif ServerLogLine == '':
                            pass
                        else:
                            ServerLogFile.write(ServerLogLine+'\n')
                await ctx.send(f'{ctx.author.mention} du nimmst hiermit an dem Wettbacken teil.')

            


                

atexit.register(offline)
client.run(token)
