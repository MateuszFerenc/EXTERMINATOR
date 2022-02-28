from threading import Thread
from datetime import datetime
import discord
import os
import random
import atexit
import time
import json

app_name = "EXTERMINATOR"
cmd_prefix = 'E>'


def print_help():
    page = f"**{app_name}** commands help (Command prefix **{cmd_prefix}**):\n"
    page += "\n• Non Admin commands •\n"
    for command in nonadmin_commands.keys():
        page += f"***{command}*** : {nonadmin_commands[command]}\n"
    page += "\n• Admin commands •\n"
    for command in admin_commands.keys():
        page += f"***{command}*** : {admin_commands[command]}\n"
    return page


async def send_embed_help(message, data):
    if data is None:
        return 3
    embed = discord.Embed(
        title="Help",
        description=data,
        color=0xC00000
    )
    await message.channel.send(embed=embed)


def exit_handler():
    print("Clean exit")


atexit.register(exit_handler)


def miniEXTERMINATOR(client):
    print("miniEXTERMINATOR thread created!")

    while True:
        a = 5


class EXTERMINATOR(discord.Client):
    def __init__(self, *args, **kwargs):

        super(EXTERMINATOR, self).__init__(*args, **kwargs)

        # self.config = config
        self.ready = False
        self.name = app_name
        self.command_prefix = cmd_prefix

    async def on_ready(self):
        print('Logged and ready as {0.user}'.format(self))
        print('Connected to:')
        for server in self.guilds:
            print("%s - %s" % (server.id, server.name))
        if not self.ready:
            Thread(target=miniEXTERMINATOR, args=(self,), daemon = True).start()
        self.ready = True

    async def on_message(self, message):
        if self.ready:
            await handle_message(self, message)

    async def on_message_edit(self, before, after):
        if self.ready:
            await handle_message(self, after)

    async def on_member_join(self, member):
        if not self.ready:
            return
        print('{0} joined!'.format(member.name))
        channel = await member.create_dm()
        embed = discord.Embed(
            title=':smiley: Witaj {} :wave:'.format(member.name),
            description='Z przyjemnością gościmy Cię na {}.\n\nZanim jednak otrzymasz możliwość '
                        'korzystania z naszego serwera, będziesz musiał się zweryfikować.'.format(member.guild.name),
            color=0xC00000
        )
        await channel.send(embed=embed)
        await user_verify_pl(self, member, channel)


async def handle_message(self, message):
    if self.ready:
        if message.author != ex.user:
            if message.guild is not None:
                if message.content.startswith("E>"):
                    msg = message.content.replace('E>', '')

                    # Users commands
                    if msg == 'hello':
                        await message.channel.send('Hello!')

                    if msg == 'ping':
                        ping = round(ex.latency, 1)
                        speed = ''
                        if ping <= 10:
                            speed = 'Super fast :rocket:'
                        elif ping <= 30:
                            speed = 'Quite fast :rabbit:'
                        elif ping <= 100:
                            speed = 'Sloow :turtle:'
                        else:
                            speed = 'Terrible :sob:'
                        await message.channel.send('pong! \n{0} {1} ms'.format(speed, ping))

                    if msg == '':
                        await message.channel.send('Yep that\'s me')

                    if msg == 'whereami':
                        await message.channel.send('You are on {} server!'.format(message.guild.name))

                    if msg == 'help':
                        await send_embed_help(message, print_help())

                    # Admin commands
                    if message.author.guild_permissions.administrator:
                        if message.content == 'hello':
                            await message.channel.send('Hi Admin!')
                        if 'set_verify_method' in msg:
                            msg = list(msg.split())
                            if msg[1] in verify_types_str:
                                global verify_method
                                verify_method = verify_types_str.index(msg[1])
                                await message.channel.send('Verification method set to {0}'.format(msg[1]))
                            else:
                                await message.channel.send(
                                    ':octagonal_sign:  ERROR!  :octagonal_sign: \nInvalid argument => {0} <='.format(
                                        msg[1]))
                        if 'set_verify_depth' in msg:
                            msg = list(msg.split())
                            if int(msg[1]) in list(range(1, verify_obj_count)):
                                global verify_depth
                                verify_depth = int(msg[1])
                                await message.channel.send('Verification depth set to {0}'.format(msg[1]))
                            else:
                                await message.channel.send(
                                    ':octagonal_sign:  ERROR!  :octagonal_sign: \nInvalid value => {0} <='.format(
                                        msg[1]))
                        if 'set_verified_role' in msg:
                            await message.channel.send(
                                ':construction: Under construction :construction: \nSoon available :construction_worker:')
                        if 'set_verify_new' in msg:
                            await message.channel.send(
                                ':construction: Under construction :construction: \nSoon available :construction_worker:')
                        if 'verify_user' in msg:
                            await message.channel.send(
                                ':construction: Under construction :construction: \nSoon available :construction_worker:')
                        if 'verify_bulk' in msg:
                            await message.channel.send(
                                ':construction: Under construction :construction: \nSoon available :construction_worker:')
                        if 'set_ghosting' in msg:
                            await message.channel.send(
                                ':construction: Under construction :construction: \nSoon available :construction_worker:')
                        if 'set_warning' in msg:
                            await message.channel.send(
                                ':construction: Under construction :construction: \nSoon available :construction_worker:')
                        if 'set_kick' in msg:
                            await message.channel.send(
                                ':construction: Under construction :construction: \nSoon available :construction_worker:')
            else:
                if message.content != "":
                    channel = await message.author.create_dm()
                    await channel.send(
                        ':construction: Under construction :construction: \nSoon available :construction_worker:')


async def user_verify_pl(self, user, channel):
    if not self.ready:
        return
    verify_emojis = []
    verify_emojis_raw = []
    for emoji in range(verify_depth):
        emoji_raw = verify_types[verify_method][random.randrange(0, len(verify_types[verify_method]))]
        verify_emojis.append(":" + emoji_raw + ":")
        verify_emojis_raw.append(emoji_raw)

    embed = discord.Embed(
        title="Weryfikacja",
        description='Aby tego dokonać, musisz wypisać w tej samej kolejności nazwy tych emoji (po przecinku i po '
                    'angielsku!) \n{0}'.format(
                                                ' , '.join(verify_emojis)),
        color=0xC00000
    )
    await channel.send(embed=embed)
    dc['Users2Verify'] = dc['Users2Verify'] + 1
    updated = False
    for i in range(len(dc['Users2VerifyData'])):
        if dc['Users2VerifyData'][i]['uname'] is None:
            dc['Users2VerifyData'][i]['uname'] = user.name
            dc['Users2VerifyData'][i]['udate'] = datetime.today().strftime('%Y-%m-%d-%H:%M')
            dc['Users2VerifyData'][i]['ucode'] = verify_emojis_raw
            updated = True

    if not updated:
        data = {
            "uname": user.name,
            "udate": datetime.today().strftime('%Y-%m-%d-%H:%M'),
            "ucode": verify_emojis_raw
        }
        dc['Users2VerifyData'].append(data)

    with open("data_container.json", "w") as data_container_write:
        json.dump(dc, data_container_write, indent=4)


animals = ["cow", "dog", "cat", "mouse", "hamster", "rabbit", "fox", "bear", "koala", "tiger", "lion", "pig", "frog",
           "monkey", "chicken", "penguin", "bird", "duck", "eagle", "owl", "bat", "wolf", "horse", "hedgehog"]

vegetables = ["watermelon", "banana", "pear", "orange", "apple", "lemon", "grapes", "blueberries", "strawberry",
              "melon", "cherries", "peach", "mango", "pineapple", "coconut", "kiwi", "tomato", "avocado", "carrot",
              "garlic", "onion", "potato", "corn", "broccoli"]

verify_obj_count = 24  # counting from 1

verify_types = [animals, vegetables]
verify_types_str = ["animals", "vegetables"]

nonadmin_commands = {
    "help": "Prints bot commands and its description",
    "hello": "Greets user with \"Hello!\"",
    "ping": "Do I hear Ping-Pong? Lets check the connection latency",
    "whereami": "Prints guild/server name"
}

admin_commands = {
    "DATA TYPES": " -> <integer> <bool><text><text_multi>",
    "set_verify_method": " <text> : Set user verification method to <text>\nAvailable methods: {}".format(
        ", ".join(verify_types_str)),
    "set_verify_depth": " <integer> : Set user verification method to <integer> depth\n<integer> must vary between <1, {}>".format(
        verify_obj_count),
    "set_verified_role": " <text> : Set <text> to role of verified user",
    "set_verify_new": " <bool> : <bool> 0 - new users won't be verified | 1 - new users will be verified",
    "verify_user": " <text> : Verifies user <text>",
    "verify_bulk": " <text_multi> : Verifies multiple users on given conditions in <text>\nexample: verify_bulk @everyone not @role0 and not @role1",
    "set_ghosting": " <bool> : <bool> 0 - non verified users ghosting disabled | 1 - enabled\n<integer> represents days to ghost user",
    "set_warning": " <bool> : <bool> 0 - non verified users warn before kick disabled | 1 - enabled\n<integer> represents days to warn user",
    "set_kick": " <bool> : <bool> 0 - non verified users kick disabled | 1 - enabled\n<integer> represents days to kick user",
}

dc = {}
verify_method = 0
verify_depth = 5

try:
    with open("data_container.json", "r") as data_container:
        dc = json.load(data_container)
        print("Data from data_container.json, successfully read")
except FileNotFoundError:
    print("data_container.json file not found!")
    os.abort()

if 'verify_method' in dc:
    verify_method = dc['verify_method']
if 'verify_depth' in dc:
    verify_depth = dc['verify_depth']
if 'bot-token' not in dc:
    dc['bot-token'] = input['No bot-token in data_container.json, enter it please\n>']

# TTODO's
# 1) Implement saving bot-token into json
# 2) Implement second thread functions (ie. remote bot control, live command execution, time handler)
# 3) Implement user deletion from json, when user leaved server (maybe implement left members logger)
# 4) Implement user verification - half done
# 5) Be happy and positive :)

while True:
    try:
        intents = discord.Intents.default()
        intents.members = True
        ex = EXTERMINATOR(intents=intents)
        ex.run(dc['bot-token'])
    except Exception as exception:
        print(f"{type(exception)}\n{exception}")
        print("Error! Retrying in 10 seconds..")
        time.sleep(10)
